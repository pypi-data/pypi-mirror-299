import datetime
from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_clients_response_200 import ListClientsResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    created_at: Union[Unset, datetime.datetime] = UNSET,
    updated_at: Union[Unset, datetime.datetime] = UNSET,
    deleted_at: Union[Unset, datetime.datetime] = UNSET,
    hydrate_domains: Union[Unset, bool] = True,
    hydrate_ous: Union[Unset, bool] = True,
    skip: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    sort_by: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    ip_address: Union[Unset, str] = UNSET,
    hostname: Union[Unset, str] = UNSET,
    configured_user: Union[Unset, str] = UNSET,
    version: Union[Unset, str] = UNSET,
    user_sid: Union[Unset, str] = UNSET,
    last_checkin: Union[Unset, str] = UNSET,
    current_job_id: Union[Unset, int] = UNSET,
    completed_job_count: Union[Unset, int] = UNSET,
    domain_controller: Union[Unset, str] = UNSET,
    id: Union[Unset, str] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    if not isinstance(prefer, Unset):
        headers["Prefer"] = str(prefer)

    params: Dict[str, Any] = {}

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

    params["hydrate_domains"] = hydrate_domains

    params["hydrate_ous"] = hydrate_ous

    params["skip"] = skip

    params["limit"] = limit

    params["sort_by"] = sort_by

    params["name"] = name

    params["ip_address"] = ip_address

    params["hostname"] = hostname

    params["configured_user"] = configured_user

    params["version"] = version

    params["user_sid"] = user_sid

    params["last_checkin"] = last_checkin

    params["current_job_id"] = current_job_id

    params["completed_job_count"] = completed_job_count

    params["domain_controller"] = domain_controller

    params["id"] = id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/api/v2/clients",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, ListClientsResponse200]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ListClientsResponse200.from_dict(response.json())

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
) -> Response[Union[Any, ListClientsResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    created_at: Union[Unset, datetime.datetime] = UNSET,
    updated_at: Union[Unset, datetime.datetime] = UNSET,
    deleted_at: Union[Unset, datetime.datetime] = UNSET,
    hydrate_domains: Union[Unset, bool] = True,
    hydrate_ous: Union[Unset, bool] = True,
    skip: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    sort_by: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    ip_address: Union[Unset, str] = UNSET,
    hostname: Union[Unset, str] = UNSET,
    configured_user: Union[Unset, str] = UNSET,
    version: Union[Unset, str] = UNSET,
    user_sid: Union[Unset, str] = UNSET,
    last_checkin: Union[Unset, str] = UNSET,
    current_job_id: Union[Unset, int] = UNSET,
    completed_job_count: Union[Unset, int] = UNSET,
    domain_controller: Union[Unset, str] = UNSET,
    id: Union[Unset, str] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Response[Union[Any, ListClientsResponse200]]:
    """List Clients

     Lists available clients for processing collection events.

    Args:
        created_at (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        updated_at (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        deleted_at (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        hydrate_domains (Union[Unset, bool]):  Default: True.
        hydrate_ous (Union[Unset, bool]):  Default: True.
        skip (Union[Unset, int]): The number of items to skip in a paginated response.
        limit (Union[Unset, int]): The limit of results requested by the client.
        sort_by (Union[Unset, str]): Sort by column. Can be used multiple times; prepend a hyphen
            for descending order.
            See parameter description for details about which columns are sortable.
        name (Union[Unset, str]): Filter results by column string value. Valid filter predicates
            are `eq`, `neq`.
        ip_address (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        hostname (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        configured_user (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        version (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        user_sid (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        last_checkin (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        current_job_id (Union[Unset, int]): Filter results by column integer value. Valid filter
            predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        completed_job_count (Union[Unset, int]): Filter results by column integer value. Valid
            filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        domain_controller (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        id (Union[Unset, str]): Filter results by column string-formatted uuid value. Valid filter
            predicates are `eq`, `neq`.
        prefer (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ListClientsResponse200]]
    """

    kwargs = _get_kwargs(
        created_at=created_at,
        updated_at=updated_at,
        deleted_at=deleted_at,
        hydrate_domains=hydrate_domains,
        hydrate_ous=hydrate_ous,
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        name=name,
        ip_address=ip_address,
        hostname=hostname,
        configured_user=configured_user,
        version=version,
        user_sid=user_sid,
        last_checkin=last_checkin,
        current_job_id=current_job_id,
        completed_job_count=completed_job_count,
        domain_controller=domain_controller,
        id=id,
        prefer=prefer,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    created_at: Union[Unset, datetime.datetime] = UNSET,
    updated_at: Union[Unset, datetime.datetime] = UNSET,
    deleted_at: Union[Unset, datetime.datetime] = UNSET,
    hydrate_domains: Union[Unset, bool] = True,
    hydrate_ous: Union[Unset, bool] = True,
    skip: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    sort_by: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    ip_address: Union[Unset, str] = UNSET,
    hostname: Union[Unset, str] = UNSET,
    configured_user: Union[Unset, str] = UNSET,
    version: Union[Unset, str] = UNSET,
    user_sid: Union[Unset, str] = UNSET,
    last_checkin: Union[Unset, str] = UNSET,
    current_job_id: Union[Unset, int] = UNSET,
    completed_job_count: Union[Unset, int] = UNSET,
    domain_controller: Union[Unset, str] = UNSET,
    id: Union[Unset, str] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Optional[Union[Any, ListClientsResponse200]]:
    """List Clients

     Lists available clients for processing collection events.

    Args:
        created_at (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        updated_at (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        deleted_at (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        hydrate_domains (Union[Unset, bool]):  Default: True.
        hydrate_ous (Union[Unset, bool]):  Default: True.
        skip (Union[Unset, int]): The number of items to skip in a paginated response.
        limit (Union[Unset, int]): The limit of results requested by the client.
        sort_by (Union[Unset, str]): Sort by column. Can be used multiple times; prepend a hyphen
            for descending order.
            See parameter description for details about which columns are sortable.
        name (Union[Unset, str]): Filter results by column string value. Valid filter predicates
            are `eq`, `neq`.
        ip_address (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        hostname (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        configured_user (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        version (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        user_sid (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        last_checkin (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        current_job_id (Union[Unset, int]): Filter results by column integer value. Valid filter
            predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        completed_job_count (Union[Unset, int]): Filter results by column integer value. Valid
            filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        domain_controller (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        id (Union[Unset, str]): Filter results by column string-formatted uuid value. Valid filter
            predicates are `eq`, `neq`.
        prefer (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ListClientsResponse200]
    """

    return sync_detailed(
        client=client,
        created_at=created_at,
        updated_at=updated_at,
        deleted_at=deleted_at,
        hydrate_domains=hydrate_domains,
        hydrate_ous=hydrate_ous,
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        name=name,
        ip_address=ip_address,
        hostname=hostname,
        configured_user=configured_user,
        version=version,
        user_sid=user_sid,
        last_checkin=last_checkin,
        current_job_id=current_job_id,
        completed_job_count=completed_job_count,
        domain_controller=domain_controller,
        id=id,
        prefer=prefer,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    created_at: Union[Unset, datetime.datetime] = UNSET,
    updated_at: Union[Unset, datetime.datetime] = UNSET,
    deleted_at: Union[Unset, datetime.datetime] = UNSET,
    hydrate_domains: Union[Unset, bool] = True,
    hydrate_ous: Union[Unset, bool] = True,
    skip: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    sort_by: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    ip_address: Union[Unset, str] = UNSET,
    hostname: Union[Unset, str] = UNSET,
    configured_user: Union[Unset, str] = UNSET,
    version: Union[Unset, str] = UNSET,
    user_sid: Union[Unset, str] = UNSET,
    last_checkin: Union[Unset, str] = UNSET,
    current_job_id: Union[Unset, int] = UNSET,
    completed_job_count: Union[Unset, int] = UNSET,
    domain_controller: Union[Unset, str] = UNSET,
    id: Union[Unset, str] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Response[Union[Any, ListClientsResponse200]]:
    """List Clients

     Lists available clients for processing collection events.

    Args:
        created_at (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        updated_at (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        deleted_at (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        hydrate_domains (Union[Unset, bool]):  Default: True.
        hydrate_ous (Union[Unset, bool]):  Default: True.
        skip (Union[Unset, int]): The number of items to skip in a paginated response.
        limit (Union[Unset, int]): The limit of results requested by the client.
        sort_by (Union[Unset, str]): Sort by column. Can be used multiple times; prepend a hyphen
            for descending order.
            See parameter description for details about which columns are sortable.
        name (Union[Unset, str]): Filter results by column string value. Valid filter predicates
            are `eq`, `neq`.
        ip_address (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        hostname (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        configured_user (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        version (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        user_sid (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        last_checkin (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        current_job_id (Union[Unset, int]): Filter results by column integer value. Valid filter
            predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        completed_job_count (Union[Unset, int]): Filter results by column integer value. Valid
            filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        domain_controller (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        id (Union[Unset, str]): Filter results by column string-formatted uuid value. Valid filter
            predicates are `eq`, `neq`.
        prefer (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ListClientsResponse200]]
    """

    kwargs = _get_kwargs(
        created_at=created_at,
        updated_at=updated_at,
        deleted_at=deleted_at,
        hydrate_domains=hydrate_domains,
        hydrate_ous=hydrate_ous,
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        name=name,
        ip_address=ip_address,
        hostname=hostname,
        configured_user=configured_user,
        version=version,
        user_sid=user_sid,
        last_checkin=last_checkin,
        current_job_id=current_job_id,
        completed_job_count=completed_job_count,
        domain_controller=domain_controller,
        id=id,
        prefer=prefer,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    created_at: Union[Unset, datetime.datetime] = UNSET,
    updated_at: Union[Unset, datetime.datetime] = UNSET,
    deleted_at: Union[Unset, datetime.datetime] = UNSET,
    hydrate_domains: Union[Unset, bool] = True,
    hydrate_ous: Union[Unset, bool] = True,
    skip: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    sort_by: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    ip_address: Union[Unset, str] = UNSET,
    hostname: Union[Unset, str] = UNSET,
    configured_user: Union[Unset, str] = UNSET,
    version: Union[Unset, str] = UNSET,
    user_sid: Union[Unset, str] = UNSET,
    last_checkin: Union[Unset, str] = UNSET,
    current_job_id: Union[Unset, int] = UNSET,
    completed_job_count: Union[Unset, int] = UNSET,
    domain_controller: Union[Unset, str] = UNSET,
    id: Union[Unset, str] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Optional[Union[Any, ListClientsResponse200]]:
    """List Clients

     Lists available clients for processing collection events.

    Args:
        created_at (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        updated_at (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        deleted_at (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        hydrate_domains (Union[Unset, bool]):  Default: True.
        hydrate_ous (Union[Unset, bool]):  Default: True.
        skip (Union[Unset, int]): The number of items to skip in a paginated response.
        limit (Union[Unset, int]): The limit of results requested by the client.
        sort_by (Union[Unset, str]): Sort by column. Can be used multiple times; prepend a hyphen
            for descending order.
            See parameter description for details about which columns are sortable.
        name (Union[Unset, str]): Filter results by column string value. Valid filter predicates
            are `eq`, `neq`.
        ip_address (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        hostname (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        configured_user (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        version (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        user_sid (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        last_checkin (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        current_job_id (Union[Unset, int]): Filter results by column integer value. Valid filter
            predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        completed_job_count (Union[Unset, int]): Filter results by column integer value. Valid
            filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        domain_controller (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        id (Union[Unset, str]): Filter results by column string-formatted uuid value. Valid filter
            predicates are `eq`, `neq`.
        prefer (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ListClientsResponse200]
    """

    return (
        await asyncio_detailed(
            client=client,
            created_at=created_at,
            updated_at=updated_at,
            deleted_at=deleted_at,
            hydrate_domains=hydrate_domains,
            hydrate_ous=hydrate_ous,
            skip=skip,
            limit=limit,
            sort_by=sort_by,
            name=name,
            ip_address=ip_address,
            hostname=hostname,
            configured_user=configured_user,
            version=version,
            user_sid=user_sid,
            last_checkin=last_checkin,
            current_job_id=current_job_id,
            completed_job_count=completed_job_count,
            domain_controller=domain_controller,
            id=id,
            prefer=prefer,
        )
    ).parsed
