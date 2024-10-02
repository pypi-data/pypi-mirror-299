from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.update_domain_entity_body import UpdateDomainEntityBody
from ...models.update_domain_entity_response_200 import UpdateDomainEntityResponse200
from ...types import Response, Unset


def _get_kwargs(
    object_id: str,
    *,
    body: UpdateDomainEntityBody,
    prefer: Union[Unset, int] = 0,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    if not isinstance(prefer, Unset):
        headers["Prefer"] = str(prefer)

    _kwargs: Dict[str, Any] = {
        "method": "patch",
        "url": f"/api/v2/domains/{object_id}",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, UpdateDomainEntityResponse200]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = UpdateDomainEntityResponse200.from_dict(response.json())

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
) -> Response[Union[Any, UpdateDomainEntityResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    object_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateDomainEntityBody,
    prefer: Union[Unset, int] = 0,
) -> Response[Union[Any, UpdateDomainEntityResponse200]]:
    """Update the Domain entity

     Updates the supported properties on the Domain entity.

    Args:
        object_id (str): The unique object identifier
        prefer (Union[Unset, int]):  Default: 0.
        body (UpdateDomainEntityBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, UpdateDomainEntityResponse200]]
    """

    kwargs = _get_kwargs(
        object_id=object_id,
        body=body,
        prefer=prefer,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    object_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateDomainEntityBody,
    prefer: Union[Unset, int] = 0,
) -> Optional[Union[Any, UpdateDomainEntityResponse200]]:
    """Update the Domain entity

     Updates the supported properties on the Domain entity.

    Args:
        object_id (str): The unique object identifier
        prefer (Union[Unset, int]):  Default: 0.
        body (UpdateDomainEntityBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, UpdateDomainEntityResponse200]
    """

    return sync_detailed(
        object_id=object_id,
        client=client,
        body=body,
        prefer=prefer,
    ).parsed


async def asyncio_detailed(
    object_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateDomainEntityBody,
    prefer: Union[Unset, int] = 0,
) -> Response[Union[Any, UpdateDomainEntityResponse200]]:
    """Update the Domain entity

     Updates the supported properties on the Domain entity.

    Args:
        object_id (str): The unique object identifier
        prefer (Union[Unset, int]):  Default: 0.
        body (UpdateDomainEntityBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, UpdateDomainEntityResponse200]]
    """

    kwargs = _get_kwargs(
        object_id=object_id,
        body=body,
        prefer=prefer,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    object_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateDomainEntityBody,
    prefer: Union[Unset, int] = 0,
) -> Optional[Union[Any, UpdateDomainEntityResponse200]]:
    """Update the Domain entity

     Updates the supported properties on the Domain entity.

    Args:
        object_id (str): The unique object identifier
        prefer (Union[Unset, int]):  Default: 0.
        body (UpdateDomainEntityBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, UpdateDomainEntityResponse200]
    """

    return (
        await asyncio_detailed(
            object_id=object_id,
            client=client,
            body=body,
            prefer=prefer,
        )
    ).parsed
