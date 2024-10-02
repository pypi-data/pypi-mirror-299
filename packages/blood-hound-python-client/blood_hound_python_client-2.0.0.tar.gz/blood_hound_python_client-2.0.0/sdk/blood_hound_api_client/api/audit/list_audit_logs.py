import datetime
from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_audit_logs_response_200 import ListAuditLogsResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    skip: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    created_at: Union[Unset, datetime.datetime] = UNSET,
    sort_by: Union[Unset, str] = UNSET,
    before: Union[Unset, datetime.datetime] = UNSET,
    after: Union[Unset, datetime.datetime] = UNSET,
    id: Union[Unset, str] = UNSET,
    actor_id: Union[Unset, str] = UNSET,
    actor_name: Union[Unset, str] = UNSET,
    actor_email: Union[Unset, str] = UNSET,
    action: Union[Unset, str] = UNSET,
    request_id: Union[Unset, str] = UNSET,
    source: Union[Unset, str] = UNSET,
    status: Union[Unset, str] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    if not isinstance(prefer, Unset):
        headers["Prefer"] = str(prefer)

    params: Dict[str, Any] = {}

    params["skip"] = skip

    params["limit"] = limit

    json_created_at: Union[Unset, str] = UNSET
    if not isinstance(created_at, Unset):
        json_created_at = created_at.isoformat()
    params["created_at"] = json_created_at

    params["sort_by"] = sort_by

    json_before: Union[Unset, str] = UNSET
    if not isinstance(before, Unset):
        json_before = before.isoformat()
    params["before"] = json_before

    json_after: Union[Unset, str] = UNSET
    if not isinstance(after, Unset):
        json_after = after.isoformat()
    params["after"] = json_after

    params["id"] = id

    params["actor_id"] = actor_id

    params["actor_name"] = actor_name

    params["actor_email"] = actor_email

    params["action"] = action

    params["request_id"] = request_id

    params["source"] = source

    params["status"] = status

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/api/v2/audit",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, ListAuditLogsResponse200]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ListAuditLogsResponse200.from_dict(response.json())

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
) -> Response[Union[Any, ListAuditLogsResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    skip: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    created_at: Union[Unset, datetime.datetime] = UNSET,
    sort_by: Union[Unset, str] = UNSET,
    before: Union[Unset, datetime.datetime] = UNSET,
    after: Union[Unset, datetime.datetime] = UNSET,
    id: Union[Unset, str] = UNSET,
    actor_id: Union[Unset, str] = UNSET,
    actor_name: Union[Unset, str] = UNSET,
    actor_email: Union[Unset, str] = UNSET,
    action: Union[Unset, str] = UNSET,
    request_id: Union[Unset, str] = UNSET,
    source: Union[Unset, str] = UNSET,
    status: Union[Unset, str] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Response[Union[Any, ListAuditLogsResponse200]]:
    """List audit logs

     Returns a list of audit logs.

    Args:
        skip (Union[Unset, int]): The number of items to skip in a paginated response.
        limit (Union[Unset, int]): The limit of results requested by the client.
        created_at (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        sort_by (Union[Unset, str]): Sort by column. Can be used multiple times; prepend a hyphen
            for descending order.
            See parameter description for details about which columns are sortable.
        before (Union[Unset, datetime.datetime]):
        after (Union[Unset, datetime.datetime]):
        id (Union[Unset, str]): Filter results by column string value. Valid filter predicates are
            `eq`, `neq`.
        actor_id (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        actor_name (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        actor_email (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        action (Union[Unset, str]): Filter results by column string value. Valid filter predicates
            are `eq`, `neq`.
        request_id (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        source (Union[Unset, str]): Filter results by column string value. Valid filter predicates
            are `eq`, `neq`.
        status (Union[Unset, str]): Filter results by column string value. Valid filter predicates
            are `eq`, `neq`.
        prefer (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ListAuditLogsResponse200]]
    """

    kwargs = _get_kwargs(
        skip=skip,
        limit=limit,
        created_at=created_at,
        sort_by=sort_by,
        before=before,
        after=after,
        id=id,
        actor_id=actor_id,
        actor_name=actor_name,
        actor_email=actor_email,
        action=action,
        request_id=request_id,
        source=source,
        status=status,
        prefer=prefer,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    skip: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    created_at: Union[Unset, datetime.datetime] = UNSET,
    sort_by: Union[Unset, str] = UNSET,
    before: Union[Unset, datetime.datetime] = UNSET,
    after: Union[Unset, datetime.datetime] = UNSET,
    id: Union[Unset, str] = UNSET,
    actor_id: Union[Unset, str] = UNSET,
    actor_name: Union[Unset, str] = UNSET,
    actor_email: Union[Unset, str] = UNSET,
    action: Union[Unset, str] = UNSET,
    request_id: Union[Unset, str] = UNSET,
    source: Union[Unset, str] = UNSET,
    status: Union[Unset, str] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Optional[Union[Any, ListAuditLogsResponse200]]:
    """List audit logs

     Returns a list of audit logs.

    Args:
        skip (Union[Unset, int]): The number of items to skip in a paginated response.
        limit (Union[Unset, int]): The limit of results requested by the client.
        created_at (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        sort_by (Union[Unset, str]): Sort by column. Can be used multiple times; prepend a hyphen
            for descending order.
            See parameter description for details about which columns are sortable.
        before (Union[Unset, datetime.datetime]):
        after (Union[Unset, datetime.datetime]):
        id (Union[Unset, str]): Filter results by column string value. Valid filter predicates are
            `eq`, `neq`.
        actor_id (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        actor_name (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        actor_email (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        action (Union[Unset, str]): Filter results by column string value. Valid filter predicates
            are `eq`, `neq`.
        request_id (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        source (Union[Unset, str]): Filter results by column string value. Valid filter predicates
            are `eq`, `neq`.
        status (Union[Unset, str]): Filter results by column string value. Valid filter predicates
            are `eq`, `neq`.
        prefer (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ListAuditLogsResponse200]
    """

    return sync_detailed(
        client=client,
        skip=skip,
        limit=limit,
        created_at=created_at,
        sort_by=sort_by,
        before=before,
        after=after,
        id=id,
        actor_id=actor_id,
        actor_name=actor_name,
        actor_email=actor_email,
        action=action,
        request_id=request_id,
        source=source,
        status=status,
        prefer=prefer,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    skip: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    created_at: Union[Unset, datetime.datetime] = UNSET,
    sort_by: Union[Unset, str] = UNSET,
    before: Union[Unset, datetime.datetime] = UNSET,
    after: Union[Unset, datetime.datetime] = UNSET,
    id: Union[Unset, str] = UNSET,
    actor_id: Union[Unset, str] = UNSET,
    actor_name: Union[Unset, str] = UNSET,
    actor_email: Union[Unset, str] = UNSET,
    action: Union[Unset, str] = UNSET,
    request_id: Union[Unset, str] = UNSET,
    source: Union[Unset, str] = UNSET,
    status: Union[Unset, str] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Response[Union[Any, ListAuditLogsResponse200]]:
    """List audit logs

     Returns a list of audit logs.

    Args:
        skip (Union[Unset, int]): The number of items to skip in a paginated response.
        limit (Union[Unset, int]): The limit of results requested by the client.
        created_at (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        sort_by (Union[Unset, str]): Sort by column. Can be used multiple times; prepend a hyphen
            for descending order.
            See parameter description for details about which columns are sortable.
        before (Union[Unset, datetime.datetime]):
        after (Union[Unset, datetime.datetime]):
        id (Union[Unset, str]): Filter results by column string value. Valid filter predicates are
            `eq`, `neq`.
        actor_id (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        actor_name (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        actor_email (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        action (Union[Unset, str]): Filter results by column string value. Valid filter predicates
            are `eq`, `neq`.
        request_id (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        source (Union[Unset, str]): Filter results by column string value. Valid filter predicates
            are `eq`, `neq`.
        status (Union[Unset, str]): Filter results by column string value. Valid filter predicates
            are `eq`, `neq`.
        prefer (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ListAuditLogsResponse200]]
    """

    kwargs = _get_kwargs(
        skip=skip,
        limit=limit,
        created_at=created_at,
        sort_by=sort_by,
        before=before,
        after=after,
        id=id,
        actor_id=actor_id,
        actor_name=actor_name,
        actor_email=actor_email,
        action=action,
        request_id=request_id,
        source=source,
        status=status,
        prefer=prefer,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    skip: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    created_at: Union[Unset, datetime.datetime] = UNSET,
    sort_by: Union[Unset, str] = UNSET,
    before: Union[Unset, datetime.datetime] = UNSET,
    after: Union[Unset, datetime.datetime] = UNSET,
    id: Union[Unset, str] = UNSET,
    actor_id: Union[Unset, str] = UNSET,
    actor_name: Union[Unset, str] = UNSET,
    actor_email: Union[Unset, str] = UNSET,
    action: Union[Unset, str] = UNSET,
    request_id: Union[Unset, str] = UNSET,
    source: Union[Unset, str] = UNSET,
    status: Union[Unset, str] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Optional[Union[Any, ListAuditLogsResponse200]]:
    """List audit logs

     Returns a list of audit logs.

    Args:
        skip (Union[Unset, int]): The number of items to skip in a paginated response.
        limit (Union[Unset, int]): The limit of results requested by the client.
        created_at (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        sort_by (Union[Unset, str]): Sort by column. Can be used multiple times; prepend a hyphen
            for descending order.
            See parameter description for details about which columns are sortable.
        before (Union[Unset, datetime.datetime]):
        after (Union[Unset, datetime.datetime]):
        id (Union[Unset, str]): Filter results by column string value. Valid filter predicates are
            `eq`, `neq`.
        actor_id (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        actor_name (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        actor_email (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        action (Union[Unset, str]): Filter results by column string value. Valid filter predicates
            are `eq`, `neq`.
        request_id (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        source (Union[Unset, str]): Filter results by column string value. Valid filter predicates
            are `eq`, `neq`.
        status (Union[Unset, str]): Filter results by column string value. Valid filter predicates
            are `eq`, `neq`.
        prefer (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ListAuditLogsResponse200]
    """

    return (
        await asyncio_detailed(
            client=client,
            skip=skip,
            limit=limit,
            created_at=created_at,
            sort_by=sort_by,
            before=before,
            after=after,
            id=id,
            actor_id=actor_id,
            actor_name=actor_name,
            actor_email=actor_email,
            action=action,
            request_id=request_id,
            source=source,
            status=status,
            prefer=prefer,
        )
    ).parsed
