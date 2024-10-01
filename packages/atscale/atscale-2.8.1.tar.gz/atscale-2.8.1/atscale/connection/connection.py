import getpass
import json
import logging
import time
from typing import Dict, List, Tuple, Union
from cryptography.fernet import Fernet
import requests
from html import unescape
import re
from inspect import getfullargspec

from atscale.errors import atscale_errors
from atscale.utils import request_utils, input_utils, validation_utils
from atscale.base import endpoints, templates, private_enums

import psycopg2

logger = logging.getLogger(__name__)


class _Connection:
    """An object responsible for the fundamental level of connection and communication to AtScale in the explicit
    realm of a user and an organization."""

    def __init__(
        self,
        server: str,
        username: str = None,
        password: str = None,
        organization: str = None,
        design_center_server_port: str = "10500",
        jdbc_driver_class: str = "org.apache.hive.jdbc.HiveDriver",
        jdbc_driver_path: str = "",
        verify: Union[str, bool] = True,
    ):
        """Instantiates a Connection to an AtScale server given the associated parameters. After instantiating,
        _Connection.connect() needs to be called to attempt to establish and store the connection.

        Args:
            server (str): The address of the AtScale server. Be sure to exclude any accidental / or : at the end
            username (str, optional): The username to log in with. Leave as None to prompt if necessary upon calling connect().
            password (str, optional): The password to log in with. Leave as None to prompt if necessary upon calling connect().
            organization (str, optional): The organization id to work in. Can be set later by calling _select_org()
                which will list all and prompt or set automatically if the user only has access to one organization.
            design_center_server_port (str, optional): The connection port for the design center. Defaults to 10500.
            jdbc_driver_class (str, optional): The class of the hive jdbc driver to use. Defaults to org.apache.hive.jdbc.HiveDriver for suggested driver.
            jdbc_driver_path (str, optional): The path to the hive jdbc driver to use. Defaults to '' which will not allow querying via jdbc
            verify (str|bool, optional): Whether to verify ssl certs. Can also be the path to the cert to use. Defaults to True.
        """
        inspection = getfullargspec(self.__init__)
        validation_utils.validate_by_type_hints(inspection=inspection, func_params=locals())

        # use the setter so it can throw exception if server is None
        if len(server) > 0 and server[-1] == "/":
            server = server[:-1]
        self.session = requests.Session()
        self.session.verify = verify
        self._design_center_url = f"{server}:{design_center_server_port}"
        # use the setter so it can throw exception if username is None
        self._username: str = username
        self.__fernet = Fernet(Fernet.generate_key())
        if password:
            self._password = self.__fernet.encrypt(password.encode())
        else:
            self._password = None
        self.jdbc_string = None
        self.jdbc_driver_path = jdbc_driver_path
        self.jdbc_driver_class = jdbc_driver_class
        self._organization = organization
        # token as private var; see: https://docs.python.org/3/tutorial/classes.html#private-variables
        self.__token: str = None
        self._engine_url = None

    @property
    def design_center_url(self) -> str:
        """Getter for the server instance variable

        Returns:
            str: the server string
        """
        return self._design_center_url

    @design_center_url.setter
    def design_center_url(
        self,
        value: str,
    ):
        """Setter for the server instance variable. Resets connection

        Args:
            value (str): the new design_center_url string
        """
        raise atscale_errors.UnsupportedOperationException(
            "The value of design_center_url is final; it cannot be altered."
        )

    @property
    def engine_url(self) -> str:
        """Getter for the engine_url instance variable

        Returns:
            str: the engine_url string
        """
        if not self._engine_url:
            self._set_engine_url()
        return self._engine_url

    @engine_url.setter
    def engine_url(
        self,
        value: str,
    ):
        """Setter for the engine_url instance variable. Resets connection

        Args:
            value (str): the new engine_url string
        """
        raise atscale_errors.UnsupportedOperationException(
            "The value of engine_url is final; it cannot be altered."
        )

    @property
    def organization(self) -> str:
        """Getter for the organization instance variable

        Returns:
            str: the organization string
        """
        return self._organization

    @organization.setter
    def organization(
        self,
        value: str,
    ):
        """Setter for the organization instance variable. Resets connection if value is None

        Args:
            value (str): the new organization string. Resets connection if None
        """
        if value is None:
            # Then they will have to (re)connect to select one.
            # I figure "no connection" errors will be easier to
            # understand than those from passing in None for org
            self.__set_token(None)
        # I don't force a reconnect otherwise. The REST API will
        # respond with errors if the user associated with token
        # Doesn't have access to the set organization.
        self._organization = value
        self._set_jdbc_string()

    @property
    def username(self) -> str:
        """Getter for the username instance variable

        Returns:
            str: the username string
        """
        return self._username

    @username.setter
    def username(
        self,
        value: str,
    ):
        """The setter for the username instance variable. Resets connection

        Args:
            value (str): the new username string
        """
        inspection = getfullargspec(self.username)
        validation_utils.validate_by_type_hints(inspection=inspection, func_params=locals())

        if value is None:
            raise ValueError("Username cannot be null.")
        # set token to none to require (re)connect
        self.__set_token(None)
        self._username = value

    @property
    def password(self) -> str:
        """The getter for the password instance variable"""
        raise atscale_errors.UnsupportedOperationException(
            "Passwords are secure and cannot be retrieved."
        )

    @password.setter
    def password(
        self,
        value: str,
    ):
        """The setter for the password instance variable. Resets connection

        Args:
            value (str): the new password to try
        """
        inspection = getfullargspec(self.password)
        validation_utils.validate_by_type_hints(inspection=inspection, func_params=locals())

        if value is None:
            raise ValueError("Password cannot be null.")
        # set token to none to require (re)connect
        self.__set_token(None)
        self._password = self.__fernet.encrypt(value.encode())

    def __set_token(
        self,
        value,
    ):
        """Private method as a convenience for maintaining headers when the token is changed.
        See https://docs.python.org/3/tutorial/classes.html#private-variables
        Args:
            value (str): the new token value
        """
        self.__token = value

    def _set_jdbc_string(self):
        if not self.__token:
            self._auth()

        server = self.design_center_url.split("//")[1].split(":")[0]
        response = self._submit_request(
            request_type=private_enums.RequestType.GET, url=endpoints._endpoint_jdbc_port(self)
        )
        jdbc_port = json.loads(response.content)["response"]["hiveServer2Port"]
        self.jdbc_string = f"jdbc:hive2://{server}:{jdbc_port}/;AuthMech=3"

    def _set_engine_url(self):
        if not self.__token:
            self._auth()
        #    The following hits an endpoint that requires the "Administer Organization" permission
        #    so we can't use that right now
        #    response = self._submit_request(
        #    request_type=private_enums.RequestType.GET, url=endpoints._endpoint_engine_settings(self))
        #    engine_settings = json.loads(response.content)["response"]["engine"]
        #    engine_protocol = engine_settings["protocol"]
        #    engine_host = engine_settings["host"]
        #    engine_port = engine_settings["port"]
        #    self._engine_url = f"{engine_protocol}://{engine_host}:{engine_port}"
        resp = self._submit_request(
            request_type=private_enums.RequestType.GET, url=endpoints._endpoint_project_folder(self)
        )
        match = re.search("""window\\.loadBalancerUrls = ({.*?});""", str(resp.content))
        if match:
            match = match[1]
            match = unescape(match).encode("utf-8").decode("unicode_escape")
            urls = json.loads(match)
            self._engine_url = urls.get("mdxUrl")
        elif re.search("<title>Login", str(resp.content)):
            raise atscale_errors.AuthenticationError(
                "Unable to determine engine url. Your token may be expired or authentication was incorrect. Please verify information and reconnect."
            )
        else:
            raise atscale_errors.AtScaleServerError(
                "Unable to determine engine url. Please verify connection information and reconnect."
            )

    def _get_postgres_conn(self, data_model):
        conn = psycopg2.connect(
            host=self.design_center_url.split("//")[1].split(":")[0],
            database=data_model.project.project_name,
            user=self._username,
            password=self.__fernet.decrypt(self._password).decode(),
            port=15432,
        )
        return conn

    def _submit_request(
        self,
        request_type: private_enums.RequestType,
        url: str,
        content_type: str = "json",
        data: str = "",
        raises: bool = False,
    ):
        headers = request_utils.generate_headers(content_type, self.__token)
        if request_type == private_enums.RequestType.GET:
            response = request_utils.get_rest_request(
                url, data, headers, raises, session=self.session
            )
        elif request_type == private_enums.RequestType.PATCH:
            response = request_utils.patch_rest_request(
                url, data, headers, raises, session=self.session
            )
        elif request_type == private_enums.RequestType.POST:
            response = request_utils.post_rest_request(
                url, data, headers, raises, session=self.session
            )
        elif request_type == private_enums.RequestType.PUT:
            response = request_utils.put_rest_request(
                url, data, headers, raises, session=self.session
            )
        elif request_type == private_enums.RequestType.DELETE:
            response = request_utils.delete_rest_request(
                url, data, headers, raises, session=self.session
            )
        else:
            raise ValueError("Invalid request type.")
        # If we get a 401 re-auth and try again else just do the normal check response flow
        if response.status_code == 401 or response.status_code == 403:
            logger.info("Token expired reauthorizing")
            self._auth()
            return self._submit_request(request_type, url, content_type, data, raises=True)
        if not response.ok and json.loads(response.text).get("response", {}).get(
            "error", ""
        ).endswith("i/o timeout"):
            logger.info("I/O internal server error, retrying")
            return self._submit_request(request_type, url, content_type, data, raises=True)
        if not raises:
            request_utils.check_response(response)
        return response

    def _connect(
        self,
        organization: str = None,
    ):
        """Connects to AtScale server using class variables necessary for authentication (which can be set directly, provided in constructor,
        or passed as a parameter here). Validates the license, stores the api token, and sets the organization.
        May ask for user input.

        Args:
            organization (str, optional): The organization to connect to. Defaults to None.
        """
        # if not self.password:
        #     self.password = getpass.getpass(prompt=f'Please enter your AtScale password for user \'{self.username}\': ')
        self.__token = None
        if organization is not None:
            self.organization = organization

        if self.organization is None:
            # This can still assign none to the org, in which case token will be
            # set to None in the setter for organization, and therefore this method
            # will exit but stil no token, connected() returns false. I figured those
            # errors will be easier to understand than those from passing None for org to urls
            self._select_org_pre_auth()
        if not self.__token:
            self._auth()
        self._validate_license()
        if not self.jdbc_string:
            self._set_jdbc_string()

    def _get_user_id_from_session(self):
        response = self._submit_request(
            request_type=private_enums.RequestType.GET, url=endpoints._endpoint_session(self)
        )
        resp = json.loads(response.content)["response"]
        return resp["user_id"]

    def _get_username(self):
        response = self._submit_request(
            request_type=private_enums.RequestType.GET, url=endpoints._endpoint_user_account(self)
        )
        resp = json.loads(response.content)["response"]
        return resp["username"]

    def _auth(self):
        if self._org_basic_auth_disabled() and self.username != "admin":
            print(
                f"""Basic auth is disabled for this organization. Please log in at: {endpoints._endpoint_login_screen(self)}"""
            )
            print(f"""Then go to: {endpoints._endpoint_jwt(self)} to retrieve a token.""")
            token = getpass.getpass(prompt=f"Token:")
            if not token:
                raise ValueError("No token supplied")
            self.__set_token(token)
            password = self.__get_user_token()
        else:
            # https://documentation.atscale.com/2022.1.0/api/authentication
            header = request_utils.generate_headers()
            url = endpoints._endpoint_auth_bearer(self)
            if not self.username:
                username = input_utils.get_string_input(msg=f"Please enter your AtScale username: ")
            else:
                username = self._username

            if self._password:
                password = self.__fernet.decrypt(self._password).decode()
            else:
                password = getpass.getpass(
                    prompt=f"Please enter your AtScale password for user '{username}': "
                )

            response = self.session.get(
                url,
                headers=header,
                auth=requests.auth.HTTPBasicAuth(self.username, password),
                stream=False,
            )
            if response.ok:
                self.__set_token(response.content.decode())
            elif response.status_code == 401:
                self._password = None
                raise atscale_errors.AuthenticationError(response.text)
            else:
                self._password = None
                resp = json.loads(response.text)
                # this makes sense as we don't know what kind of error it is
                raise Exception(resp["response"]["error"])
        # if we get here it worked so persist the fields we want to keep
        self._user_id = self._get_user_id_from_session()
        # we might want to pull the username from the server because auth is case insensitive which can cause problemns later
        # self._username = self._get_username()
        self._password = self.__fernet.encrypt(password.encode())

    def _validate_license(
        self,
        specific_feature_flag=None,
    ) -> bool:
        """Validates that the AtScale server has the necessary flags in its license.

        Args:
            specific_feature_flag (str, optional): The specific feature flag to validate. Defaults to None to check all flags necessary for AI-Link.
        """
        response = self._submit_request(
            request_type=private_enums.RequestType.GET, url=endpoints._endpoint_engine_version(self)
        )
        engine_version_string = response.text
        engine_version = float(
            engine_version_string.split(".")[0] + "." + engine_version_string.split(".")[1]
        )
        response = self._submit_request(
            request_type=private_enums.RequestType.GET,
            url=endpoints._endpoint_license_details(self),
        )
        resp = json.loads(response.text)
        if not specific_feature_flag:
            if (
                "query_rest" not in resp["response"]["content"]["features"]
                or resp["response"]["content"]["features"]["query_rest"] is False
            ):
                logger.warning(
                    "Query REST Endpoint not licensed for your server. You will be unable to query through AI-Link"
                )
            if engine_version >= 2022.2:
                if (
                    "data_catalog_api" not in resp["response"]["content"]["features"]
                    or resp["response"]["content"]["features"]["data_catalog_api"] is False
                ):
                    logger.warning(
                        "Data Catalog not licensed for your server. You may have issues pulling metadata"
                    )
            if (
                "ai-link" not in resp["response"]["content"]["features"]
                or resp["response"]["content"]["features"]["ai-link"] is False
            ):
                self.__set_token(None)
                raise atscale_errors.InaccessibleAPIError(
                    "AI-Link is not licensed for your AtScale server."
                )
            return True
        else:
            if (
                specific_feature_flag not in resp["response"]["content"]["features"]
                or resp["response"]["content"]["features"][specific_feature_flag] is False
            ):
                return False
            else:
                return True

    def _connected(self) -> bool:
        """Convenience method to determine if this object has connected to the server and authenticated.
        This is determined based on whether a token has been stored locally after a connection with the
        server.

        Returns:
            bool: whether this object has connected to the server and authenticated.
        """
        if self.__token is not None:
            return True
        else:
            return False

    def _get_orgs(self) -> List[Dict]:
        """Get a list of metadata for all organizations available to the connection.

        Returns:
            List(Dict): a list of dictionaries providing metadata per organization
        """
        self._check_connected()

        # The current API docs are a bit off in the response descriptions so leaving out of docstring
        # https://documentation.atscale.com/2022.1.0/api-ref/organizations
        # url = f'{self.server}:{self.design_center_server_port}/api/1.0/org'
        # submit request, check for errors which will raise exceptions if there are any
        # response = self._submit_request(request_type=private_enums.RequestType.GET, url=url)
        # if we get down here, no exceptions raised, so parse response
        # return json.loads(response.content)['response']

        # Due to engien bug requiring sysadmin for above endpoint we need to use the below function.
        # This is a workaround and should be removed when the endpoint is fixed
        return self._get_orgs_for_all_users()

    def _get_orgs_for_all_users(self):
        url = endpoints._endpoint_login_screen(self)
        resp = self._submit_request(request_type=private_enums.RequestType.GET, url=url)
        match = re.search("window\\.organizations = (.*?]);", str(resp.content))
        match = match[1]
        match = unescape(match).encode("utf-8").decode("unicode_escape")
        org_list = json.loads(match)
        return org_list

    def _select_org(self):
        """Uses an established connection to enable the user to select from the orgs they have access to.
        This is different from setting the organization directly, for which there is a property and associated
        setter.
        """
        orgs = self._get_orgs()

        org = input_utils.choose_id_and_name_from_dict_list(orgs, "Please choose an organization:")
        if org is not None:
            self.organization = org["id"]

    def _select_org_pre_auth(self):
        """Same as select_org but will list all organizations regardless of user access"""
        orgs = self._get_orgs_for_all_users()
        org = input_utils.choose_id_and_name_from_dict_list(
            dcts=orgs, prompt="Please choose an organization:"
        )
        if org is not None:
            self.organization = org["id"]
        else:
            raise atscale_errors.WorkFlowError(
                "An organization must be selected before authentication occurs."
            )

    def _get_connection_groups(self) -> list:
        u = endpoints._endpoint_connection_groups(self)
        # this call will handle or raise any errors
        tmp = self._submit_request(request_type=private_enums.RequestType.GET, url=u)
        # bunch of parsing I'm just going to wrap in a try and if any of it fails I'll log and raise
        content = json.loads(tmp.content)
        if content["response"]["results"].get("count", 0) < 1:
            raise atscale_errors.AtScaleServerError(
                "No connection groups found. Make "
                "sure there is a warehouse connection in the AtScale UI"
            )
        return content["response"]["results"]["values"]

    def _get_published_projects(self):
        url = endpoints._endpoint_published_project_list(self)
        # submit request, check for errors which will raise exceptions if there are any
        response = self._submit_request(request_type=private_enums.RequestType.GET, url=url)
        # if we get down here, no exceptions raised, so parse response
        return json.loads(response.content)["response"]

    def _get_projects(self):
        """See https://documentation.atscale.com/2022.1.0/api-ref/projects#projects-list-all
        Grabs projects using organization information this object was initialized with. I believe this
        will only return draft projects since it indicates full json is returned and that doesn't
        happen with published projects.

        Returns:
            Dict: full json spec of any projects
        """
        # construct the request url
        url = endpoints._endpoint_list_projects(self)
        # submit request, check for errors which will raise exceptions if there are any
        response = self._submit_request(request_type=private_enums.RequestType.GET, url=url)
        # if we get down here, no exceptions raised, so parse response
        resp = json.loads(response.content)["response"]
        return resp

    def _get_draft_project_dict(
        self,
        draft_project_id: str,
    ) -> Dict:
        """Get the draft project json and convert to a dict.

        Args:
            draft_project_id (str): The id for the draft project (i.e. not published project) to be retrieved.

        Returns:
            Dict: the dict representation of the draft project, or None if no project exists for the provided draft_project_id
        """
        # construct the request url
        url = endpoints._endpoint_design_draft_project(self, draft_project_id)
        response = self._submit_request(request_type=private_enums.RequestType.GET, url=url)
        return json.loads(response.content)["response"]

    # hitting endpoints

    def _post_atscale_query(
        self,
        query,
        project_name,
        use_aggs=True,
        gen_aggs=False,
        fake_results=False,
        use_local_cache=True,
        use_aggregate_cache=True,
        timeout=10,
    ):
        """Submits an AtScale SQL query to the AtScale server and returns the http requests.response object.

        :param str query: The query to submit.
        :param bool use_aggs: Whether to allow the query to use aggs. Defaults to True.
        :param bool gen_aggs: Whether to allow the query to generate aggs. Defaults to False.
        :param bool fake_results: Whether to use fake results. Defaults to False.
        :param bool use_local_cache: Whether to allow the query to use the local cache. Defaults to True.
        :param bool use_aggregate_cache: Whether to allow the query to use the aggregate cache. Defaults to True.
        :param int timeout: The number of minutes to wait for a response before timing out. Defaults to 10.
        :return: A response with a status code, text, and content fields.
        :rtype: requests.response
        """
        json_data = json.dumps(
            templates.create_query_for_post_request(
                query=query,
                project_name=project_name,
                organization=self.organization,
                use_aggs=use_aggs,
                gen_aggs=gen_aggs,
                fake_results=fake_results,
                use_local_cache=use_local_cache,
                use_aggregate_cache=use_aggregate_cache,
                timeout=timeout,
            )
        )
        attempts = 10
        done = False
        while attempts > 0 and done == False:
            response = self._submit_request(
                request_type=private_enums.RequestType.POST,
                url=endpoints._endpoint_atscale_query_submit(self),
                data=json_data,
            )
            data = json.loads(response.text)
            if data["metadata"]["succeeded"] == False and (
                "Error during query planning: no such vertex in graph"
                in data["metadata"]["error-message"]
                or "Error during query planning: key not found: AnonymousKey("
                in data["metadata"]["error-message"]
                or "Error during query planning: In query planning stage EvaluateCalculations: Flat attribute"
                in data["metadata"]["error-message"]
            ):
                time.sleep(1)
                attempts = attempts - 1
            else:
                done = True
        return response

    def _get_jdbc_connection(self):
        """Returns a jaydebeapi connection to the data model

        Returns:
            _Connection: The jaydebeapi connection
        """
        try:
            import jaydebeapi
        except ImportError as e:
            raise atscale_errors.AtScaleExtrasDependencyImportError("jdbc", str(e))

        if self.jdbc_driver_path == "":
            raise atscale_errors.WorkFlowError(
                "Cannot create jdbc connection because jdbc_driver_path is not set on the Client"
            )
        return jaydebeapi.connect(
            self.jdbc_driver_class,
            self.jdbc_string,
            [self.username, self.__fernet.decrypt(self._password).decode()],
            self.jdbc_driver_path,
        )

    def _get_connected_warehouses(self) -> List[Dict]:
        """Returns metadata on all warehouses visible to the connection

        Returns:
            List[Dict]: The list of available warehouses
        """
        self._check_connected()

        connectionGroups = self._get_connection_groups()

        output_list = []
        result_keys = ["name", "platformType", "connectionId"]
        result_key_map = {
            "name": "name",
            "platformType": "platform",
            "connectionId": "warehouse_id",
        }

        for warehouse in connectionGroups:
            output_list.append(
                {result_key_map[res_key]: warehouse[res_key] for res_key in result_keys}
            )
        return output_list

    def _get_warehouse_platform(
        self,
        warehouse_id: str,
    ) -> private_enums.PlatformType:
        self._check_connected()
        warehouses = self._get_connected_warehouses()
        warehouse = [w for w in warehouses if w["warehouse_id"] == warehouse_id]  # single item list
        if len(warehouse) == 0:
            raise atscale_errors.ModelingError(
                f"No warehouse exists in the connection with the warehouse_id '{warehouse_id}'. "
                f"The following warehouses are present: {warehouses}"
            )
        warehouse = warehouse[
            0
        ]  # warehouse ids are unique so we should have gotten a list of length 1
        platform = warehouse["platform"]
        return private_enums.PlatformType(platform)

    def _get_connected_databases(
        self,
        warehouse_id: str,
    ) -> List[str]:
        """Get a list of databases the organization can access in the provided warehouse.

        Args:
            warehouse_id (str): The AtScale warehouse connection to use.

        Returns:
            List[str]: The list of available databases
        """

        self._check_connected()

        u = endpoints._endpoint_warehouse_tables_cacheRefresh(self, warehouse_id)
        response = self._submit_request(request_type=private_enums.RequestType.POST, url=u, data="")

        u = endpoints._endpoint_warehouse_databases(self, warehouse_id)
        response = self._submit_request(request_type=private_enums.RequestType.GET, url=u)
        return json.loads(response.content)["response"]

    def _get_connected_schemas(
        self,
        warehouse_id: str,
        database: str,
    ) -> List[str]:
        """Get a list of schemas the organization can access in the provided warehouse and database.

        Args:
            warehouse_id (str): The AtScale warehouse connection to use.
            database (str): The database to use.

        Returns:
            List[str]: The list of available tables
        """

        self._check_connected()

        u = endpoints._endpoint_warehouse_tables_cacheRefresh(self, warehouse_id)
        response = self._submit_request(request_type=private_enums.RequestType.POST, url=u, data="")

        u = endpoints._endpoint_warehouse_all_schemas(self, warehouse_id, database)
        response = self._submit_request(request_type=private_enums.RequestType.GET, url=u)
        return json.loads(response.content)["response"]

    def _get_connected_tables(
        self,
        warehouse_id: str,
        database: str,
        schema: str,
    ) -> List[str]:
        """Get a list of tables the organization can access in the provided warehouse, database, and schema.

        Args:
            warehouse_id (str): The AtScale warehouse connection to use.
            database (str): The database to use.
            schema (str): The schema to use.

        Returns:
            List[str]: The list of available tables
        """

        self._check_connected()

        u = endpoints._endpoint_warehouse_tables_cacheRefresh(self, warehouse_id)
        response = self._submit_request(request_type=private_enums.RequestType.POST, url=u, data="")

        u = endpoints._endpoint_warehouse_all_tables(
            self,
            warehouse_id=warehouse_id,
            schema=schema,
            database=database,
        )
        response = self._submit_request(request_type=private_enums.RequestType.GET, url=u)
        return json.loads(response.content)["response"]

    def _get_query_columns(
        self,
        warehouse_id: str,
        query: str,
    ):
        """Get all columns of a direct query, to the given warehouse_id, as they are represented by AtScale.

        Args:
            warehouse_id (str): The AtScale warehouse to use.
            query (str): A valid query for the warehouse of the given id, of which to return the resulting columns

        Returns:
            List[Tuple]: A list of columns represented as Tuples of (name, data-type)
        """
        self._check_connected()

        # cache refresh
        u = endpoints._endpoint_warehouse_tables_cacheRefresh(self, warehouse_id)
        self._submit_request(request_type=private_enums.RequestType.POST, url=u)

        # preview query
        url = endpoints._endpoint_warehouse_query_info(self, warehouse_id)
        payload = {"query": query}
        response = self._submit_request(
            request_type=private_enums.RequestType.POST, url=url, data=json.dumps(payload)
        )
        # parse response into tuples of name and data-type
        columns = [
            (x["name"], x["column-type"]["data-type"])
            for x in json.loads(response.content)["response"]["columns"]
        ]
        return columns

    def _get_table_columns(
        self,
        warehouse_id: str,
        table_name: str,
        database: str = None,
        schema: str = None,
        expected_columns: List[str] = None,
    ) -> List[Tuple]:
        """Get all columns in a given table

        Args:
            warehouse_id (str): The AtScale warehouse to use.
            table_name (str): The name of the table to use.
            database (str, optional): The database to use. Defaults to None to use default database
            schema (str, optional): The schema to use. Defaults to None to use default schema
            expected_columns (List[str], optional): A list of expected column names to validate. Defaults to None

        Returns:
            List[Tuple]: Pairs of the columns and data-types (respectively) of the passed table
        """
        self._check_connected()

        u = endpoints._endpoint_warehouse_tables_cacheRefresh(self, warehouse_id)
        self._submit_request(request_type=private_enums.RequestType.POST, url=u, data="")

        url = endpoints._endpoint_warehouse_single_table_info(
            self,
            warehouse_id=warehouse_id,
            table=table_name,
            schema=schema,
            database=database,
        )
        response = self._submit_request(request_type=private_enums.RequestType.GET, url=url)
        table_columns = [
            (x["name"], x["column-type"]["data-type"])
            for x in json.loads(response.content)["response"]["columns"]
        ]
        table_column_names = [x[0] for x in table_columns]
        if expected_columns is not None:
            for column in expected_columns:
                if column in table_column_names:
                    continue
                elif column.upper() in table_column_names:
                    logger.warning(f"Column name: {column} appears as {column.upper()}")
                elif column.lower() in table_column_names:
                    logger.warning(f"Column name: {column} appears as {column.lower()}")
                else:
                    logger.warning(f"Column name: {column} does not appear in table {table_name}")
        return table_columns

    def _unpublish_project(
        self,
        published_project_id: str,
    ) -> bool:
        """Internal function to unpublishes the provided published_project_id making in no longer queryable

        Args:
            published_project_id (str): the id of the published project to unpublish

        Returns:
            bool: Whether the unpublish was successful
        """
        u = endpoints._endpoint_draft_project_unpublish(self, published_project_id)
        response = self._submit_request(request_type=private_enums.RequestType.DELETE, url=u)
        if response.status_code == 200:
            return True
        else:
            logger.error(json.loads(response.content)["response"]["status"]["message"])
            return False

    def _check_connected(
        self,
        err_msg=None,
    ):
        outbound_error = "No connection established to AtScale, please establish a connection by calling Client.connect()."
        if err_msg:
            outbound_error = err_msg
        if not self._connected():
            raise atscale_errors.AuthenticationError(outbound_error)

    def _org_basic_auth_disabled(self) -> bool:
        """Internal function to check if basic authentication is disabled for the current org
           due to OAuth or SAML so we account for it in the auth process

        Returns:
            bool: Whether basic authentication is disabled.
        """
        response = self._submit_request(
            request_type=private_enums.RequestType.GET, url=endpoints._endpoint_login_screen(self)
        )

        match = re.search("window\\.organizations = (.*?]);", str(response.content))
        match = match[1]
        match = unescape(match).encode("utf-8").decode("unicode_escape")
        org_list = json.loads(match)

        for org in org_list:
            if org.get("id") == self.organization:
                if org.get("OAuth", "") != "" or org.get("SAML", {}.get("enabled", False)) == True:
                    return True
                else:
                    return False
        raise atscale_errors.ObjectNotFoundError(
            f"Unable to find organization: {self.organization}"
        )

    def __get_user_token(self):
        try:
            response = self._submit_request(
                request_type=private_enums.RequestType.GET,
                url=endpoints._endpoint_user_account(self),
            )
            token = json.loads(response.content).get("response", {}).get("secret_token")
            if token:
                return token
            else:
                raise
        except:
            raise atscale_errors.AtScaleServerError(
                f"Unable to retrive authorization token, which is required for jdbc queries, "
                f"for user: {self.username}  please ensure the username was entered correctly "
                f"and an authorization token is available in your profile page."
            )
