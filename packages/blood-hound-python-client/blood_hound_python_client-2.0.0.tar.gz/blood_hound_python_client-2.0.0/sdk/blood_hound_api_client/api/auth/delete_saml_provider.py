from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_error_wrapper import ApiErrorWrapper
from ...models.delete_saml_provider_response_200 import DeleteSamlProviderResponse200
from ...types import Response, Unset


def _get_kwargs(
    saml_provider_id: int,
    *,
    prefer: Union[Unset, int] = 0,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    if not isinstance(prefer, Unset):
        headers["Prefer"] = str(prefer)

    _kwargs: Dict[str, Any] = {
        "method": "delete",
        "url": f"/api/v2/saml/providers/{saml_provider_id}",
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, ApiErrorWrapper, DeleteSamlProviderResponse200]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = DeleteSamlProviderResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = cast(Any, None)
        return response_401
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = cast(Any, None)
        return response_403
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = cast(Any, None)
        return response_404
    if response.status_code == HTTPStatus.CONFLICT:
        response_409 = ApiErrorWrapper.from_dict(response.json())

        return response_409
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
) -> Response[Union[Any, ApiErrorWrapper, DeleteSamlProviderResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    saml_provider_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    prefer: Union[Unset, int] = 0,
) -> Response[Union[Any, ApiErrorWrapper, DeleteSamlProviderResponse200]]:
    """Delete a SAML Provider

     Deletes an existing BloodHound SAML provider.

    Args:
        saml_provider_id (int):
        prefer (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ApiErrorWrapper, DeleteSamlProviderResponse200]]
    """

    kwargs = _get_kwargs(
        saml_provider_id=saml_provider_id,
        prefer=prefer,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    saml_provider_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    prefer: Union[Unset, int] = 0,
) -> Optional[Union[Any, ApiErrorWrapper, DeleteSamlProviderResponse200]]:
    """Delete a SAML Provider

     Deletes an existing BloodHound SAML provider.

    Args:
        saml_provider_id (int):
        prefer (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ApiErrorWrapper, DeleteSamlProviderResponse200]
    """

    return sync_detailed(
        saml_provider_id=saml_provider_id,
        client=client,
        prefer=prefer,
    ).parsed


async def asyncio_detailed(
    saml_provider_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    prefer: Union[Unset, int] = 0,
) -> Response[Union[Any, ApiErrorWrapper, DeleteSamlProviderResponse200]]:
    """Delete a SAML Provider

     Deletes an existing BloodHound SAML provider.

    Args:
        saml_provider_id (int):
        prefer (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ApiErrorWrapper, DeleteSamlProviderResponse200]]
    """

    kwargs = _get_kwargs(
        saml_provider_id=saml_provider_id,
        prefer=prefer,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    saml_provider_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    prefer: Union[Unset, int] = 0,
) -> Optional[Union[Any, ApiErrorWrapper, DeleteSamlProviderResponse200]]:
    """Delete a SAML Provider

     Deletes an existing BloodHound SAML provider.

    Args:
        saml_provider_id (int):
        prefer (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ApiErrorWrapper, DeleteSamlProviderResponse200]
    """

    return (
        await asyncio_detailed(
            saml_provider_id=saml_provider_id,
            client=client,
            prefer=prefer,
        )
    ).parsed
