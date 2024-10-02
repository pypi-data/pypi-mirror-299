import datetime
from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_posture_stats_response_200 import GetPostureStatsResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    sort_by: Union[Unset, str] = UNSET,
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
    domain_sid: Union[Unset, str] = UNSET,
    exposure_index: Union[Unset, int] = UNSET,
    tier_zero_count: Union[Unset, int] = UNSET,
    critical_risk_count: Union[Unset, int] = UNSET,
    id: Union[Unset, int] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    if not isinstance(prefer, Unset):
        headers["Prefer"] = str(prefer)

    params: Dict[str, Any] = {}

    params["sort_by"] = sort_by

    json_from_: Union[Unset, str] = UNSET
    if not isinstance(from_, Unset):
        json_from_ = from_.isoformat()
    params["from"] = json_from_

    json_to: Union[Unset, str] = UNSET
    if not isinstance(to, Unset):
        json_to = to.isoformat()
    params["to"] = json_to

    params["domain_sid"] = domain_sid

    params["exposure_index"] = exposure_index

    params["tier_zero_count"] = tier_zero_count

    params["critical_risk_count"] = critical_risk_count

    params["id"] = id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/api/v2/posture-stats",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, GetPostureStatsResponse200]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetPostureStatsResponse200.from_dict(response.json())

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
) -> Response[Union[Any, GetPostureStatsResponse200]]:
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
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
    domain_sid: Union[Unset, str] = UNSET,
    exposure_index: Union[Unset, int] = UNSET,
    tier_zero_count: Union[Unset, int] = UNSET,
    critical_risk_count: Union[Unset, int] = UNSET,
    id: Union[Unset, int] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Response[Union[Any, GetPostureStatsResponse200]]:
    """Get Posture Statistics

     Gets the history of database stats saved in the database

    Args:
        sort_by (Union[Unset, str]): Sort by column. Can be used multiple times; prepend a hyphen
            for descending order.
            See parameter description for details about which columns are sortable.
        from_ (Union[Unset, datetime.datetime]):
        to (Union[Unset, datetime.datetime]):
        domain_sid (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        exposure_index (Union[Unset, int]): Filter results by column integer value. Valid filter
            predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        tier_zero_count (Union[Unset, int]): Filter results by column integer value. Valid filter
            predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        critical_risk_count (Union[Unset, int]): Filter results by column integer value. Valid
            filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        id (Union[Unset, int]): Filter results by column integer value. Valid filter predicates
            are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        prefer (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, GetPostureStatsResponse200]]
    """

    kwargs = _get_kwargs(
        sort_by=sort_by,
        from_=from_,
        to=to,
        domain_sid=domain_sid,
        exposure_index=exposure_index,
        tier_zero_count=tier_zero_count,
        critical_risk_count=critical_risk_count,
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
    sort_by: Union[Unset, str] = UNSET,
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
    domain_sid: Union[Unset, str] = UNSET,
    exposure_index: Union[Unset, int] = UNSET,
    tier_zero_count: Union[Unset, int] = UNSET,
    critical_risk_count: Union[Unset, int] = UNSET,
    id: Union[Unset, int] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Optional[Union[Any, GetPostureStatsResponse200]]:
    """Get Posture Statistics

     Gets the history of database stats saved in the database

    Args:
        sort_by (Union[Unset, str]): Sort by column. Can be used multiple times; prepend a hyphen
            for descending order.
            See parameter description for details about which columns are sortable.
        from_ (Union[Unset, datetime.datetime]):
        to (Union[Unset, datetime.datetime]):
        domain_sid (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        exposure_index (Union[Unset, int]): Filter results by column integer value. Valid filter
            predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        tier_zero_count (Union[Unset, int]): Filter results by column integer value. Valid filter
            predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        critical_risk_count (Union[Unset, int]): Filter results by column integer value. Valid
            filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        id (Union[Unset, int]): Filter results by column integer value. Valid filter predicates
            are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        prefer (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, GetPostureStatsResponse200]
    """

    return sync_detailed(
        client=client,
        sort_by=sort_by,
        from_=from_,
        to=to,
        domain_sid=domain_sid,
        exposure_index=exposure_index,
        tier_zero_count=tier_zero_count,
        critical_risk_count=critical_risk_count,
        id=id,
        prefer=prefer,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    sort_by: Union[Unset, str] = UNSET,
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
    domain_sid: Union[Unset, str] = UNSET,
    exposure_index: Union[Unset, int] = UNSET,
    tier_zero_count: Union[Unset, int] = UNSET,
    critical_risk_count: Union[Unset, int] = UNSET,
    id: Union[Unset, int] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Response[Union[Any, GetPostureStatsResponse200]]:
    """Get Posture Statistics

     Gets the history of database stats saved in the database

    Args:
        sort_by (Union[Unset, str]): Sort by column. Can be used multiple times; prepend a hyphen
            for descending order.
            See parameter description for details about which columns are sortable.
        from_ (Union[Unset, datetime.datetime]):
        to (Union[Unset, datetime.datetime]):
        domain_sid (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        exposure_index (Union[Unset, int]): Filter results by column integer value. Valid filter
            predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        tier_zero_count (Union[Unset, int]): Filter results by column integer value. Valid filter
            predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        critical_risk_count (Union[Unset, int]): Filter results by column integer value. Valid
            filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        id (Union[Unset, int]): Filter results by column integer value. Valid filter predicates
            are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        prefer (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, GetPostureStatsResponse200]]
    """

    kwargs = _get_kwargs(
        sort_by=sort_by,
        from_=from_,
        to=to,
        domain_sid=domain_sid,
        exposure_index=exposure_index,
        tier_zero_count=tier_zero_count,
        critical_risk_count=critical_risk_count,
        id=id,
        prefer=prefer,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    sort_by: Union[Unset, str] = UNSET,
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
    domain_sid: Union[Unset, str] = UNSET,
    exposure_index: Union[Unset, int] = UNSET,
    tier_zero_count: Union[Unset, int] = UNSET,
    critical_risk_count: Union[Unset, int] = UNSET,
    id: Union[Unset, int] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Optional[Union[Any, GetPostureStatsResponse200]]:
    """Get Posture Statistics

     Gets the history of database stats saved in the database

    Args:
        sort_by (Union[Unset, str]): Sort by column. Can be used multiple times; prepend a hyphen
            for descending order.
            See parameter description for details about which columns are sortable.
        from_ (Union[Unset, datetime.datetime]):
        to (Union[Unset, datetime.datetime]):
        domain_sid (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        exposure_index (Union[Unset, int]): Filter results by column integer value. Valid filter
            predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        tier_zero_count (Union[Unset, int]): Filter results by column integer value. Valid filter
            predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        critical_risk_count (Union[Unset, int]): Filter results by column integer value. Valid
            filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        id (Union[Unset, int]): Filter results by column integer value. Valid filter predicates
            are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        prefer (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, GetPostureStatsResponse200]
    """

    return (
        await asyncio_detailed(
            client=client,
            sort_by=sort_by,
            from_=from_,
            to=to,
            domain_sid=domain_sid,
            exposure_index=exposure_index,
            tier_zero_count=tier_zero_count,
            critical_risk_count=critical_risk_count,
            id=id,
            prefer=prefer,
        )
    ).parsed
