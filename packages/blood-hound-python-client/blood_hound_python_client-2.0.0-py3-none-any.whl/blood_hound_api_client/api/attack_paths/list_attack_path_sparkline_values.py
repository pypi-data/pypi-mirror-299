import datetime
from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_attack_path_sparkline_values_response_200 import ListAttackPathSparklineValuesResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    domain_id: str,
    *,
    sort_by: Union[Unset, str] = UNSET,
    finding: str,
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    if not isinstance(prefer, Unset):
        headers["Prefer"] = str(prefer)

    params: Dict[str, Any] = {}

    params["sort_by"] = sort_by

    params["finding"] = finding

    json_from_: Union[Unset, str] = UNSET
    if not isinstance(from_, Unset):
        json_from_ = from_.isoformat()
    params["from"] = json_from_

    json_to: Union[Unset, str] = UNSET
    if not isinstance(to, Unset):
        json_to = to.isoformat()
    params["to"] = json_to

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/api/v2/domains/{domain_id}/sparkline",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, ListAttackPathSparklineValuesResponse200]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ListAttackPathSparklineValuesResponse200.from_dict(response.json())

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
) -> Response[Union[Any, ListAttackPathSparklineValuesResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    domain_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    sort_by: Union[Unset, str] = UNSET,
    finding: str,
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Response[Union[Any, ListAttackPathSparklineValuesResponse200]]:
    """List attack path sparkline values

     List the values that represent the sparklines for individual attack paths

    Args:
        domain_id (str):
        sort_by (Union[Unset, str]): Sort by column. Can be used multiple times; prepend a hyphen
            for descending order.
            See parameter description for details about which columns are sortable.
        finding (str): Filter results by column string value. Valid filter predicates are `eq`,
            `neq`.
        from_ (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        to (Union[Unset, datetime.datetime]): Filter results by column timestamp value formatted
            as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        prefer (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ListAttackPathSparklineValuesResponse200]]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
        sort_by=sort_by,
        finding=finding,
        from_=from_,
        to=to,
        prefer=prefer,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    domain_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    sort_by: Union[Unset, str] = UNSET,
    finding: str,
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Optional[Union[Any, ListAttackPathSparklineValuesResponse200]]:
    """List attack path sparkline values

     List the values that represent the sparklines for individual attack paths

    Args:
        domain_id (str):
        sort_by (Union[Unset, str]): Sort by column. Can be used multiple times; prepend a hyphen
            for descending order.
            See parameter description for details about which columns are sortable.
        finding (str): Filter results by column string value. Valid filter predicates are `eq`,
            `neq`.
        from_ (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        to (Union[Unset, datetime.datetime]): Filter results by column timestamp value formatted
            as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        prefer (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ListAttackPathSparklineValuesResponse200]
    """

    return sync_detailed(
        domain_id=domain_id,
        client=client,
        sort_by=sort_by,
        finding=finding,
        from_=from_,
        to=to,
        prefer=prefer,
    ).parsed


async def asyncio_detailed(
    domain_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    sort_by: Union[Unset, str] = UNSET,
    finding: str,
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Response[Union[Any, ListAttackPathSparklineValuesResponse200]]:
    """List attack path sparkline values

     List the values that represent the sparklines for individual attack paths

    Args:
        domain_id (str):
        sort_by (Union[Unset, str]): Sort by column. Can be used multiple times; prepend a hyphen
            for descending order.
            See parameter description for details about which columns are sortable.
        finding (str): Filter results by column string value. Valid filter predicates are `eq`,
            `neq`.
        from_ (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        to (Union[Unset, datetime.datetime]): Filter results by column timestamp value formatted
            as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        prefer (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ListAttackPathSparklineValuesResponse200]]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
        sort_by=sort_by,
        finding=finding,
        from_=from_,
        to=to,
        prefer=prefer,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    domain_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    sort_by: Union[Unset, str] = UNSET,
    finding: str,
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Optional[Union[Any, ListAttackPathSparklineValuesResponse200]]:
    """List attack path sparkline values

     List the values that represent the sparklines for individual attack paths

    Args:
        domain_id (str):
        sort_by (Union[Unset, str]): Sort by column. Can be used multiple times; prepend a hyphen
            for descending order.
            See parameter description for details about which columns are sortable.
        finding (str): Filter results by column string value. Valid filter predicates are `eq`,
            `neq`.
        from_ (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        to (Union[Unset, datetime.datetime]): Filter results by column timestamp value formatted
            as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        prefer (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ListAttackPathSparklineValuesResponse200]
    """

    return (
        await asyncio_detailed(
            domain_id=domain_id,
            client=client,
            sort_by=sort_by,
            finding=finding,
            from_=from_,
            to=to,
            prefer=prefer,
        )
    ).parsed
