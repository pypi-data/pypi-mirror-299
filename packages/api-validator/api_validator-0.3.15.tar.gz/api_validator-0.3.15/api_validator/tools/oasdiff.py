import yaml
from typing import Union
import collections
import json
from os.path import exists
from os import remove
from typing import List, Dict, Optional
import io
from pathlib import Path
from yaml import load, Loader
from api_validator.diff_utils.oasdiff_utils import get_endpoint_method_pairs_from_openapi, get_endpoints_with_parameters, read_file, find_unique_endpoints, match_exclusions
from api_validator.diff_utils.complex_oasdiff_yaml_utils import OasdiffFile


def preprocess_yaml(file_path, new_file_path):
    """
    oasdiff has some annoying complex key structures in yaml and we don't need it. Remove this annoying shit
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    if exists(new_file_path):
        remove(new_file_path)

    with open(new_file_path, 'w') as file:
        previous_line = None
        for i in range(len(lines)):
            line = lines[i]
            if i > 0:
                previous_line = lines[i - 1]
            # Remove question mark from the start of the line
            # while preserving indentation
            if line.lstrip().startswith('?'):
                line = line.replace('?', '', 1)
            file.write(line)


def read_oasdiff_yaml_file(file) -> dict:
    """
    Read the OASDiff YAML file, handling complex keys.

    :param file: The file path of the YAML file.
    :return: The parsed data.
    """
    file_name = Path(file)

    class ComplexKey:
        def __init__(self, value):
            self.value = value

        def __repr__(self):
            return f"{type(self).__name__}({self.value})"

        def __hash__(self):
            return hash(tuple(sorted(self.value.items())) if isinstance(self.value, dict) else self.value)

        def __eq__(self, other):
            return isinstance(other, ComplexKey) and self.value == other.value

    def construct_complex_key(loader, node):
        if node.value == '{}':
            return ComplexKey({})
        return ComplexKey(loader.construct_mapping(node))

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        mapping = {}
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node, deep=True)
            if isinstance(key, dict) and not key:
                key = ComplexKey({})  # Treat empty dict as a special complex key
            elif not isinstance(key, collections.Hashable):
                key = ComplexKey(key)
            value = loader.construct_object(value_node, deep=True)
            mapping[key] = value
        return mapping

    Loader.add_constructor("tag:yaml.org,2002:map", construct_mapping)
    Loader.add_constructor("tag:yaml.org,2002:seq", Loader.construct_sequence)
    Loader.add_constructor("tag:yaml.org,2002:str", Loader.construct_scalar)
    Loader.add_constructor(None, construct_complex_key)

    with io.open(file_name, mode="r", encoding=None) as stream:
        data = load(stream, Loader=Loader)
    return data


def construct_mapping(loader, node):
    loader.flatten_mapping(node)
    mapping = {}

    for key_node, value_node in node.value:
        # Construct the key and ensure it's hashable
        key = loader.construct_object(key_node)

        # Construct the value if it exists
        value = loader.construct_object(value_node) if value_node else None

        # In case the key is a dictionary, convert it to a tuple
        if isinstance(key, dict):
            key = tuple(key.items())

        # Add the constructed key-value pair to the mapping
        mapping[key] = value

    return mapping


class Change:
    def __init__(self, from_value: Optional[str] = None, to_value: Optional[str] = None, **kwargs):        # Assign from_value from the 'from' keyword if present in kwargs
        self.from_value = kwargs.get('from', from_value)
        self.to_value = to_value if to_value is not None else kwargs.get('to')

    def __repr__(self):
        return f"{type(self).__name__}(from={self.from_value}, to={self.to_value})"


class InfoDetail:
    def __init__(self, version: Change):
        self.version = version

    def __repr__(self):
        return f"{type(self).__name__}(version={self.version})"


class OperationChange:
    def __init__(self, added: List[str], deleted: List[str], modified: Dict[str, Change]):
        self.added = added
        self.deleted = deleted
        self.modified = modified


class OperationDetails:
    def __init__(self, tags: Optional[dict] = None, operationID: Optional[Change] = None, responses: Optional[dict] = None, requestBody: Optional[dict] = None):
        self.tags = tags if tags is not None else {}
        self.operationID = operationID if operationID is not None else Change()
        self.responses = responses if responses is not None else {}
        self.requestBody = requestBody if requestBody is not None else {}

    def __repr__(self):
        return f"{type(self).__name__}(tags={self.tags}, operationID={self.operationID}, responses={self.responses}, requestBody={self.requestBody})"


class PathChange:
    def __init__(self, operations: Dict[str, OperationDetails]):
        self.operations = operations

    def __repr__(self):
        return f"{type(self).__name__}(operations={self.operations})"


class PathsDetail:
    def __init__(self, added: Optional[List[str]], modified: Optional[Dict[str, PathChange]], deleted: Optional[List[str]] = None):
        self.added = added
        self.modified = modified
        self.deleted = deleted

    def __repr__(self):
        return f"{type(self).__name__}(added={len(self.added)}, modified={len(self.modified)}, deleted={len(self.deleted) if self.deleted is not None else []})"


class Endpoint:
    def __init__(
            self,
            method: str,
            path: str,
            operationID: Optional[Change] = None,
            responses: Optional[dict] = None,
            tags: Optional[dict] = None,
            parameters: Optional[dict] = None,
            requestBody: Optional[dict] = None,
            deprecated: Optional[dict] = None,
            securityRequirements: Optional[dict] = None,
            **kwargs
    ):
        self.method = method
        self.path = path
        self.parameters = parameters if parameters is not None else {}
        self.operationID = operationID if operationID is not None else Change()
        self.responses = responses if responses is not None else {}
        self.tags = tags if tags is not None else {}
        self.requestBody = requestBody if requestBody is not None else {}
        self.securityRequirements = securityRequirements if securityRequirements is not None else {}
        self.deprecated = deprecated if deprecated is not None else {}
        self.additional_arguments = kwargs

    def __repr__(self):
        return f"{type(self).__name__}(method={self.method}, path={self.path}, parameters={len(self.parameters) if self.parameters is not None else 0})"


class EndpointsDetail:
    def __init__(self, added: List[Endpoint], modified: List[Endpoint], deleted: List[Endpoint] = None):
        self.added = added
        self.modified = modified
        self.deleted = deleted

    def __repr__(self):
        return f"{type(self).__name__}(added={len(self.added)}, modified={len(self.modified)}, deleted={len(self.deleted) if self.deleted is not None else []})"


class ServerChange:
    def __init__(self, url: str, description: Change):
        self.url = url
        self.description = description

    def __repr__(self):
        return f"{type(self).__name__}(url={self.url}, description={self.description})"


class ServersDetail:
    def __init__(self, modified: Dict[str, ServerChange]):
        self.modified = modified

    def __repr__(self):
        return f"{type(self).__name__}(modified={len(self.modified)})"


class ComponentChange:
    def __init__(self, added: List[str], modified: Dict[str, Change]):
        self.added = added
        self.modified = modified

    def __repr__(self):
        return f"{type(self).__name__}(added={len(self.added)}, modified={len(self.modified)})"


class ComponentsDetail:
    def __init__(self, schemas: ComponentChange):
        self.schemas = schemas

    def __repr__(self):
        schema_names = []
        schema_names_modified = [k for k, v in self.schemas.modified.items()]
        if schema_names_modified:
            schema_names.extend(schema_names_modified)
        if self.schemas.added:
            schema_names.extend(self.schemas.added)
        return f"{type(self).__name__}(schemas={schema_names})"


class OasdiffOutput:
    def __init__(
            self,
            open_api: Union[Change, None],
            paths: PathsDetail,
            endpoints: EndpointsDetail,
            components: ComponentsDetail,
            repository_url: Optional[str] = None,
            subdirectory: Optional[str] = None,
            provided_swagger_file: Optional[str] = None,
            new_swagger_file: Optional[str] = None,
            elapsed_time: Optional[float] = None,
            language: Optional[str] = None,
            github_stars: Optional[int] = None,
            exclude_paths: List[str] = None,
            new_spec_component_count: Optional[int] = None,
            old_spec_component_count: Optional[int] = None,
    ):
        self.open_api = open_api
        self.paths = paths
        self.endpoints = endpoints
        self.subdirectory = subdirectory
        self.components = components
        self.elapsed_time = elapsed_time
        self.repository_url = repository_url
        self.provided_swagger_file = provided_swagger_file
        self.new_swagger_file = new_swagger_file
        self.language = language
        self.github_stars = github_stars
        self.exclude_paths = exclude_paths
        self.new_spec_component_count = new_spec_component_count
        self.old_spec_component_count = old_spec_component_count
        # repo_name is the repo from the GitHub url
        self.owner = self.repository_url.split('/')[-2]
        self.repo_name = self.repository_url.split('/')[-1].replace("/", "")

    @staticmethod
    def from_dict(
            data: Dict,
            repository_url: Optional[str] = None,
            subdirectory: Optional[str] = None,
            provided_swagger_file: Optional[str] = None,
            new_swagger_file: Optional[str] = None,
            elapsed_time: Optional[float] = None,
            language: Optional[str] = None,
            github_stars: Optional[int] = None,
            exclude_paths: List[str] = None,
            new_spec_component_count: Optional[int] = None,
            old_spec_component_count: Optional[int] = None,
    ) -> Union['OasdiffOutput', None]:
        """
        # Example usage
        data = {}  # Replace with the actual JSON data
        oasdiff_output = OasdiffOutput.from_dict(data)
        """
        if not data:
            raise ValueError(f"data cannot be empty. Failed to create OasdiffOutput object for {language} on repository {repository_url}")
        try:
            open_api = Change(from_value=data['openAPI']['from'], to_value=data['openAPI']['to'])
        except KeyError:
            open_api = None

        paths_added = data['paths'].get('added', [])
        paths_modified = {}
        if data['paths'].get('modified') is not None:
            for path, details in data['paths']['modified'].items():
                operations = {}
                if "modified" in details['operations']:
                    for method, method_details in details['operations']['modified'].items():
                        if method_details.get('operationID') is not None:
                            operations[method] = OperationDetails(
                                tags=method_details.get('tags'),
                                operationID=Change(**method_details['operationID']),
                                responses=method_details.get('responses'),
                                requestBody=method_details.get('requestBody')
                            )
                paths_modified[path] = PathChange(operations)

        paths = PathsDetail(added=paths_added, modified=paths_modified)

        endpoints_added = []
        endpoints_modified = []
        endpoints_deleted = []
        raw_endpoints = data.get('endpoints', {})
        all_endpoints = set()
        if raw_endpoints:
            for status in ['added', 'modified', 'deleted']:
                endpoints = raw_endpoints.get(status, [])
                for endpoint in endpoints:
                    try:
                        all_endpoints.update(endpoint['path'])
                    # Debugging: TypeError: string indices must be integers, not 'str'
                    except TypeError as e:
                        pass
                all_endpoints.update(endpoint['path'] for endpoint in endpoints)

        skip_endpoints = match_exclusions(list(all_endpoints), exclude_paths)
        skip_endpoints = set(skip_endpoints)

        if raw_endpoints:
            for status, endpoint_list in [('added', endpoints_added), ('modified', endpoints_modified), ('deleted', endpoints_deleted)]:
                for endpoint_info in raw_endpoints.get(status, []):
                    endpoint = Endpoint(**endpoint_info)
                    if endpoint.path in skip_endpoints:
                        print(f"\t\t\tExcluded endpoint: {endpoint.path}")
                        continue
                    endpoint_list.append(endpoint)
                endpoint_list.sort(key=lambda x: (x.path, x.method))

        endpoints = EndpointsDetail(added=endpoints_added, modified=endpoints_modified, deleted=endpoints_deleted)

        try:
            components_added = data['components']["schemas"].get('added', [])
        except KeyError:
            components_added = []
        # sort the components added by name
        components_added = components_added.sort()
        components_modified = {}
        try:
            if data['components']["schemas"].get('modified') is not None:
                for schema_name, schema_details in data['components']["schemas"]['modified'].items():
                    change = Change(**schema_details)
                    components_modified[schema_name] = change
        except KeyError:
            components_modified = {}
        components_schemas = ComponentChange(
            added=components_added,
            modified=components_modified
        )
        components = ComponentsDetail(schemas=components_schemas)

        return OasdiffOutput(
            open_api=open_api,
            paths=paths,
            endpoints=endpoints,
            components=components,
            repository_url=repository_url,
            subdirectory=subdirectory,
            provided_swagger_file=provided_swagger_file,
            new_swagger_file=new_swagger_file,
            elapsed_time=elapsed_time,
            language=language,
            github_stars=github_stars,
            exclude_paths=exclude_paths,
            new_spec_component_count=new_spec_component_count,
            old_spec_component_count=old_spec_component_count,
        )

    @staticmethod
    def from_yaml(
            file_path: str,
            repository_url: Optional[str] = None,
            subdirectory: Optional[str] = None,
            provided_swagger_file: Optional[str] = None,
            new_swagger_file: Optional[str] = None,
            elapsed_time: Optional[float] = None,
            language: Optional[str] = None,
            github_stars: Optional[int] = None,
            exclude_paths: List[str] = None,
            new_spec_component_count: Optional[int] = None,
            old_spec_component_count: Optional[int] = None,
    ) -> Union['OasdiffOutput', None]:
        """
        # Example usage
        file_path = 'path_to_your_yaml_file.yaml'
        oasdiff_output = OasdiffOutput.from_yaml(file_path)
        """
        with open(file_path, 'r') as file:
            content = file.read()
        transformer = OasdiffFile(content)
        transformer.apply_transformations()
        data = transformer.dict()
        return OasdiffOutput.from_dict(
            data=data,
            repository_url=repository_url,
            subdirectory=subdirectory,
            provided_swagger_file=provided_swagger_file,
            new_swagger_file=new_swagger_file,
            elapsed_time=elapsed_time,
            language=language,
            github_stars=github_stars,
            exclude_paths=exclude_paths,
            new_spec_component_count=new_spec_component_count,
            old_spec_component_count=old_spec_component_count,
        )

    def added_endpoints(self):
        endpoints = []
        for item in self.endpoints.added:
            endpoint = {
                "method": item.method,
                "path": item.path,
                "parameters": len(item.parameters),
            }
            endpoints.append(endpoint)
        # Sort them by path, then method
        endpoints = sorted(endpoints, key=lambda x: (x['path'], x['method']))
        return endpoints

    def deleted_endpoints(self):
        endpoints = []
        for item in self.endpoints.deleted:
            endpoint = {
                "method": item.method,
                "path": item.path,
                "parameters": len(item.parameters),
            }
            endpoints.append(endpoint)
        # Sort them by path, then method
        endpoints = sorted(endpoints, key=lambda x: (x['path'], x['method']))
        return endpoints

    def modified_endpoints(self):
        endpoints = []
        for item in self.endpoints.modified:
            endpoint = {
                "method": item.method,
                "path": item.path,
                "parameters": item.parameters,
            }
            if 'deleted' in item.parameters:
                endpoint['deleted_parameters'] = item.parameters['deleted']
            if 'modified' in item.parameters:
                endpoint['modified_parameters'] = item.parameters['modified']
            if 'added' in item.parameters:
                endpoint['added_parameters'] = item.parameters['added']
            if item.requestBody:
                endpoint['requestBody'] = item.requestBody
            endpoints.append(endpoint)
        # Sort them by path, then method
        endpoints = sorted(endpoints, key=lambda x: (x['path'], x['method']))
        return endpoints

    def unmodified_endpoints(self):
        """
        Oasdiff only calculates new, modified, or deleted - it doesn't calculate the ones that were untouched.

        To give a true calculation as to which ones we discovered, we need to calculate the unmodified ones too.

        This helps in cases where the base Swagger file is actually generated by NightVision, or combined NightVision with another spec. We do this for integration tests.
        """
        oasdiff_endpoint_pairs = self.all_oasdiff_endpoints()
        revision_endpoint_pairs = self.all_revision_endpoints()
        unmodified_endpoints = find_unique_endpoints(oasdiff_endpoint_pairs, [(method, path) for method, path in revision_endpoint_pairs])
        # Convert the list of tuples to a list of dicts
        # TODO: We aren't adding parameters here. We probably should and I should file a bug. Tech debt for now.
        unmodified_endpoints = [{"method": item[0], "path": item[1], "parameters": []} for item in unmodified_endpoints]
        # Sort them by path, then method
        endpoints = sorted(unmodified_endpoints, key=lambda x: (x['path'], x['method']))
        return endpoints

    def all_revision_endpoints(self) -> List[tuple]:
        """
        Return a tuple of method/path for all endpoints that were in the revision
        """
        file_content = read_file(self.new_swagger_file)
        endpoints = get_endpoints_with_parameters(file_content)
        return endpoints

    def all_oasdiff_endpoints(self) -> List[tuple]:
        """
        Return a tuple of method/path for all endpoints that were in the oasdiff
        """
        endpoints = []
        for item in self.endpoints.added:
            endpoints.append((item.method, item.path))
        for item in self.endpoints.modified:
            endpoints.append((item.method, item.path))
        return endpoints

    def deleted_security_requirements(self):
        endpoints_with_deleted_security_requirements = []
        # For modified endpoints, calculate how many have "deleted" securityRequirements
        for item in self.endpoints.modified:
            if item.securityRequirements.get('deleted') is not None:
                endpoints_with_deleted_security_requirements.append({"method": item.method, "path": item.path, "deleted_security_requirements": len(item.securityRequirements.get('deleted'))})
        return endpoints_with_deleted_security_requirements

    def deleted_parameters(self):
        """Endpoints with deleted parameters"""
        endpoints_with_deleted_parameters = []
        for item in self.endpoints.modified:
            if item.parameters.get('deleted') is not None:
                endpoints_with_deleted_parameters.append({"method": item.method, "path": item.path, "deleted_parameters": len(item.parameters.get('deleted'))})
        return endpoints_with_deleted_parameters

    def report(self) -> dict:
        """Create a report of the OASDiff output"""
        modified_endpoints = self.modified_endpoints()
        deleted_endpoints = self.deleted_endpoints()
        added_endpoints = self.added_endpoints()
        unmodified_endpoints = self.unmodified_endpoints()
        deleted_parameters = self.deleted_parameters()
        deleted_security_requirements = self.deleted_security_requirements()
        # TODO: Extraction time? Repository details?
        total_discovered = len(self.endpoints.added) + len(self.endpoints.modified) + len(unmodified_endpoints)
        all_total_endpoints = len(self.endpoints.added) + len(self.endpoints.modified) + len(self.endpoints.deleted) + len(unmodified_endpoints)
        success_rate = (total_discovered / all_total_endpoints) * 100
        try:
            component_count_success_rate = (self.new_spec_component_count / self.old_spec_component_count) * 100
            # We shouldn't let it be greater than 100
            if component_count_success_rate > 100:
                component_count_success_rate = 100.0
        except ZeroDivisionError:
            # If the old spec has no components, then we can say the success rate is 100%
            component_count_success_rate = 100.0

        # Merge added_endpoints with unmodified_endpoints
        added_endpoints = added_endpoints + unmodified_endpoints
        added_endpoints = sorted(added_endpoints, key=lambda x: (x['path'], x['method']))
        results = {
            "total_discovered": total_discovered,
            "success_rate": success_rate,
            "success_rate_string": f"{success_rate:.2f}",
            "modified_endpoints": modified_endpoints,
            "deleted_endpoints": deleted_endpoints,
            "added_endpoints": added_endpoints,
            "deleted_parameters": deleted_parameters,
            "deleted_security_requirements": deleted_security_requirements,
            "elapsed_time": int(self.elapsed_time),  # in seconds
            "subdirectory": self.subdirectory,
            "repository_url": self.repository_url,
            "provided_swagger_file": self.provided_swagger_file,
            "language": self.language,
            "repo_name": self.repo_name,
            "owner": self.owner,
            "github_stars": self.github_stars,
            "component_count_success_rate": component_count_success_rate,
            "component_count_success_rate_string": f"{component_count_success_rate:.2f}",
            "new_spec_component_count": self.new_spec_component_count,
            "old_spec_component_count": self.old_spec_component_count,
        }
        return results

    def __repr__(self):
        # new/deleted/modified endpoints, new/deleted/modified components
        return f"{type(self).__name__}(added={self.endpoints.added}, deleted={self.endpoints.deleted}, components={self.components})"



