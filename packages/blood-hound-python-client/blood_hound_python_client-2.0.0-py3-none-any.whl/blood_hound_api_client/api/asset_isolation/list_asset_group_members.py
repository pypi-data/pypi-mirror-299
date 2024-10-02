from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_asset_group_members_response_200 import ListAssetGroupMembersResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    asset_group_id: int,
    *,
    skip: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    sort_by: Union[Unset, str] = UNSET,
    object_id: Union[Unset, str] = UNSET,
    primary_kind: Union[Unset, str] = UNSET,
    environment_id: Union[Unset, str] = UNSET,
    environment_kind: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    custom_member: Union[Unset, str] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    if not isinstance(prefer, Unset):
        headers["Prefer"] = str(prefer)

    params: Dict[str, Any] = {}

    params["skip"] = skip

    params["limit"] = limit

    params["sort_by"] = sort_by

    params["object_id"] = object_id

    params["primary_kind"] = primary_kind

    params["environment_id"] = environment_id

    params["environment_kind"] = environment_kind

    params["name"] = name

    params["custom_member"] = custom_member

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/api/v2/asset-groups/{asset_group_id}/members",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, ListAssetGroupMembersResponse200]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ListAssetGroupMembersResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = cast(Any, None)
        return response_401
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = cast(Any, None)
        return response_403
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = cast(Any, None)
        return response_404
    if response.status_code == HTTPStatus.TOO_MANY_REQUESTS:
        response_429 = cast(Any, None)
        return response_429
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = cast(Any, None)
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, ListAssetGroupMembersResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    asset_group_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    skip: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    sort_by: Union[Unset, str] = UNSET,
    object_id: Union[Unset, str] = UNSET,
    primary_kind: Union[Unset, str] = UNSET,
    environment_id: Union[Unset, str] = UNSET,
    environment_kind: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    custom_member: Union[Unset, str] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Response[Union[Any, ListAssetGroupMembersResponse200]]:
    """List all asset isolation group members

     List all members of an asset isolation group.

    Args:
        asset_group_id (int):
        skip (Union[Unset, int]): The number of items to skip in a paginated response.
        limit (Union[Unset, int]): The limit of results requested by the client.
        sort_by (Union[Unset, str]): Sort by column. Can be used multiple times; prepend a hyphen
            for descending order.
            See parameter description for details about which columns are sortable.
        object_id (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        primary_kind (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        environment_id (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        environment_kind (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        name (Union[Unset, str]): Filter results by column string value. Valid filter predicates
            are `eq`, `neq`.
        custom_member (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        prefer (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ListAssetGroupMembersResponse200]]
    """

    kwargs = _get_kwargs(
        asset_group_id=asset_group_id,
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        object_id=object_id,
        primary_kind=primary_kind,
        environment_id=environment_id,
        environment_kind=environment_kind,
        name=name,
        custom_member=custom_member,
        prefer=prefer,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    asset_group_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    skip: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    sort_by: Union[Unset, str] = UNSET,
    object_id: Union[Unset, str] = UNSET,
    primary_kind: Union[Unset, str] = UNSET,
    environment_id: Union[Unset, str] = UNSET,
    environment_kind: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    custom_member: Union[Unset, str] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Optional[Union[Any, ListAssetGroupMembersResponse200]]:
    """List all asset isolation group members

     List all members of an asset isolation group.

    Args:
        asset_group_id (int):
        skip (Union[Unset, int]): The number of items to skip in a paginated response.
        limit (Union[Unset, int]): The limit of results requested by the client.
        sort_by (Union[Unset, str]): Sort by column. Can be used multiple times; prepend a hyphen
            for descending order.
            See parameter description for details about which columns are sortable.
        object_id (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        primary_kind (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        environment_id (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        environment_kind (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        name (Union[Unset, str]): Filter results by column string value. Valid filter predicates
            are `eq`, `neq`.
        custom_member (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        prefer (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ListAssetGroupMembersResponse200]
    """

    return sync_detailed(
        asset_group_id=asset_group_id,
        client=client,
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        object_id=object_id,
        primary_kind=primary_kind,
        environment_id=environment_id,
        environment_kind=environment_kind,
        name=name,
        custom_member=custom_member,
        prefer=prefer,
    ).parsed


async def asyncio_detailed(
    asset_group_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    skip: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    sort_by: Union[Unset, str] = UNSET,
    object_id: Union[Unset, str] = UNSET,
    primary_kind: Union[Unset, str] = UNSET,
    environment_id: Union[Unset, str] = UNSET,
    environment_kind: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    custom_member: Union[Unset, str] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Response[Union[Any, ListAssetGroupMembersResponse200]]:
    """List all asset isolation group members

     List all members of an asset isolation group.

    Args:
        asset_group_id (int):
        skip (Union[Unset, int]): The number of items to skip in a paginated response.
        limit (Union[Unset, int]): The limit of results requested by the client.
        sort_by (Union[Unset, str]): Sort by column. Can be used multiple times; prepend a hyphen
            for descending order.
            See parameter description for details about which columns are sortable.
        object_id (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        primary_kind (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        environment_id (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        environment_kind (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        name (Union[Unset, str]): Filter results by column string value. Valid filter predicates
            are `eq`, `neq`.
        custom_member (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        prefer (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ListAssetGroupMembersResponse200]]
    """

    kwargs = _get_kwargs(
        asset_group_id=asset_group_id,
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        object_id=object_id,
        primary_kind=primary_kind,
        environment_id=environment_id,
        environment_kind=environment_kind,
        name=name,
        custom_member=custom_member,
        prefer=prefer,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    asset_group_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    skip: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    sort_by: Union[Unset, str] = UNSET,
    object_id: Union[Unset, str] = UNSET,
    primary_kind: Union[Unset, str] = UNSET,
    environment_id: Union[Unset, str] = UNSET,
    environment_kind: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    custom_member: Union[Unset, str] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Optional[Union[Any, ListAssetGroupMembersResponse200]]:
    """List all asset isolation group members

     List all members of an asset isolation group.

    Args:
        asset_group_id (int):
        skip (Union[Unset, int]): The number of items to skip in a paginated response.
        limit (Union[Unset, int]): The limit of results requested by the client.
        sort_by (Union[Unset, str]): Sort by column. Can be used multiple times; prepend a hyphen
            for descending order.
            See parameter description for details about which columns are sortable.
        object_id (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        primary_kind (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        environment_id (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        environment_kind (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        name (Union[Unset, str]): Filter results by column string value. Valid filter predicates
            are `eq`, `neq`.
        custom_member (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        prefer (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ListAssetGroupMembersResponse200]
    """

    return (
        await asyncio_detailed(
            asset_group_id=asset_group_id,
            client=client,
            skip=skip,
            limit=limit,
            sort_by=sort_by,
            object_id=object_id,
            primary_kind=primary_kind,
            environment_id=environment_id,
            environment_kind=environment_kind,
            name=name,
            custom_member=custom_member,
            prefer=prefer,
        )
    ).parsed
