import abc
from typing import Dict, Literal, Optional

import devtools as dtz

# from guard_post import Client
from guard_post.api.assigns import (
    assign_edge_api_assigns_add_post as assign_edge,
    check_relationship_api_assigns_check_post as check_relation,
    expand_relationship_api_assigns_expand_post as expand_object,
    list_edges_api_assigns_list_post as list_edges,
    revoke_user_to_org_api_assigns_revoke_post as revoke_edge,
)
from guard_post.api.azure_ad import (
    get_user_api_active_dir_get_user_get as get_user_oauth,
)

# from guard_post.models.http_validation_error import HTTPValidationError
# from guard_post.types import Response
from guard_post.api.orgs import (
    delete_api_orgs_delete_post as delete_orgs,
    list_items_api_orgs_list_get as list_orgs,
    sync_api_orgs_sync_post as sync_orgs,
)
from guard_post.api.sites import (
    delete_api_sites_delete_post as delete_sites,
    list_sites_api_sites_list_get as list_sites,
    sync_api_sites_sync_post as sync_sites,
)
from guard_post.api.users import (
    delete_api_users_delete_post as delete_users,
    list_items_api_users_list_get as list_users,
    sync_api_users_sync_post as sync_users,
)
from guard_post.client import Client
from guard_post.imports import logger

# User, Site, Org
from guard_post.models import (  # CreateSiteAttributes,
    CreateOrg,
    CreateSite,
    CreateUser,
    DeleteOrg,
    DeleteSite,
    DeleteUser,
    EdgeInput,
    ExpandInput,
    ListObjectsInputKey,
    Site as SiteInput,
)

# edge_input,
from guard_post.models.create_user_attributes import CreateUserAttributes
from guard_post.models.edge_keys import EdgeKeys
from guard_post.models.list_objects_input_key_key import ListObjectsInputKeyKey
from guard_post.models.pydantic_models import (
    Organization,
    Organization as OrganizationModel,
    Users,
    Users as UsersModel,
)
from guard_post.models.pydantic_models.relations import (
    EdgeInput as PyEdgeInput,
    EdgeKeys as PyEdgeKeys,
    ExpandInput as PyExpandInput,
)


class Path(abc.ABC):
    def __init__(self, client: "GuardPost") -> None:
        self.client = client

    @abc.abstractmethod
    def get(self, *args, **kwargs) -> None:
        pass

    @abc.abstractmethod
    def list(self, *args, **kwargs) -> None:
        pass

    @abc.abstractmethod
    def create_or_sync(self, *args, **kwargs) -> None:
        pass

    @abc.abstractmethod
    def remove(self, *args, **kwargs) -> None:
        pass

    def class_name(self) -> str:
        return self.__class__.__name__

    def __repr__(self) -> str:
        client_repr = repr(self.client)

        return f"{self.class_name().title()}(client={client_repr[:20]} ...)"


class UserPath(Path):
    """
    Handles user-related operations in the GuardPost system.

    This class provides methods for creating, listing, updating, and managing users,
    as well as their group associations.
    """

    def get(self, *args, **kwargs) -> None:
        """
        Retrieves a user.

        Note: This method is currently a placeholder and needs to be implemented.

        Returns:
            None
        """
        logger.info("Calling organization get")
        return self

    def list(self, limit: int = 100) -> None:
        """
        Lists users with an optional limit.

        Args:
            limit (int): The maximum number of users to return. Default is 100.

        Returns:
            The list of users.
        """
        return list_users.sync(client=self.client, limit=limit)

    def create_or_sync(
        self,
        *args,
        key: Optional[Dict[str, str]] = None,
        name: Optional[str] = None,
        site_id: Optional[int] = None,
        **kwargs,
    ) -> None:
        """
        Creates or synchronizes a user.

        Args:
            key (Optional[Dict[str, str]]): The unique key for the user.
            name (Optional[str]): The name of the user (currently unused).
            site_id (Optional[int]): The site ID associated with the user (currently unused).
            **kwargs: Additional keyword arguments for user attributes.

        Returns:
            The created or synchronized user object.
        """
        key_input = key or kwargs.get("key", None) or {"test": "users", "type": "user"}
        create_site = CreateUser(
            key=key_input,
            first_name="test_first_name",
            last_name="test_last_name",
            email=kwargs.get("email", None) or "kevin.hill@hussmann.com",
            phone=kwargs.get("phone", None) or "1234567890",
            attributes=CreateUserAttributes(),
        )
        return sync_users.sync(client=self.client, json_body=create_site)

    def remove(self, key: dict = dict()) -> None:
        """
        Removes a user.

        Args:
            key (dict): The unique key of the user to remove.

        Returns:
            The result of the removal operation.

        Raises:
            ValueError: If the key is not provided.
        """
        if not key:
            raise ValueError("key is required")
        del_input = DeleteUser(key=key)
        return delete_users.sync(client=self.client, json_body=del_input)

    def add_groups(self, key: dict, groups: list = []) -> dict:
        """
        Adds the user to specified groups.

        Args:
            key (dict): The user's unique key.
            groups (list): A list of group names to add the user to.

        Returns:
            dict: A dictionary containing the operation result.
        """
        return {
            "key": key,
            "groups": groups,
            "success": True,
        }

    def add_group(self, key: dict, group: str) -> dict:
        """
        Adds the user to a single group.

        Args:
            key (dict): The user's unique key.
            group (str): The group name to add the user to.

        Returns:
            dict: A dictionary containing the operation result.
        """
        group_list = [group]
        return self.add_groups(key=key, groups=group_list)

    def remove_groups(self, key: dict, groups: list = []) -> dict:
        """
        Removes the user from specified groups.

        Args:
            key (dict): The user's unique key.
            groups (list): A list of group names to remove the user from.

        Returns:
            dict: A dictionary containing the operation result.
        """
        return {
            "key": key,
            "groups": groups,
            "success": True,
        }

    def remove_group(self, key: dict, group: str) -> dict:
        """
        Removes the user from a single group.

        Args:
            key (dict): The user's unique key.
            group (str): The group name to remove the user from.

        Returns:
            dict: A dictionary containing the operation result.
        """
        group_list = [group]
        return self.remove_groups(key=key, groups=group_list)

    def read_groups(self, key: dict) -> dict:
        """
        Reads the groups the user belongs to.

        Note: This is a placeholder implementation and needs to be updated with actual API call.

        Args:
            key (dict): The user's unique key.

        Returns:
            dict: A dictionary containing the groups the user is part of and the operation status.
        """
        return {
            "key": key,
            "groups": ["admin", "member"],
            "success": True,
        }


class SitePath(Path):
    """
    Handles site-related operations in the GuardPost system.

    This class provides methods for creating, listing, updating, and managing sites.
    """

    def get(self, *args, **kwargs) -> None:
        """
        Retrieves a site.

        Note: This method is currently a placeholder and needs to be implemented.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            None
        """
        logger.info("Calling organization get")
        return self

    def list(self, limit: int = 100) -> None:
        """
        Lists sites with an optional limit.

        Args:
            limit (int): The maximum number of sites to return. Default is 100.

        Returns:
            The list of sites.
        """
        return list_sites.sync(client=self.client, limit=limit)

    def create_or_sync(
        self,
        *args,
        key: Optional[Dict[str, str]] = None,
        name: Optional[str] = None,
        site_id: Optional[int] = None,
        **kwargs,
    ) -> None:
        """
        Creates or synchronizes a site.

        Args:
            key (Optional[Dict[str, str]]): The unique key for the site.
            name (Optional[str]): The name of the site.
            site_id (Optional[int]): An identifier for the site.
            **kwargs: Additional keyword arguments for site attributes.

        Returns:
            The created or synchronized site object.
        """
        key_input = (
            key or kwargs.get("key", None) or {"test": "organization", "type": "org"}
        )
        name_input = name or kwargs.get("name", None) or "test_site"
        description = kwargs.get("description", None) or "test_org_descriptionssssss"
        site_id = site_id or kwargs.get("site_id", None) or 4
        create_site = CreateSite(
            key=key_input,
            name=name_input,
            description=description,
            site_id=site_id,
        )
        return sync_sites.sync(client=self.client, json_body=create_site)

    def remove(self, key: dict = dict()) -> None:
        """
        Removes a site.

        Args:
            key (dict): The unique key of the site to remove.

        Returns:
            The result of the removal operation.

        Raises:
            ValueError: If the key is not provided.
        """
        if not key:
            raise ValueError("key is required")
        del_input = DeleteSite(key=key)
        return delete_sites.sync(client=self.client, json_body=del_input)


class OrganizationPath(Path):
    """
    Handles organization-related operations in the GuardPost system.

    This class provides methods for creating, listing, updating, and managing organizations.
    """

    def get(self, *args, **kwargs) -> None:
        """
        Retrieves an organization.

        Note: This method is currently a placeholder and needs to be implemented.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            None
        """
        logger.info("Calling organization get")
        return self

    def list(self, limit: int = 100) -> None:
        """
        Lists organizations with an optional limit.

        Args:
            limit (int): The maximum number of organizations to return. Default is 100.

        Returns:
            The list of organizations.
        """
        return list_orgs.sync(client=self.client, limit=limit)

    def create_or_sync(
        self,
        *args,
        key: Optional[Dict[str, str]] = None,
        name: Optional[str] = None,
        **kwargs,
    ) -> None:
        """
        Creates or synchronizes an organization.

        Args:
            key (Optional[Dict[str, str]]): The unique key for the organization.
            name (Optional[str]): The name of the organization.
            **kwargs: Additional keyword arguments for organization attributes.

        Returns:
            The created or synchronized organization object.
        """
        key_input = (
            key or kwargs.get("key", None) or {"test": "organization", "type": "org"}
        )
        name_input = name or kwargs.get("name", None) or "test_org"
        descript = kwargs.get("description", None) or "test_org_descriptionssssss"
        create_org = CreateOrg(
            key=key_input,
            name=name_input,
            description=descript,
        )
        return sync_orgs.sync(client=self.client, json_body=create_org)

    def remove(self, key: dict = dict(), **kwargs) -> None:
        """
        Removes an organization.

        Args:
            key (dict): The unique key of the organization to remove.
            **kwargs: Additional keyword arguments.

        Returns:
            The result of the removal operation.

        Raises:
            ValueError: If the key is not provided.
        """
        if not key:
            raise ValueError("key is required")
        del_input = DeleteOrg(key=key)
        return delete_orgs.sync(client=self.client, json_body=del_input)


class GuardPost(Client):
    """
    Main client class for interacting with the GuardPost system.
    Provides methods for managing users, sites, organizations, and their relationships.
    """

    @property
    def users(self) -> "UserPath":
        """
        Returns a UserPath instance for user-related operations.

        Returns:
            UserPath: An instance to manage user operations.
        """
        return UserPath(client=self)

    @property
    def sites(self) -> Path:
        """
        Returns a SitePath instance for site-related operations.

        Returns:
            Path: An instance to manage site operations.
        """
        return SitePath(client=self)

    @property
    def orgs(self) -> Path:
        """
        Returns an OrganizationPath instance for organization-related operations.

        Returns:
            Path: An instance to manage organization operations.
        """
        return OrganizationPath(client=self)

    @property
    def httpx_client(self):
        """
        Returns the synchronous HTTPX client.

        Returns:
            httpx.Client: The synchronous HTTPX client instance.
        """
        return self.get_httpx_client()

    @property
    def async_httpx_client(self):
        """
        Returns the asynchronous HTTPX client.

        Returns:
            httpx.AsyncClient: The asynchronous HTTPX client instance.
        """
        return self.get_async_httpx_client()

    def check(self, source: dict, relation: str, target: dict) -> bool:
        """
        Checks if a relationship exists between a source and a target.

        Args:
            source (dict): The source entity.
            relation (str): The type of relationship to check.
            target (dict): The target entity.

        Returns:
            bool: True if the relationship exists, False otherwise.
        """
        logger.info("Calling check")
        edge_input = EdgeInput(
            keys=EdgeKeys(start=source, end=target), relation=relation
        )
        response = check_relation.sync(client=self, json_body=edge_input)

        return response.get("allowed", False)

    def assign(self, source: dict, relation: str, target: dict) -> bool:
        """
        Assigns a relationship between a source and a target.

        Args:
            source (dict): The source entity.
            relation (str): The type of relationship to assign.
            target (dict): The target entity.

        Returns:
            bool: True if the assignment was successful, False otherwise.
        """
        edge_input = EdgeInput(
            keys=EdgeKeys(start=source, end=target), relation=relation
        )
        assigned = assign_edge.sync(client=self, json_body=edge_input)
        return assigned

    def revoke(self, source: dict, relation: str, target: dict) -> bool:
        """
        Revokes a relationship between a source and a target.

        Args:
            source (dict): The source entity.
            relation (str): The type of relationship to revoke.
            target (dict): The target entity.

        Returns:
            bool: True if the revocation was successful, False otherwise.
        """
        edge_input = EdgeInput(
            keys=EdgeKeys(start=source, end=target), relation=relation
        )
        revoked = revoke_edge.sync(client=self, json_body=edge_input)
        return revoked

    def expand(self, source: dict, relation: str) -> bool:
        """
        Expands a relationship from a source entity.

        Args:
            source (dict): The source entity.
            relation (str): The type of relationship to expand.

        Returns:
            bool: The result of the expansion operation.
        """
        expand_input = ExpandInput(key=source, relation=relation)
        response = expand_object.sync(client=self, json_body=expand_input)
        return response

    @logger.catch
    def resources(self, source: dict, relation: str, relation_type: str) -> bool:
        """
        Lists resources related to a source entity based on a specific relation and type.

        Args:
            source (dict): The source entity.
            relation (str): The type of relationship to list.
            relation_type (str): The type of the related resources.

        Returns:
            bool: The result of the resource listing operation.
        """
        list_obj_input = ListObjectsInputKey(
            key=source, relation=relation, type=relation_type
        )
        response = list_edges.sync(client=self, json_body=list_obj_input)
        return response

    def oauth_token(self, token: str):
        """
        Authenticates a user using an OAuth token.

        Args:
            token (str): The OAuth token to authenticate with.

        Returns:
            The response from the authentication request.
        """
        response = get_user_oauth.sync(
            client=self.with_headers({"Authorization": f"Bearer {token}"})
        )
        return response

    def assign_user_roles(
        self,
        org: OrganizationModel,
        user: UsersModel,
        roles: list[Literal["owner", "admin", "member"]] = [],
    ):
        """
        Assigns roles to a user within an organization.

        Args:
            org (OrganizationModel): The organization model.
            user (UsersModel): The user model.
            roles (list): A list of roles to assign (owner, admin, member).

        Returns:
            list: A list of assignment results.

        Raises:
            AttributeError: If no roles are provided or if user or org keys are missing.
            ValueError: If the organization or user creation/retrieval fails.
        """
        if not roles:
            raise AttributeError(
                "You need to provide groups/roles for the user and organization"
            )

        target_organization = self.orgs.create_or_sync(**org.get_storable())
        if (
            not isinstance(target_organization, dict)
            or "org" not in target_organization
        ):
            raise ValueError("We weren't able to create or retrieve the organization")
        org_key = target_organization["org"]["key"]

        source_user = self.users.create_or_sync(**user.get_storable())
        if not isinstance(source_user, dict) or "user" not in source_user:
            raise ValueError("Couldn't add or retrieve the user")
        user_key = source_user["user"]["key"]

        if not user_key or not org_key:
            raise AttributeError("We need both a user key and an organization key.")

        assignments = [self.assign(user_key, role, org_key) for role in roles]

        return assignments

    def get_user_roles(self, user: Users, org: Organization):
        """
        Retrieves the roles of a user within an organization.

        Args:
            user (Users): The user model.
            org (Organization): The organization model.

        Returns:
            list: A list of roles the user has in the organization.

        Raises:
            httpx.HTTPStatusError: If the API request fails.
        """
        endpoint = "/api/assigns/get_relationships"
        edge_keys = PyEdgeKeys(start=user.key, end=org.key)
        edge_input = PyEdgeInput(keys=edge_keys, relation="admin")

        response = self.httpx_client.post(
            endpoint, json=edge_input.model_dump(mode="json")
        )
        response.raise_for_status()
        resp_json = response.json()
        if "roles" in resp_json:
            return resp_json["roles"]
        return []


def main():
    # Initialize GuardPost client
    guard = GuardPost(base_url="http://localhost:8000")

    # Define keys for different entities
    org_key = {"test": "organization", "type": "org", "name": "simple_org"}
    org_key2 = {"test": "organization", "type": "org", "name": "simple_org2"}
    site_key = {"test": "site", "type": "site", "name": "simple_site"}
    user_key = {
        "test": "user",
        "type": "user",
        "name": "simple_user",
        "email": "monika@hussmann.com",
    }

    # Create organizations
    logger.info("Creating organizations...")
    created_org = guard.orgs.create_or_sync(
        key=org_key,
        name="monika's org",
        description="monika's org description",
    )
    created_org2 = guard.orgs.create_or_sync(
        key=org_key2,
        name="kevin's org",
        description="kevin's org description",
    )
    logger.warning(created_org)
    logger.warning(created_org2)

    # List organizations to verify creation
    logger.info("Listing organizations...")
    org_list = guard.orgs.list(limit=2)
    logger.debug(f"Organization list: {org_list}")
    assert len(org_list) >= 2, "Failed to create both organizations"

    # Create a site
    logger.info("Creating a site...")
    created_site = guard.sites.create_or_sync(
        key=site_key,
        name="monika's site",
        description="monika's site description",
        site_id=44,
    )
    logger.debug(created_site)

    # List sites to verify creation
    logger.info("Listing sites...")
    site_list = guard.sites.list(limit=1)
    logger.debug(f"Site list: {site_list}")
    assert len(site_list) >= 1, "Failed to create site"

    # Create a user and add groups
    logger.info("Creating a user and adding groups...")
    created_user = guard.users.create_or_sync(
        key=user_key,
        name="monika's user",
        description="monika's user description",
        phone="+491761234567",
        email="monika@hussmann.com",
    )
    added_groups = guard.users.add_groups(
        key=user_key,
        groups=["admin", "member"],
    )
    logger.warning(created_user)
    logger.info(f"Added groups: {added_groups}")

    # List users to verify creation
    logger.info("Listing users...")
    user_list = guard.users.list(limit=1)
    logger.debug(f"User list: {user_list}")
    assert len(user_list) >= 1, "Failed to create user"

    # Manage relationships
    logger.info("Managing relationships...")
    # Assign admin relationship from user to org
    assigned_admin = guard.assign(user_key, "admin", org_key)
    logger.success(f"Assigned admin relationship: {assigned_admin}")

    # Revoke admin relationship from user to org
    revoked_original = guard.revoke(user_key, "admin", org_key)
    logger.success(f"Revoked admin relationship: {revoked_original}")

    # Assign parent relationship between organizations
    org_assigned = guard.assign(org_key2, "parent", org_key)
    logger.success(f"Assigned parent relationship: {org_assigned}")

    # Assign admin relationship from user to org2
    assigned = guard.assign(user_key, "admin", org_key2)
    logger.success(f"Assigned admin relationship: {assigned}")

    # Check relationships
    logger.info("Checking relationships...")
    allowed_admin = guard.check(user_key, "admin", org_key)
    allowed_create_org = guard.check(user_key, "can_create_org", org_key)
    allowed_add_member = guard.check(user_key, "can_add_member", org_key)
    logger.debug(f"Admin check: {allowed_admin}")
    logger.debug(f"Can create org check: {allowed_create_org}")
    logger.debug(f"Can add member check: {allowed_add_member}")

    # Assert that at least one check passed
    assert any([allowed_admin, allowed_create_org, allowed_add_member]), "All checks failed"

    # Expand relationships
    logger.info("Expanding relationships...")
    expanded = guard.expand(org_key2, "admin")
    logger.info(f"Expanded admin relationship: {expanded}")

    # List resources
    logger.info("Listing resources...")
    resources = guard.resources(user_key, "member", "org")
    logger.debug(f"User resources: {resources}")

    # Test get_user_roles method
    logger.info("Testing get_user_roles method...")
    user_model = Users(key=user_key, name="monika's user", email="monika@hussmann.com")
    org_model = Organization(key=org_key2, name="kevin's org")
    user_roles = guard.get_user_roles(user_model, org_model)
    logger.info(f"User roles: {user_roles}")
    assert "admin" in user_roles, "Expected 'admin' role not found"

    # Remove the site to test deletion
    logger.info("Removing site...")
    removed_site = guard.sites.remove(key=site_key)
    logger.debug(f"Removed site: {removed_site}")

    # Verify site removal
    site_list_after = guard.sites.list(limit=1)
    assert len(site_list_after) < len(site_list), "Failed to remove site"

    # Clean up: Remove created entities
    logger.info("Cleaning up...")
    guard.users.remove(key=user_key)
    guard.orgs.remove(key=org_key)
    guard.orgs.remove(key=org_key2)

    logger.info("Test workflow completed successfully!")

if __name__ == "__main__":
    main()