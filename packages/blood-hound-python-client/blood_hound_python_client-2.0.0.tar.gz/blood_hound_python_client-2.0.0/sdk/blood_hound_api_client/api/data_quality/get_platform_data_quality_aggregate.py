import datetime
from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_response_data_quality_platform_aggregate import ApiResponseDataQualityPlatformAggregate
from ...models.get_platform_data_quality_aggregate_platform_id import GetPlatformDataQualityAggregatePlatformId
from ...types import UNSET, Response, Unset


def _get_kwargs(
    platform_id: GetPlatformDataQualityAggregatePlatformId,
    *,
    sort_by: Union[Unset, str] = UNSET,
    start: Union[Unset, datetime.datetime] = UNSET,
    end: Union[Unset, datetime.datetime] = UNSET,
    skip: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    if not isinstance(prefer, Unset):
        headers["Prefer"] = str(prefer)

    params: Dict[str, Any] = {}

    params["sort_by"] = sort_by

    json_start: Union[Unset, str] = UNSET
    if not isinstance(start, Unset):
        json_start = start.isoformat()
    params["start"] = json_start

    json_end: Union[Unset, str] = UNSET
    if not isinstance(end, Unset):
        json_end = end.isoformat()
    params["end"] = json_end

    params["skip"] = skip

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/api/v2/platform/{platform_id}/data-quality-stats",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, ApiResponseDataQualityPlatformAggregate]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ApiResponseDataQualityPlatformAggregate.from_dict(response.json())

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
) -> Response[Union[Any, ApiResponseDataQualityPlatformAggregate]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    platform_id: GetPlatformDataQualityAggregatePlatformId,
    *,
    client: Union[AuthenticatedClient, Client],
    sort_by: Union[Unset, str] = UNSET,
    start: Union[Unset, datetime.datetime] = UNSET,
    end: Union[Unset, datetime.datetime] = UNSET,
    skip: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Response[Union[Any, ApiResponseDataQualityPlatformAggregate]]:
    """Get platform data quality aggregate

     Time series list of aggregate data quality stats for a given platform

    Args:
        platform_id (GetPlatformDataQualityAggregatePlatformId):
        sort_by (Union[Unset, str]): Sort by column. Can be used multiple times; prepend a hyphen
            for descending order.
            See parameter description for details about which columns are sortable.
        start (Union[Unset, datetime.datetime]):
        end (Union[Unset, datetime.datetime]):
        skip (Union[Unset, int]): The number of items to skip in a paginated response.
        limit (Union[Unset, int]): The limit of results requested by the client.
        prefer (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ApiResponseDataQualityPlatformAggregate]]
    """

    kwargs = _get_kwargs(
        platform_id=platform_id,
        sort_by=sort_by,
        start=start,
        end=end,
        skip=skip,
        limit=limit,
        prefer=prefer,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    platform_id: GetPlatformDataQualityAggregatePlatformId,
    *,
    client: Union[AuthenticatedClient, Client],
    sort_by: Union[Unset, str] = UNSET,
    start: Union[Unset, datetime.datetime] = UNSET,
    end: Union[Unset, datetime.datetime] = UNSET,
    skip: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Optional[Union[Any, ApiResponseDataQualityPlatformAggregate]]:
    """Get platform data quality aggregate

     Time series list of aggregate data quality stats for a given platform

    Args:
        platform_id (GetPlatformDataQualityAggregatePlatformId):
        sort_by (Union[Unset, str]): Sort by column. Can be used multiple times; prepend a hyphen
            for descending order.
            See parameter description for details about which columns are sortable.
        start (Union[Unset, datetime.datetime]):
        end (Union[Unset, datetime.datetime]):
        skip (Union[Unset, int]): The number of items to skip in a paginated response.
        limit (Union[Unset, int]): The limit of results requested by the client.
        prefer (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ApiResponseDataQualityPlatformAggregate]
    """

    return sync_detailed(
        platform_id=platform_id,
        client=client,
        sort_by=sort_by,
        start=start,
        end=end,
        skip=skip,
        limit=limit,
        prefer=prefer,
    ).parsed


async def asyncio_detailed(
    platform_id: GetPlatformDataQualityAggregatePlatformId,
    *,
    client: Union[AuthenticatedClient, Client],
    sort_by: Union[Unset, str] = UNSET,
    start: Union[Unset, datetime.datetime] = UNSET,
    end: Union[Unset, datetime.datetime] = UNSET,
    skip: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Response[Union[Any, ApiResponseDataQualityPlatformAggregate]]:
    """Get platform data quality aggregate

     Time series list of aggregate data quality stats for a given platform

    Args:
        platform_id (GetPlatformDataQualityAggregatePlatformId):
        sort_by (Union[Unset, str]): Sort by column. Can be used multiple times; prepend a hyphen
            for descending order.
            See parameter description for details about which columns are sortable.
        start (Union[Unset, datetime.datetime]):
        end (Union[Unset, datetime.datetime]):
        skip (Union[Unset, int]): The number of items to skip in a paginated response.
        limit (Union[Unset, int]): The limit of results requested by the client.
        prefer (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ApiResponseDataQualityPlatformAggregate]]
    """

    kwargs = _get_kwargs(
        platform_id=platform_id,
        sort_by=sort_by,
        start=start,
        end=end,
        skip=skip,
        limit=limit,
        prefer=prefer,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    platform_id: GetPlatformDataQualityAggregatePlatformId,
    *,
    client: Union[AuthenticatedClient, Client],
    sort_by: Union[Unset, str] = UNSET,
    start: Union[Unset, datetime.datetime] = UNSET,
    end: Union[Unset, datetime.datetime] = UNSET,
    skip: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Optional[Union[Any, ApiResponseDataQualityPlatformAggregate]]:
    """Get platform data quality aggregate

     Time series list of aggregate data quality stats for a given platform

    Args:
        platform_id (GetPlatformDataQualityAggregatePlatformId):
        sort_by (Union[Unset, str]): Sort by column. Can be used multiple times; prepend a hyphen
            for descending order.
            See parameter description for details about which columns are sortable.
        start (Union[Unset, datetime.datetime]):
        end (Union[Unset, datetime.datetime]):
        skip (Union[Unset, int]): The number of items to skip in a paginated response.
        limit (Union[Unset, int]): The limit of results requested by the client.
        prefer (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ApiResponseDataQualityPlatformAggregate]
    """

    return (
        await asyncio_detailed(
            platform_id=platform_id,
            client=client,
            sort_by=sort_by,
            start=start,
            end=end,
            skip=skip,
            limit=limit,
            prefer=prefer,
        )
    ).parsed
