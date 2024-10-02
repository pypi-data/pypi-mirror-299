import datetime
from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_client_finished_jobs_response_200 import ListClientFinishedJobsResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    sort_by: Union[Unset, str] = UNSET,
    log_path: Union[Unset, str] = UNSET,
    session_collection: Union[Unset, bool] = UNSET,
    local_group_collection: Union[Unset, bool] = UNSET,
    cert_services_collection: Union[Unset, bool] = UNSET,
    ca_registry_collection: Union[Unset, bool] = UNSET,
    dc_registry_collection: Union[Unset, bool] = UNSET,
    ad_structure_collection: Union[Unset, bool] = UNSET,
    domain_controller: Union[Unset, str] = UNSET,
    status: Union[Unset, str] = UNSET,
    event_title: Union[Unset, str] = UNSET,
    client_id: Union[Unset, str] = UNSET,
    event_id: Union[Unset, int] = UNSET,
    execution_time: Union[Unset, datetime.datetime] = UNSET,
    start_time: Union[Unset, datetime.datetime] = UNSET,
    end_time: Union[Unset, datetime.datetime] = UNSET,
    last_ingest: Union[Unset, datetime.datetime] = UNSET,
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

    params["log_path"] = log_path

    params["session_collection"] = session_collection

    params["local_group_collection"] = local_group_collection

    params["cert_services_collection"] = cert_services_collection

    params["ca_registry_collection"] = ca_registry_collection

    params["dc_registry_collection"] = dc_registry_collection

    params["ad_structure_collection"] = ad_structure_collection

    params["domain_controller"] = domain_controller

    params["status"] = status

    params["event_title"] = event_title

    params["client_id"] = client_id

    params["event_id"] = event_id

    json_execution_time: Union[Unset, str] = UNSET
    if not isinstance(execution_time, Unset):
        json_execution_time = execution_time.isoformat()
    params["execution_time"] = json_execution_time

    json_start_time: Union[Unset, str] = UNSET
    if not isinstance(start_time, Unset):
        json_start_time = start_time.isoformat()
    params["start_time"] = json_start_time

    json_end_time: Union[Unset, str] = UNSET
    if not isinstance(end_time, Unset):
        json_end_time = end_time.isoformat()
    params["end_time"] = json_end_time

    json_last_ingest: Union[Unset, str] = UNSET
    if not isinstance(last_ingest, Unset):
        json_last_ingest = last_ingest.isoformat()
    params["last_ingest"] = json_last_ingest

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
        "url": "/api/v2/jobs/finished",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, ListClientFinishedJobsResponse200]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ListClientFinishedJobsResponse200.from_dict(response.json())

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
) -> Response[Union[Any, ListClientFinishedJobsResponse200]]:
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
    log_path: Union[Unset, str] = UNSET,
    session_collection: Union[Unset, bool] = UNSET,
    local_group_collection: Union[Unset, bool] = UNSET,
    cert_services_collection: Union[Unset, bool] = UNSET,
    ca_registry_collection: Union[Unset, bool] = UNSET,
    dc_registry_collection: Union[Unset, bool] = UNSET,
    ad_structure_collection: Union[Unset, bool] = UNSET,
    domain_controller: Union[Unset, str] = UNSET,
    status: Union[Unset, str] = UNSET,
    event_title: Union[Unset, str] = UNSET,
    client_id: Union[Unset, str] = UNSET,
    event_id: Union[Unset, int] = UNSET,
    execution_time: Union[Unset, datetime.datetime] = UNSET,
    start_time: Union[Unset, datetime.datetime] = UNSET,
    end_time: Union[Unset, datetime.datetime] = UNSET,
    last_ingest: Union[Unset, datetime.datetime] = UNSET,
    hydrate_domains: Union[Unset, bool] = True,
    hydrate_ous: Union[Unset, bool] = True,
    created_at: Union[Unset, datetime.datetime] = UNSET,
    updated_at: Union[Unset, datetime.datetime] = UNSET,
    deleted_at: Union[Unset, datetime.datetime] = UNSET,
    skip: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Response[Union[Any, ListClientFinishedJobsResponse200]]:
    """List finished jobs

     Gets all finished jobs

    Args:
        sort_by (Union[Unset, str]): Sort by column. Can be used multiple times; prepend a hyphen
            for descending order.
            See parameter description for details about which columns are sortable.
        log_path (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        session_collection (Union[Unset, bool]): Filter results by column boolean value. Valid
            filter predicates are `eq`, `neq`.
        local_group_collection (Union[Unset, bool]): Filter results by column boolean value. Valid
            filter predicates are `eq`, `neq`.
        cert_services_collection (Union[Unset, bool]): Filter results by column boolean value.
            Valid filter predicates are `eq`, `neq`.
        ca_registry_collection (Union[Unset, bool]): Filter results by column boolean value. Valid
            filter predicates are `eq`, `neq`.
        dc_registry_collection (Union[Unset, bool]): Filter results by column boolean value. Valid
            filter predicates are `eq`, `neq`.
        ad_structure_collection (Union[Unset, bool]): Filter results by column boolean value.
            Valid filter predicates are `eq`, `neq`.
        domain_controller (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        status (Union[Unset, str]): Filter results by column string value. Valid filter predicates
            are `eq`, `neq`.
        event_title (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        client_id (Union[Unset, str]): Filter results by column string-formatted uuid value. Valid
            filter predicates are `eq`, `neq`.
        event_id (Union[Unset, int]): Filter results by column integer value. Valid filter
            predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        execution_time (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        start_time (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        end_time (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        last_ingest (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
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
        Response[Union[Any, ListClientFinishedJobsResponse200]]
    """

    kwargs = _get_kwargs(
        sort_by=sort_by,
        log_path=log_path,
        session_collection=session_collection,
        local_group_collection=local_group_collection,
        cert_services_collection=cert_services_collection,
        ca_registry_collection=ca_registry_collection,
        dc_registry_collection=dc_registry_collection,
        ad_structure_collection=ad_structure_collection,
        domain_controller=domain_controller,
        status=status,
        event_title=event_title,
        client_id=client_id,
        event_id=event_id,
        execution_time=execution_time,
        start_time=start_time,
        end_time=end_time,
        last_ingest=last_ingest,
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
    log_path: Union[Unset, str] = UNSET,
    session_collection: Union[Unset, bool] = UNSET,
    local_group_collection: Union[Unset, bool] = UNSET,
    cert_services_collection: Union[Unset, bool] = UNSET,
    ca_registry_collection: Union[Unset, bool] = UNSET,
    dc_registry_collection: Union[Unset, bool] = UNSET,
    ad_structure_collection: Union[Unset, bool] = UNSET,
    domain_controller: Union[Unset, str] = UNSET,
    status: Union[Unset, str] = UNSET,
    event_title: Union[Unset, str] = UNSET,
    client_id: Union[Unset, str] = UNSET,
    event_id: Union[Unset, int] = UNSET,
    execution_time: Union[Unset, datetime.datetime] = UNSET,
    start_time: Union[Unset, datetime.datetime] = UNSET,
    end_time: Union[Unset, datetime.datetime] = UNSET,
    last_ingest: Union[Unset, datetime.datetime] = UNSET,
    hydrate_domains: Union[Unset, bool] = True,
    hydrate_ous: Union[Unset, bool] = True,
    created_at: Union[Unset, datetime.datetime] = UNSET,
    updated_at: Union[Unset, datetime.datetime] = UNSET,
    deleted_at: Union[Unset, datetime.datetime] = UNSET,
    skip: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Optional[Union[Any, ListClientFinishedJobsResponse200]]:
    """List finished jobs

     Gets all finished jobs

    Args:
        sort_by (Union[Unset, str]): Sort by column. Can be used multiple times; prepend a hyphen
            for descending order.
            See parameter description for details about which columns are sortable.
        log_path (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        session_collection (Union[Unset, bool]): Filter results by column boolean value. Valid
            filter predicates are `eq`, `neq`.
        local_group_collection (Union[Unset, bool]): Filter results by column boolean value. Valid
            filter predicates are `eq`, `neq`.
        cert_services_collection (Union[Unset, bool]): Filter results by column boolean value.
            Valid filter predicates are `eq`, `neq`.
        ca_registry_collection (Union[Unset, bool]): Filter results by column boolean value. Valid
            filter predicates are `eq`, `neq`.
        dc_registry_collection (Union[Unset, bool]): Filter results by column boolean value. Valid
            filter predicates are `eq`, `neq`.
        ad_structure_collection (Union[Unset, bool]): Filter results by column boolean value.
            Valid filter predicates are `eq`, `neq`.
        domain_controller (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        status (Union[Unset, str]): Filter results by column string value. Valid filter predicates
            are `eq`, `neq`.
        event_title (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        client_id (Union[Unset, str]): Filter results by column string-formatted uuid value. Valid
            filter predicates are `eq`, `neq`.
        event_id (Union[Unset, int]): Filter results by column integer value. Valid filter
            predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        execution_time (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        start_time (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        end_time (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        last_ingest (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
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
        Union[Any, ListClientFinishedJobsResponse200]
    """

    return sync_detailed(
        client=client,
        sort_by=sort_by,
        log_path=log_path,
        session_collection=session_collection,
        local_group_collection=local_group_collection,
        cert_services_collection=cert_services_collection,
        ca_registry_collection=ca_registry_collection,
        dc_registry_collection=dc_registry_collection,
        ad_structure_collection=ad_structure_collection,
        domain_controller=domain_controller,
        status=status,
        event_title=event_title,
        client_id=client_id,
        event_id=event_id,
        execution_time=execution_time,
        start_time=start_time,
        end_time=end_time,
        last_ingest=last_ingest,
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
    log_path: Union[Unset, str] = UNSET,
    session_collection: Union[Unset, bool] = UNSET,
    local_group_collection: Union[Unset, bool] = UNSET,
    cert_services_collection: Union[Unset, bool] = UNSET,
    ca_registry_collection: Union[Unset, bool] = UNSET,
    dc_registry_collection: Union[Unset, bool] = UNSET,
    ad_structure_collection: Union[Unset, bool] = UNSET,
    domain_controller: Union[Unset, str] = UNSET,
    status: Union[Unset, str] = UNSET,
    event_title: Union[Unset, str] = UNSET,
    client_id: Union[Unset, str] = UNSET,
    event_id: Union[Unset, int] = UNSET,
    execution_time: Union[Unset, datetime.datetime] = UNSET,
    start_time: Union[Unset, datetime.datetime] = UNSET,
    end_time: Union[Unset, datetime.datetime] = UNSET,
    last_ingest: Union[Unset, datetime.datetime] = UNSET,
    hydrate_domains: Union[Unset, bool] = True,
    hydrate_ous: Union[Unset, bool] = True,
    created_at: Union[Unset, datetime.datetime] = UNSET,
    updated_at: Union[Unset, datetime.datetime] = UNSET,
    deleted_at: Union[Unset, datetime.datetime] = UNSET,
    skip: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Response[Union[Any, ListClientFinishedJobsResponse200]]:
    """List finished jobs

     Gets all finished jobs

    Args:
        sort_by (Union[Unset, str]): Sort by column. Can be used multiple times; prepend a hyphen
            for descending order.
            See parameter description for details about which columns are sortable.
        log_path (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        session_collection (Union[Unset, bool]): Filter results by column boolean value. Valid
            filter predicates are `eq`, `neq`.
        local_group_collection (Union[Unset, bool]): Filter results by column boolean value. Valid
            filter predicates are `eq`, `neq`.
        cert_services_collection (Union[Unset, bool]): Filter results by column boolean value.
            Valid filter predicates are `eq`, `neq`.
        ca_registry_collection (Union[Unset, bool]): Filter results by column boolean value. Valid
            filter predicates are `eq`, `neq`.
        dc_registry_collection (Union[Unset, bool]): Filter results by column boolean value. Valid
            filter predicates are `eq`, `neq`.
        ad_structure_collection (Union[Unset, bool]): Filter results by column boolean value.
            Valid filter predicates are `eq`, `neq`.
        domain_controller (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        status (Union[Unset, str]): Filter results by column string value. Valid filter predicates
            are `eq`, `neq`.
        event_title (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        client_id (Union[Unset, str]): Filter results by column string-formatted uuid value. Valid
            filter predicates are `eq`, `neq`.
        event_id (Union[Unset, int]): Filter results by column integer value. Valid filter
            predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        execution_time (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        start_time (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        end_time (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        last_ingest (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
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
        Response[Union[Any, ListClientFinishedJobsResponse200]]
    """

    kwargs = _get_kwargs(
        sort_by=sort_by,
        log_path=log_path,
        session_collection=session_collection,
        local_group_collection=local_group_collection,
        cert_services_collection=cert_services_collection,
        ca_registry_collection=ca_registry_collection,
        dc_registry_collection=dc_registry_collection,
        ad_structure_collection=ad_structure_collection,
        domain_controller=domain_controller,
        status=status,
        event_title=event_title,
        client_id=client_id,
        event_id=event_id,
        execution_time=execution_time,
        start_time=start_time,
        end_time=end_time,
        last_ingest=last_ingest,
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
    log_path: Union[Unset, str] = UNSET,
    session_collection: Union[Unset, bool] = UNSET,
    local_group_collection: Union[Unset, bool] = UNSET,
    cert_services_collection: Union[Unset, bool] = UNSET,
    ca_registry_collection: Union[Unset, bool] = UNSET,
    dc_registry_collection: Union[Unset, bool] = UNSET,
    ad_structure_collection: Union[Unset, bool] = UNSET,
    domain_controller: Union[Unset, str] = UNSET,
    status: Union[Unset, str] = UNSET,
    event_title: Union[Unset, str] = UNSET,
    client_id: Union[Unset, str] = UNSET,
    event_id: Union[Unset, int] = UNSET,
    execution_time: Union[Unset, datetime.datetime] = UNSET,
    start_time: Union[Unset, datetime.datetime] = UNSET,
    end_time: Union[Unset, datetime.datetime] = UNSET,
    last_ingest: Union[Unset, datetime.datetime] = UNSET,
    hydrate_domains: Union[Unset, bool] = True,
    hydrate_ous: Union[Unset, bool] = True,
    created_at: Union[Unset, datetime.datetime] = UNSET,
    updated_at: Union[Unset, datetime.datetime] = UNSET,
    deleted_at: Union[Unset, datetime.datetime] = UNSET,
    skip: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Optional[Union[Any, ListClientFinishedJobsResponse200]]:
    """List finished jobs

     Gets all finished jobs

    Args:
        sort_by (Union[Unset, str]): Sort by column. Can be used multiple times; prepend a hyphen
            for descending order.
            See parameter description for details about which columns are sortable.
        log_path (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        session_collection (Union[Unset, bool]): Filter results by column boolean value. Valid
            filter predicates are `eq`, `neq`.
        local_group_collection (Union[Unset, bool]): Filter results by column boolean value. Valid
            filter predicates are `eq`, `neq`.
        cert_services_collection (Union[Unset, bool]): Filter results by column boolean value.
            Valid filter predicates are `eq`, `neq`.
        ca_registry_collection (Union[Unset, bool]): Filter results by column boolean value. Valid
            filter predicates are `eq`, `neq`.
        dc_registry_collection (Union[Unset, bool]): Filter results by column boolean value. Valid
            filter predicates are `eq`, `neq`.
        ad_structure_collection (Union[Unset, bool]): Filter results by column boolean value.
            Valid filter predicates are `eq`, `neq`.
        domain_controller (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        status (Union[Unset, str]): Filter results by column string value. Valid filter predicates
            are `eq`, `neq`.
        event_title (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        client_id (Union[Unset, str]): Filter results by column string-formatted uuid value. Valid
            filter predicates are `eq`, `neq`.
        event_id (Union[Unset, int]): Filter results by column integer value. Valid filter
            predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        execution_time (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        start_time (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        end_time (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        last_ingest (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
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
        Union[Any, ListClientFinishedJobsResponse200]
    """

    return (
        await asyncio_detailed(
            client=client,
            sort_by=sort_by,
            log_path=log_path,
            session_collection=session_collection,
            local_group_collection=local_group_collection,
            cert_services_collection=cert_services_collection,
            ca_registry_collection=ca_registry_collection,
            dc_registry_collection=dc_registry_collection,
            ad_structure_collection=ad_structure_collection,
            domain_controller=domain_controller,
            status=status,
            event_title=event_title,
            client_id=client_id,
            event_id=event_id,
            execution_time=execution_time,
            start_time=start_time,
            end_time=end_time,
            last_ingest=last_ingest,
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
