import datetime
from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_roles_response_200 import ListRolesResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    sort_by: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    id: Union[Unset, int] = UNSET,
    created_at: Union[Unset, datetime.datetime] = UNSET,
    updated_at: Union[Unset, datetime.datetime] = UNSET,
    deleted_at: Union[Unset, datetime.datetime] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    if not isinstance(prefer, Unset):
        headers["Prefer"] = str(prefer)

    params: Dict[str, Any] = {}

    params["sort_by"] = sort_by

    params["name"] = name

    params["id"] = id

    json_created_at: Union[Unset, str] = UNSET
    if not isinstance(created_at, Unset):
        json_created_at = created_at.isoformat()
    params["created_at"] = json_created_at

    json_updated_at: Union[Unset, str] = UNSET
    if not isinstance(updated_at, Unset):
        json_updated_at = updated_at.isoformat()
    params["updated_at"] = json_updated_at

    json_deleted_at: Union[Unset, str] = UNSET
    if not isinstance(deleted_at, Unset):
        json_deleted_at = deleted_at.isoformat()
    params["deleted_at"] = json_deleted_at

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/api/v2/roles",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, ListRolesResponse200]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ListRolesResponse200.from_dict(response.json())

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
) -> Response[Union[Any, ListRolesResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    sort_by: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    id: Union[Unset, int] = UNSET,
    created_at: Union[Unset, datetime.datetime] = UNSET,
    updated_at: Union[Unset, datetime.datetime] = UNSET,
    deleted_at: Union[Unset, datetime.datetime] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Response[Union[Any, ListRolesResponse200]]:
    """List Roles

     List all authorization roles.

    Args:
        sort_by (Union[Unset, str]): Sort by column. Can be used multiple times; prepend a hyphen
            for descending order.
            See parameter description for details about which columns are sortable.
        name (Union[Unset, str]): Filter results by column string value. Valid filter predicates
            are `eq`, `neq`.
        id (Union[Unset, int]): Filter results by column integer value. Valid filter predicates
            are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        created_at (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        updated_at (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        deleted_at (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        prefer (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ListRolesResponse200]]
    """

    kwargs = _get_kwargs(
        sort_by=sort_by,
        name=name,
        id=id,
        created_at=created_at,
        updated_at=updated_at,
        deleted_at=deleted_at,
        prefer=prefer,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    sort_by: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    id: Union[Unset, int] = UNSET,
    created_at: Union[Unset, datetime.datetime] = UNSET,
    updated_at: Union[Unset, datetime.datetime] = UNSET,
    deleted_at: Union[Unset, datetime.datetime] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Optional[Union[Any, ListRolesResponse200]]:
    """List Roles

     List all authorization roles.

    Args:
        sort_by (Union[Unset, str]): Sort by column. Can be used multiple times; prepend a hyphen
            for descending order.
            See parameter description for details about which columns are sortable.
        name (Union[Unset, str]): Filter results by column string value. Valid filter predicates
            are `eq`, `neq`.
        id (Union[Unset, int]): Filter results by column integer value. Valid filter predicates
            are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        created_at (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        updated_at (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        deleted_at (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        prefer (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ListRolesResponse200]
    """

    return sync_detailed(
        client=client,
        sort_by=sort_by,
        name=name,
        id=id,
        created_at=created_at,
        updated_at=updated_at,
        deleted_at=deleted_at,
        prefer=prefer,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    sort_by: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    id: Union[Unset, int] = UNSET,
    created_at: Union[Unset, datetime.datetime] = UNSET,
    updated_at: Union[Unset, datetime.datetime] = UNSET,
    deleted_at: Union[Unset, datetime.datetime] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Response[Union[Any, ListRolesResponse200]]:
    """List Roles

     List all authorization roles.

    Args:
        sort_by (Union[Unset, str]): Sort by column. Can be used multiple times; prepend a hyphen
            for descending order.
            See parameter description for details about which columns are sortable.
        name (Union[Unset, str]): Filter results by column string value. Valid filter predicates
            are `eq`, `neq`.
        id (Union[Unset, int]): Filter results by column integer value. Valid filter predicates
            are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        created_at (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        updated_at (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        deleted_at (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        prefer (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ListRolesResponse200]]
    """

    kwargs = _get_kwargs(
        sort_by=sort_by,
        name=name,
        id=id,
        created_at=created_at,
        updated_at=updated_at,
        deleted_at=deleted_at,
        prefer=prefer,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    sort_by: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    id: Union[Unset, int] = UNSET,
    created_at: Union[Unset, datetime.datetime] = UNSET,
    updated_at: Union[Unset, datetime.datetime] = UNSET,
    deleted_at: Union[Unset, datetime.datetime] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Optional[Union[Any, ListRolesResponse200]]:
    """List Roles

     List all authorization roles.

    Args:
        sort_by (Union[Unset, str]): Sort by column. Can be used multiple times; prepend a hyphen
            for descending order.
            See parameter description for details about which columns are sortable.
        name (Union[Unset, str]): Filter results by column string value. Valid filter predicates
            are `eq`, `neq`.
        id (Union[Unset, int]): Filter results by column integer value. Valid filter predicates
            are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        created_at (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        updated_at (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        deleted_at (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        prefer (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ListRolesResponse200]
    """

    return (
        await asyncio_detailed(
            client=client,
            sort_by=sort_by,
            name=name,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            deleted_at=deleted_at,
            prefer=prefer,
        )
    ).parsed
