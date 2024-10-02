import datetime
from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_auth_tokens_response_200 import ListAuthTokensResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    user_id: Union[Unset, str] = UNSET,
    sort_by: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    key: Union[Unset, str] = UNSET,
    hmac_method: Union[Unset, str] = UNSET,
    last_access: Union[Unset, datetime.datetime] = UNSET,
    id: Union[Unset, str] = UNSET,
    created_at: Union[Unset, datetime.datetime] = UNSET,
    updated_at: Union[Unset, datetime.datetime] = UNSET,
    deleted_at: Union[Unset, datetime.datetime] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    if not isinstance(prefer, Unset):
        headers["Prefer"] = str(prefer)

    params: Dict[str, Any] = {}

    params["user_id"] = user_id

    params["sort_by"] = sort_by

    params["name"] = name

    params["key"] = key

    params["hmac_method"] = hmac_method

    json_last_access: Union[Unset, str] = UNSET
    if not isinstance(last_access, Unset):
        json_last_access = last_access.isoformat()
    params["last_access"] = json_last_access

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
        "url": "/api/v2/tokens",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, ListAuthTokensResponse200]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ListAuthTokensResponse200.from_dict(response.json())

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
) -> Response[Union[Any, ListAuthTokensResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    user_id: Union[Unset, str] = UNSET,
    sort_by: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    key: Union[Unset, str] = UNSET,
    hmac_method: Union[Unset, str] = UNSET,
    last_access: Union[Unset, datetime.datetime] = UNSET,
    id: Union[Unset, str] = UNSET,
    created_at: Union[Unset, datetime.datetime] = UNSET,
    updated_at: Union[Unset, datetime.datetime] = UNSET,
    deleted_at: Union[Unset, datetime.datetime] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Response[Union[Any, ListAuthTokensResponse200]]:
    """List Auth Tokens

     Get all auth tokens.

    Args:
        user_id (Union[Unset, str]): Filter results by column string-formatted uuid value. Valid
            filter predicates are `eq`, `neq`.
        sort_by (Union[Unset, str]): Sort by column. Can be used multiple times; prepend a hyphen
            for descending order.
            See parameter description for details about which columns are sortable.
        name (Union[Unset, str]): Filter results by column string value. Valid filter predicates
            are `eq`, `neq`.
        key (Union[Unset, str]): Filter results by column string value. Valid filter predicates
            are `eq`, `neq`.
        hmac_method (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        last_access (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        id (Union[Unset, str]): Filter results by column string-formatted uuid value. Valid filter
            predicates are `eq`, `neq`.
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
        Response[Union[Any, ListAuthTokensResponse200]]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        sort_by=sort_by,
        name=name,
        key=key,
        hmac_method=hmac_method,
        last_access=last_access,
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
    user_id: Union[Unset, str] = UNSET,
    sort_by: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    key: Union[Unset, str] = UNSET,
    hmac_method: Union[Unset, str] = UNSET,
    last_access: Union[Unset, datetime.datetime] = UNSET,
    id: Union[Unset, str] = UNSET,
    created_at: Union[Unset, datetime.datetime] = UNSET,
    updated_at: Union[Unset, datetime.datetime] = UNSET,
    deleted_at: Union[Unset, datetime.datetime] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Optional[Union[Any, ListAuthTokensResponse200]]:
    """List Auth Tokens

     Get all auth tokens.

    Args:
        user_id (Union[Unset, str]): Filter results by column string-formatted uuid value. Valid
            filter predicates are `eq`, `neq`.
        sort_by (Union[Unset, str]): Sort by column. Can be used multiple times; prepend a hyphen
            for descending order.
            See parameter description for details about which columns are sortable.
        name (Union[Unset, str]): Filter results by column string value. Valid filter predicates
            are `eq`, `neq`.
        key (Union[Unset, str]): Filter results by column string value. Valid filter predicates
            are `eq`, `neq`.
        hmac_method (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        last_access (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        id (Union[Unset, str]): Filter results by column string-formatted uuid value. Valid filter
            predicates are `eq`, `neq`.
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
        Union[Any, ListAuthTokensResponse200]
    """

    return sync_detailed(
        client=client,
        user_id=user_id,
        sort_by=sort_by,
        name=name,
        key=key,
        hmac_method=hmac_method,
        last_access=last_access,
        id=id,
        created_at=created_at,
        updated_at=updated_at,
        deleted_at=deleted_at,
        prefer=prefer,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    user_id: Union[Unset, str] = UNSET,
    sort_by: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    key: Union[Unset, str] = UNSET,
    hmac_method: Union[Unset, str] = UNSET,
    last_access: Union[Unset, datetime.datetime] = UNSET,
    id: Union[Unset, str] = UNSET,
    created_at: Union[Unset, datetime.datetime] = UNSET,
    updated_at: Union[Unset, datetime.datetime] = UNSET,
    deleted_at: Union[Unset, datetime.datetime] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Response[Union[Any, ListAuthTokensResponse200]]:
    """List Auth Tokens

     Get all auth tokens.

    Args:
        user_id (Union[Unset, str]): Filter results by column string-formatted uuid value. Valid
            filter predicates are `eq`, `neq`.
        sort_by (Union[Unset, str]): Sort by column. Can be used multiple times; prepend a hyphen
            for descending order.
            See parameter description for details about which columns are sortable.
        name (Union[Unset, str]): Filter results by column string value. Valid filter predicates
            are `eq`, `neq`.
        key (Union[Unset, str]): Filter results by column string value. Valid filter predicates
            are `eq`, `neq`.
        hmac_method (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        last_access (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        id (Union[Unset, str]): Filter results by column string-formatted uuid value. Valid filter
            predicates are `eq`, `neq`.
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
        Response[Union[Any, ListAuthTokensResponse200]]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        sort_by=sort_by,
        name=name,
        key=key,
        hmac_method=hmac_method,
        last_access=last_access,
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
    user_id: Union[Unset, str] = UNSET,
    sort_by: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    key: Union[Unset, str] = UNSET,
    hmac_method: Union[Unset, str] = UNSET,
    last_access: Union[Unset, datetime.datetime] = UNSET,
    id: Union[Unset, str] = UNSET,
    created_at: Union[Unset, datetime.datetime] = UNSET,
    updated_at: Union[Unset, datetime.datetime] = UNSET,
    deleted_at: Union[Unset, datetime.datetime] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Optional[Union[Any, ListAuthTokensResponse200]]:
    """List Auth Tokens

     Get all auth tokens.

    Args:
        user_id (Union[Unset, str]): Filter results by column string-formatted uuid value. Valid
            filter predicates are `eq`, `neq`.
        sort_by (Union[Unset, str]): Sort by column. Can be used multiple times; prepend a hyphen
            for descending order.
            See parameter description for details about which columns are sortable.
        name (Union[Unset, str]): Filter results by column string value. Valid filter predicates
            are `eq`, `neq`.
        key (Union[Unset, str]): Filter results by column string value. Valid filter predicates
            are `eq`, `neq`.
        hmac_method (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        last_access (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        id (Union[Unset, str]): Filter results by column string-formatted uuid value. Valid filter
            predicates are `eq`, `neq`.
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
        Union[Any, ListAuthTokensResponse200]
    """

    return (
        await asyncio_detailed(
            client=client,
            user_id=user_id,
            sort_by=sort_by,
            name=name,
            key=key,
            hmac_method=hmac_method,
            last_access=last_access,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            deleted_at=deleted_at,
            prefer=prefer,
        )
    ).parsed
