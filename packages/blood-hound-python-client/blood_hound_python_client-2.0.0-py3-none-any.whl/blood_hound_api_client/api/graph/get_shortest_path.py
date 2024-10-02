from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_shortest_path_response_200 import GetShortestPathResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    start_node: int,
    end_node: int,
    relationship_kinds: Union[Unset, str] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    if not isinstance(prefer, Unset):
        headers["Prefer"] = str(prefer)

    params: Dict[str, Any] = {}

    params["start_node"] = start_node

    params["end_node"] = end_node

    params["relationship_kinds"] = relationship_kinds

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/api/v2/graphs/shortest-path",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, GetShortestPathResponse200]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetShortestPathResponse200.from_dict(response.json())

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
) -> Response[Union[Any, GetShortestPathResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    start_node: int,
    end_node: int,
    relationship_kinds: Union[Unset, str] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Response[Union[Any, GetShortestPathResponse200]]:
    """Get the shortest path graph

     A graph of the shortest path from `start_node` to `end_node`.

    Args:
        start_node (int):
        end_node (int):
        relationship_kinds (Union[Unset, str]): The contains predicate checks a property against
            the values in a given comma separated list.
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
        Response[Union[Any, GetShortestPathResponse200]]
    """

    kwargs = _get_kwargs(
        start_node=start_node,
        end_node=end_node,
        relationship_kinds=relationship_kinds,
        prefer=prefer,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    start_node: int,
    end_node: int,
    relationship_kinds: Union[Unset, str] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Optional[Union[Any, GetShortestPathResponse200]]:
    """Get the shortest path graph

     A graph of the shortest path from `start_node` to `end_node`.

    Args:
        start_node (int):
        end_node (int):
        relationship_kinds (Union[Unset, str]): The contains predicate checks a property against
            the values in a given comma separated list.
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
        Union[Any, GetShortestPathResponse200]
    """

    return sync_detailed(
        client=client,
        start_node=start_node,
        end_node=end_node,
        relationship_kinds=relationship_kinds,
        prefer=prefer,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    start_node: int,
    end_node: int,
    relationship_kinds: Union[Unset, str] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Response[Union[Any, GetShortestPathResponse200]]:
    """Get the shortest path graph

     A graph of the shortest path from `start_node` to `end_node`.

    Args:
        start_node (int):
        end_node (int):
        relationship_kinds (Union[Unset, str]): The contains predicate checks a property against
            the values in a given comma separated list.
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
        Response[Union[Any, GetShortestPathResponse200]]
    """

    kwargs = _get_kwargs(
        start_node=start_node,
        end_node=end_node,
        relationship_kinds=relationship_kinds,
        prefer=prefer,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    start_node: int,
    end_node: int,
    relationship_kinds: Union[Unset, str] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Optional[Union[Any, GetShortestPathResponse200]]:
    """Get the shortest path graph

     A graph of the shortest path from `start_node` to `end_node`.

    Args:
        start_node (int):
        end_node (int):
        relationship_kinds (Union[Unset, str]): The contains predicate checks a property against
            the values in a given comma separated list.
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
        Union[Any, GetShortestPathResponse200]
    """

    return (
        await asyncio_detailed(
            client=client,
            start_node=start_node,
            end_node=end_node,
            relationship_kinds=relationship_kinds,
            prefer=prefer,
        )
    ).parsed
