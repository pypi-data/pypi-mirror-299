from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_saved_queries_response_200 import ListSavedQueriesResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    skip: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    sort_by: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    query: Union[Unset, str] = UNSET,
    user_id: Union[Unset, str] = UNSET,
    scope: Union[Unset, str] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    if not isinstance(prefer, Unset):
        headers["Prefer"] = str(prefer)

    params: Dict[str, Any] = {}

    params["skip"] = skip

    params["limit"] = limit

    params["sort_by"] = sort_by

    params["name"] = name

    params["query"] = query

    params["user_id"] = user_id

    params["scope"] = scope

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/api/v2/saved-queries",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, ListSavedQueriesResponse200]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ListSavedQueriesResponse200.from_dict(response.json())

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
) -> Response[Union[Any, ListSavedQueriesResponse200]]:
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
    sort_by: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    query: Union[Unset, str] = UNSET,
    user_id: Union[Unset, str] = UNSET,
    scope: Union[Unset, str] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Response[Union[Any, ListSavedQueriesResponse200]]:
    """List saved queries

     Get all saved queries for the current user

    Args:
        skip (Union[Unset, int]): The number of items to skip in a paginated response.
        limit (Union[Unset, int]): The limit of results requested by the client.
        sort_by (Union[Unset, str]): Sort by column. Can be used multiple times; prepend a hyphen
            for descending order.
            See parameter description for details about which columns are sortable.
        name (Union[Unset, str]): Filter results by column string value. Valid filter predicates
            are `eq`, `neq`.
        query (Union[Unset, str]): Filter results by column string value. Valid filter predicates
            are `eq`, `neq`.
        user_id (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        scope (Union[Unset, str]): The contains predicate checks a property against the values in
            a given comma separated list.
            - `in` checks if the property matches an element in the given comma separated list.
              - `in:Contains,GetChangesAll,MemberOf`
            - `nin` checks if the property does not match an element in the given comma separated
            list.
              - `nin:LocalToComputer,MemberOfLocalGroup`
        prefer (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ListSavedQueriesResponse200]]
    """

    kwargs = _get_kwargs(
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        name=name,
        query=query,
        user_id=user_id,
        scope=scope,
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
    sort_by: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    query: Union[Unset, str] = UNSET,
    user_id: Union[Unset, str] = UNSET,
    scope: Union[Unset, str] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Optional[Union[Any, ListSavedQueriesResponse200]]:
    """List saved queries

     Get all saved queries for the current user

    Args:
        skip (Union[Unset, int]): The number of items to skip in a paginated response.
        limit (Union[Unset, int]): The limit of results requested by the client.
        sort_by (Union[Unset, str]): Sort by column. Can be used multiple times; prepend a hyphen
            for descending order.
            See parameter description for details about which columns are sortable.
        name (Union[Unset, str]): Filter results by column string value. Valid filter predicates
            are `eq`, `neq`.
        query (Union[Unset, str]): Filter results by column string value. Valid filter predicates
            are `eq`, `neq`.
        user_id (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        scope (Union[Unset, str]): The contains predicate checks a property against the values in
            a given comma separated list.
            - `in` checks if the property matches an element in the given comma separated list.
              - `in:Contains,GetChangesAll,MemberOf`
            - `nin` checks if the property does not match an element in the given comma separated
            list.
              - `nin:LocalToComputer,MemberOfLocalGroup`
        prefer (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ListSavedQueriesResponse200]
    """

    return sync_detailed(
        client=client,
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        name=name,
        query=query,
        user_id=user_id,
        scope=scope,
        prefer=prefer,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    skip: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    sort_by: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    query: Union[Unset, str] = UNSET,
    user_id: Union[Unset, str] = UNSET,
    scope: Union[Unset, str] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Response[Union[Any, ListSavedQueriesResponse200]]:
    """List saved queries

     Get all saved queries for the current user

    Args:
        skip (Union[Unset, int]): The number of items to skip in a paginated response.
        limit (Union[Unset, int]): The limit of results requested by the client.
        sort_by (Union[Unset, str]): Sort by column. Can be used multiple times; prepend a hyphen
            for descending order.
            See parameter description for details about which columns are sortable.
        name (Union[Unset, str]): Filter results by column string value. Valid filter predicates
            are `eq`, `neq`.
        query (Union[Unset, str]): Filter results by column string value. Valid filter predicates
            are `eq`, `neq`.
        user_id (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        scope (Union[Unset, str]): The contains predicate checks a property against the values in
            a given comma separated list.
            - `in` checks if the property matches an element in the given comma separated list.
              - `in:Contains,GetChangesAll,MemberOf`
            - `nin` checks if the property does not match an element in the given comma separated
            list.
              - `nin:LocalToComputer,MemberOfLocalGroup`
        prefer (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ListSavedQueriesResponse200]]
    """

    kwargs = _get_kwargs(
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        name=name,
        query=query,
        user_id=user_id,
        scope=scope,
        prefer=prefer,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    skip: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    sort_by: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    query: Union[Unset, str] = UNSET,
    user_id: Union[Unset, str] = UNSET,
    scope: Union[Unset, str] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Optional[Union[Any, ListSavedQueriesResponse200]]:
    """List saved queries

     Get all saved queries for the current user

    Args:
        skip (Union[Unset, int]): The number of items to skip in a paginated response.
        limit (Union[Unset, int]): The limit of results requested by the client.
        sort_by (Union[Unset, str]): Sort by column. Can be used multiple times; prepend a hyphen
            for descending order.
            See parameter description for details about which columns are sortable.
        name (Union[Unset, str]): Filter results by column string value. Valid filter predicates
            are `eq`, `neq`.
        query (Union[Unset, str]): Filter results by column string value. Valid filter predicates
            are `eq`, `neq`.
        user_id (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        scope (Union[Unset, str]): The contains predicate checks a property against the values in
            a given comma separated list.
            - `in` checks if the property matches an element in the given comma separated list.
              - `in:Contains,GetChangesAll,MemberOf`
            - `nin` checks if the property does not match an element in the given comma separated
            list.
              - `nin:LocalToComputer,MemberOfLocalGroup`
        prefer (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ListSavedQueriesResponse200]
    """

    return (
        await asyncio_detailed(
            client=client,
            skip=skip,
            limit=limit,
            sort_by=sort_by,
            name=name,
            query=query,
            user_id=user_id,
            scope=scope,
            prefer=prefer,
        )
    ).parsed
