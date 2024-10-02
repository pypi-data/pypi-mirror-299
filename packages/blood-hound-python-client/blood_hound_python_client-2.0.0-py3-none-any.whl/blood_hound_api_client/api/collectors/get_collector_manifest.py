from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.enum_client_type import EnumClientType
from ...models.get_collector_manifest_response_200 import GetCollectorManifestResponse200
from ...types import Response, Unset


def _get_kwargs(
    collector_type: EnumClientType,
    *,
    prefer: Union[Unset, int] = 0,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    if not isinstance(prefer, Unset):
        headers["Prefer"] = str(prefer)

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/api/v2/collectors/{collector_type}",
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, GetCollectorManifestResponse200]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetCollectorManifestResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = cast(Any, None)
        return response_401
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = cast(Any, None)
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, GetCollectorManifestResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    collector_type: EnumClientType,
    *,
    client: Union[AuthenticatedClient, Client],
    prefer: Union[Unset, int] = 0,
) -> Response[Union[Any, GetCollectorManifestResponse200]]:
    """Get collector manifest

     Retrieves the version manifest for a given collector

    Args:
        collector_type (EnumClientType): This enum describes the collector client type.
        prefer (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, GetCollectorManifestResponse200]]
    """

    kwargs = _get_kwargs(
        collector_type=collector_type,
        prefer=prefer,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    collector_type: EnumClientType,
    *,
    client: Union[AuthenticatedClient, Client],
    prefer: Union[Unset, int] = 0,
) -> Optional[Union[Any, GetCollectorManifestResponse200]]:
    """Get collector manifest

     Retrieves the version manifest for a given collector

    Args:
        collector_type (EnumClientType): This enum describes the collector client type.
        prefer (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, GetCollectorManifestResponse200]
    """

    return sync_detailed(
        collector_type=collector_type,
        client=client,
        prefer=prefer,
    ).parsed


async def asyncio_detailed(
    collector_type: EnumClientType,
    *,
    client: Union[AuthenticatedClient, Client],
    prefer: Union[Unset, int] = 0,
) -> Response[Union[Any, GetCollectorManifestResponse200]]:
    """Get collector manifest

     Retrieves the version manifest for a given collector

    Args:
        collector_type (EnumClientType): This enum describes the collector client type.
        prefer (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, GetCollectorManifestResponse200]]
    """

    kwargs = _get_kwargs(
        collector_type=collector_type,
        prefer=prefer,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    collector_type: EnumClientType,
    *,
    client: Union[AuthenticatedClient, Client],
    prefer: Union[Unset, int] = 0,
) -> Optional[Union[Any, GetCollectorManifestResponse200]]:
    """Get collector manifest

     Retrieves the version manifest for a given collector

    Args:
        collector_type (EnumClientType): This enum describes the collector client type.
        prefer (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, GetCollectorManifestResponse200]
    """

    return (
        await asyncio_detailed(
            collector_type=collector_type,
            client=client,
            prefer=prefer,
        )
    ).parsed
