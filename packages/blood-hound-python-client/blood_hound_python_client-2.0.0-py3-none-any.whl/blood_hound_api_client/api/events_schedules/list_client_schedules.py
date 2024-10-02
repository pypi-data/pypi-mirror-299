import datetime
from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_client_schedules_response_200 import ListClientSchedulesResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    sort_by: Union[Unset, str] = UNSET,
    id: Union[Unset, int] = UNSET,
    rrule: Union[Unset, str] = UNSET,
    next_scheduled_at: Union[Unset, datetime.datetime] = UNSET,
    client_id: Union[Unset, str] = UNSET,
    session_collection: Union[Unset, bool] = UNSET,
    local_group_collection: Union[Unset, bool] = UNSET,
    ad_structure_collection: Union[Unset, bool] = UNSET,
    cert_services_collection: Union[Unset, bool] = UNSET,
    ca_registry_collection: Union[Unset, bool] = UNSET,
    dc_registry_collection: Union[Unset, bool] = UNSET,
    hydrate_domains: Union[Unset, bool] = True,
    hydrate_ous: Union[Unset, bool] = True,
    created_at: Union[Unset, datetime.datetime] = UNSET,
    updated_at: Union[Unset, datetime.datetime] = UNSET,
    deleted_at: Union[Unset, datetime.datetime] = UNSET,
    skip: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    if not isinstance(prefer, Unset):
        headers["Prefer"] = str(prefer)

    params: Dict[str, Any] = {}

    params["sort_by"] = sort_by

    params["id"] = id

    params["rrule"] = rrule

    json_next_scheduled_at: Union[Unset, str] = UNSET
    if not isinstance(next_scheduled_at, Unset):
        json_next_scheduled_at = next_scheduled_at.isoformat()
    params["next_scheduled_at"] = json_next_scheduled_at

    params["client_id"] = client_id

    params["session_collection"] = session_collection

    params["local_group_collection"] = local_group_collection

    params["ad_structure_collection"] = ad_structure_collection

    params["cert_services_collection"] = cert_services_collection

    params["ca_registry_collection"] = ca_registry_collection

    params["dc_registry_collection"] = dc_registry_collection

    params["hydrate_domains"] = hydrate_domains

    params["hydrate_ous"] = hydrate_ous

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

    params["skip"] = skip

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/api/v2/events",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, ListClientSchedulesResponse200]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ListClientSchedulesResponse200.from_dict(response.json())

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
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = cast(Any, None)
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, ListClientSchedulesResponse200]]:
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
    id: Union[Unset, int] = UNSET,
    rrule: Union[Unset, str] = UNSET,
    next_scheduled_at: Union[Unset, datetime.datetime] = UNSET,
    client_id: Union[Unset, str] = UNSET,
    session_collection: Union[Unset, bool] = UNSET,
    local_group_collection: Union[Unset, bool] = UNSET,
    ad_structure_collection: Union[Unset, bool] = UNSET,
    cert_services_collection: Union[Unset, bool] = UNSET,
    ca_registry_collection: Union[Unset, bool] = UNSET,
    dc_registry_collection: Union[Unset, bool] = UNSET,
    hydrate_domains: Union[Unset, bool] = True,
    hydrate_ous: Union[Unset, bool] = True,
    created_at: Union[Unset, datetime.datetime] = UNSET,
    updated_at: Union[Unset, datetime.datetime] = UNSET,
    deleted_at: Union[Unset, datetime.datetime] = UNSET,
    skip: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Response[Union[Any, ListClientSchedulesResponse200]]:
    """List events

     Gets all client scheduled events.

    Args:
        sort_by (Union[Unset, str]): Sort by column. Can be used multiple times; prepend a hyphen
            for descending order.
            See parameter description for details about which columns are sortable.
        id (Union[Unset, int]): Filter results by column integer value. Valid filter predicates
            are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        rrule (Union[Unset, str]): Filter results by column string value. Valid filter predicates
            are `eq`, `neq`.
        next_scheduled_at (Union[Unset, datetime.datetime]): Filter results by column timestamp
            value formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        client_id (Union[Unset, str]): Filter results by column string-formatted uuid value. Valid
            filter predicates are `eq`, `neq`.
        session_collection (Union[Unset, bool]): Filter results by column boolean value. Valid
            filter predicates are `eq`, `neq`.
        local_group_collection (Union[Unset, bool]): Filter results by column boolean value. Valid
            filter predicates are `eq`, `neq`.
        ad_structure_collection (Union[Unset, bool]): Filter results by column boolean value.
            Valid filter predicates are `eq`, `neq`.
        cert_services_collection (Union[Unset, bool]): Filter results by column boolean value.
            Valid filter predicates are `eq`, `neq`.
        ca_registry_collection (Union[Unset, bool]): Filter results by column boolean value. Valid
            filter predicates are `eq`, `neq`.
        dc_registry_collection (Union[Unset, bool]): Filter results by column boolean value. Valid
            filter predicates are `eq`, `neq`.
        hydrate_domains (Union[Unset, bool]):  Default: True.
        hydrate_ous (Union[Unset, bool]):  Default: True.
        created_at (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        updated_at (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        deleted_at (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        skip (Union[Unset, int]): The number of items to skip in a paginated response.
        limit (Union[Unset, int]): The limit of results requested by the client.
        prefer (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ListClientSchedulesResponse200]]
    """

    kwargs = _get_kwargs(
        sort_by=sort_by,
        id=id,
        rrule=rrule,
        next_scheduled_at=next_scheduled_at,
        client_id=client_id,
        session_collection=session_collection,
        local_group_collection=local_group_collection,
        ad_structure_collection=ad_structure_collection,
        cert_services_collection=cert_services_collection,
        ca_registry_collection=ca_registry_collection,
        dc_registry_collection=dc_registry_collection,
        hydrate_domains=hydrate_domains,
        hydrate_ous=hydrate_ous,
        created_at=created_at,
        updated_at=updated_at,
        deleted_at=deleted_at,
        skip=skip,
        limit=limit,
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
    id: Union[Unset, int] = UNSET,
    rrule: Union[Unset, str] = UNSET,
    next_scheduled_at: Union[Unset, datetime.datetime] = UNSET,
    client_id: Union[Unset, str] = UNSET,
    session_collection: Union[Unset, bool] = UNSET,
    local_group_collection: Union[Unset, bool] = UNSET,
    ad_structure_collection: Union[Unset, bool] = UNSET,
    cert_services_collection: Union[Unset, bool] = UNSET,
    ca_registry_collection: Union[Unset, bool] = UNSET,
    dc_registry_collection: Union[Unset, bool] = UNSET,
    hydrate_domains: Union[Unset, bool] = True,
    hydrate_ous: Union[Unset, bool] = True,
    created_at: Union[Unset, datetime.datetime] = UNSET,
    updated_at: Union[Unset, datetime.datetime] = UNSET,
    deleted_at: Union[Unset, datetime.datetime] = UNSET,
    skip: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Optional[Union[Any, ListClientSchedulesResponse200]]:
    """List events

     Gets all client scheduled events.

    Args:
        sort_by (Union[Unset, str]): Sort by column. Can be used multiple times; prepend a hyphen
            for descending order.
            See parameter description for details about which columns are sortable.
        id (Union[Unset, int]): Filter results by column integer value. Valid filter predicates
            are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        rrule (Union[Unset, str]): Filter results by column string value. Valid filter predicates
            are `eq`, `neq`.
        next_scheduled_at (Union[Unset, datetime.datetime]): Filter results by column timestamp
            value formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        client_id (Union[Unset, str]): Filter results by column string-formatted uuid value. Valid
            filter predicates are `eq`, `neq`.
        session_collection (Union[Unset, bool]): Filter results by column boolean value. Valid
            filter predicates are `eq`, `neq`.
        local_group_collection (Union[Unset, bool]): Filter results by column boolean value. Valid
            filter predicates are `eq`, `neq`.
        ad_structure_collection (Union[Unset, bool]): Filter results by column boolean value.
            Valid filter predicates are `eq`, `neq`.
        cert_services_collection (Union[Unset, bool]): Filter results by column boolean value.
            Valid filter predicates are `eq`, `neq`.
        ca_registry_collection (Union[Unset, bool]): Filter results by column boolean value. Valid
            filter predicates are `eq`, `neq`.
        dc_registry_collection (Union[Unset, bool]): Filter results by column boolean value. Valid
            filter predicates are `eq`, `neq`.
        hydrate_domains (Union[Unset, bool]):  Default: True.
        hydrate_ous (Union[Unset, bool]):  Default: True.
        created_at (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        updated_at (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        deleted_at (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        skip (Union[Unset, int]): The number of items to skip in a paginated response.
        limit (Union[Unset, int]): The limit of results requested by the client.
        prefer (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ListClientSchedulesResponse200]
    """

    return sync_detailed(
        client=client,
        sort_by=sort_by,
        id=id,
        rrule=rrule,
        next_scheduled_at=next_scheduled_at,
        client_id=client_id,
        session_collection=session_collection,
        local_group_collection=local_group_collection,
        ad_structure_collection=ad_structure_collection,
        cert_services_collection=cert_services_collection,
        ca_registry_collection=ca_registry_collection,
        dc_registry_collection=dc_registry_collection,
        hydrate_domains=hydrate_domains,
        hydrate_ous=hydrate_ous,
        created_at=created_at,
        updated_at=updated_at,
        deleted_at=deleted_at,
        skip=skip,
        limit=limit,
        prefer=prefer,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    sort_by: Union[Unset, str] = UNSET,
    id: Union[Unset, int] = UNSET,
    rrule: Union[Unset, str] = UNSET,
    next_scheduled_at: Union[Unset, datetime.datetime] = UNSET,
    client_id: Union[Unset, str] = UNSET,
    session_collection: Union[Unset, bool] = UNSET,
    local_group_collection: Union[Unset, bool] = UNSET,
    ad_structure_collection: Union[Unset, bool] = UNSET,
    cert_services_collection: Union[Unset, bool] = UNSET,
    ca_registry_collection: Union[Unset, bool] = UNSET,
    dc_registry_collection: Union[Unset, bool] = UNSET,
    hydrate_domains: Union[Unset, bool] = True,
    hydrate_ous: Union[Unset, bool] = True,
    created_at: Union[Unset, datetime.datetime] = UNSET,
    updated_at: Union[Unset, datetime.datetime] = UNSET,
    deleted_at: Union[Unset, datetime.datetime] = UNSET,
    skip: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Response[Union[Any, ListClientSchedulesResponse200]]:
    """List events

     Gets all client scheduled events.

    Args:
        sort_by (Union[Unset, str]): Sort by column. Can be used multiple times; prepend a hyphen
            for descending order.
            See parameter description for details about which columns are sortable.
        id (Union[Unset, int]): Filter results by column integer value. Valid filter predicates
            are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        rrule (Union[Unset, str]): Filter results by column string value. Valid filter predicates
            are `eq`, `neq`.
        next_scheduled_at (Union[Unset, datetime.datetime]): Filter results by column timestamp
            value formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        client_id (Union[Unset, str]): Filter results by column string-formatted uuid value. Valid
            filter predicates are `eq`, `neq`.
        session_collection (Union[Unset, bool]): Filter results by column boolean value. Valid
            filter predicates are `eq`, `neq`.
        local_group_collection (Union[Unset, bool]): Filter results by column boolean value. Valid
            filter predicates are `eq`, `neq`.
        ad_structure_collection (Union[Unset, bool]): Filter results by column boolean value.
            Valid filter predicates are `eq`, `neq`.
        cert_services_collection (Union[Unset, bool]): Filter results by column boolean value.
            Valid filter predicates are `eq`, `neq`.
        ca_registry_collection (Union[Unset, bool]): Filter results by column boolean value. Valid
            filter predicates are `eq`, `neq`.
        dc_registry_collection (Union[Unset, bool]): Filter results by column boolean value. Valid
            filter predicates are `eq`, `neq`.
        hydrate_domains (Union[Unset, bool]):  Default: True.
        hydrate_ous (Union[Unset, bool]):  Default: True.
        created_at (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        updated_at (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        deleted_at (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        skip (Union[Unset, int]): The number of items to skip in a paginated response.
        limit (Union[Unset, int]): The limit of results requested by the client.
        prefer (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ListClientSchedulesResponse200]]
    """

    kwargs = _get_kwargs(
        sort_by=sort_by,
        id=id,
        rrule=rrule,
        next_scheduled_at=next_scheduled_at,
        client_id=client_id,
        session_collection=session_collection,
        local_group_collection=local_group_collection,
        ad_structure_collection=ad_structure_collection,
        cert_services_collection=cert_services_collection,
        ca_registry_collection=ca_registry_collection,
        dc_registry_collection=dc_registry_collection,
        hydrate_domains=hydrate_domains,
        hydrate_ous=hydrate_ous,
        created_at=created_at,
        updated_at=updated_at,
        deleted_at=deleted_at,
        skip=skip,
        limit=limit,
        prefer=prefer,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    sort_by: Union[Unset, str] = UNSET,
    id: Union[Unset, int] = UNSET,
    rrule: Union[Unset, str] = UNSET,
    next_scheduled_at: Union[Unset, datetime.datetime] = UNSET,
    client_id: Union[Unset, str] = UNSET,
    session_collection: Union[Unset, bool] = UNSET,
    local_group_collection: Union[Unset, bool] = UNSET,
    ad_structure_collection: Union[Unset, bool] = UNSET,
    cert_services_collection: Union[Unset, bool] = UNSET,
    ca_registry_collection: Union[Unset, bool] = UNSET,
    dc_registry_collection: Union[Unset, bool] = UNSET,
    hydrate_domains: Union[Unset, bool] = True,
    hydrate_ous: Union[Unset, bool] = True,
    created_at: Union[Unset, datetime.datetime] = UNSET,
    updated_at: Union[Unset, datetime.datetime] = UNSET,
    deleted_at: Union[Unset, datetime.datetime] = UNSET,
    skip: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Optional[Union[Any, ListClientSchedulesResponse200]]:
    """List events

     Gets all client scheduled events.

    Args:
        sort_by (Union[Unset, str]): Sort by column. Can be used multiple times; prepend a hyphen
            for descending order.
            See parameter description for details about which columns are sortable.
        id (Union[Unset, int]): Filter results by column integer value. Valid filter predicates
            are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        rrule (Union[Unset, str]): Filter results by column string value. Valid filter predicates
            are `eq`, `neq`.
        next_scheduled_at (Union[Unset, datetime.datetime]): Filter results by column timestamp
            value formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        client_id (Union[Unset, str]): Filter results by column string-formatted uuid value. Valid
            filter predicates are `eq`, `neq`.
        session_collection (Union[Unset, bool]): Filter results by column boolean value. Valid
            filter predicates are `eq`, `neq`.
        local_group_collection (Union[Unset, bool]): Filter results by column boolean value. Valid
            filter predicates are `eq`, `neq`.
        ad_structure_collection (Union[Unset, bool]): Filter results by column boolean value.
            Valid filter predicates are `eq`, `neq`.
        cert_services_collection (Union[Unset, bool]): Filter results by column boolean value.
            Valid filter predicates are `eq`, `neq`.
        ca_registry_collection (Union[Unset, bool]): Filter results by column boolean value. Valid
            filter predicates are `eq`, `neq`.
        dc_registry_collection (Union[Unset, bool]): Filter results by column boolean value. Valid
            filter predicates are `eq`, `neq`.
        hydrate_domains (Union[Unset, bool]):  Default: True.
        hydrate_ous (Union[Unset, bool]):  Default: True.
        created_at (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        updated_at (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        deleted_at (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        skip (Union[Unset, int]): The number of items to skip in a paginated response.
        limit (Union[Unset, int]): The limit of results requested by the client.
        prefer (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ListClientSchedulesResponse200]
    """

    return (
        await asyncio_detailed(
            client=client,
            sort_by=sort_by,
            id=id,
            rrule=rrule,
            next_scheduled_at=next_scheduled_at,
            client_id=client_id,
            session_collection=session_collection,
            local_group_collection=local_group_collection,
            ad_structure_collection=ad_structure_collection,
            cert_services_collection=cert_services_collection,
            ca_registry_collection=ca_registry_collection,
            dc_registry_collection=dc_registry_collection,
            hydrate_domains=hydrate_domains,
            hydrate_ous=hydrate_ous,
            created_at=created_at,
            updated_at=updated_at,
            deleted_at=deleted_at,
            skip=skip,
            limit=limit,
            prefer=prefer,
        )
    ).parsed
