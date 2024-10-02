from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_response_finding import ApiResponseFinding
from ...models.update_attack_path_risk_body import UpdateAttackPathRiskBody
from ...types import Response, Unset


def _get_kwargs(
    attack_path_id: int,
    *,
    body: UpdateAttackPathRiskBody,
    prefer: Union[Unset, int] = 0,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    if not isinstance(prefer, Unset):
        headers["Prefer"] = str(prefer)

    _kwargs: Dict[str, Any] = {
        "method": "put",
        "url": f"/api/v2/attack-paths/{attack_path_id}/acceptance",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, ApiResponseFinding]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ApiResponseFinding.from_dict(response.json())

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
) -> Response[Union[Any, ApiResponseFinding]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    attack_path_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateAttackPathRiskBody,
    prefer: Union[Unset, int] = 0,
) -> Response[Union[Any, ApiResponseFinding]]:
    """Update attack path risk

     Updates an attack path as an accepted or unaccepted risk until a given time.

    Args:
        attack_path_id (int):
        prefer (Union[Unset, int]):  Default: 0.
        body (UpdateAttackPathRiskBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ApiResponseFinding]]
    """

    kwargs = _get_kwargs(
        attack_path_id=attack_path_id,
        body=body,
        prefer=prefer,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    attack_path_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateAttackPathRiskBody,
    prefer: Union[Unset, int] = 0,
) -> Optional[Union[Any, ApiResponseFinding]]:
    """Update attack path risk

     Updates an attack path as an accepted or unaccepted risk until a given time.

    Args:
        attack_path_id (int):
        prefer (Union[Unset, int]):  Default: 0.
        body (UpdateAttackPathRiskBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ApiResponseFinding]
    """

    return sync_detailed(
        attack_path_id=attack_path_id,
        client=client,
        body=body,
        prefer=prefer,
    ).parsed


async def asyncio_detailed(
    attack_path_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateAttackPathRiskBody,
    prefer: Union[Unset, int] = 0,
) -> Response[Union[Any, ApiResponseFinding]]:
    """Update attack path risk

     Updates an attack path as an accepted or unaccepted risk until a given time.

    Args:
        attack_path_id (int):
        prefer (Union[Unset, int]):  Default: 0.
        body (UpdateAttackPathRiskBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ApiResponseFinding]]
    """

    kwargs = _get_kwargs(
        attack_path_id=attack_path_id,
        body=body,
        prefer=prefer,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    attack_path_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateAttackPathRiskBody,
    prefer: Union[Unset, int] = 0,
) -> Optional[Union[Any, ApiResponseFinding]]:
    """Update attack path risk

     Updates an attack path as an accepted or unaccepted risk until a given time.

    Args:
        attack_path_id (int):
        prefer (Union[Unset, int]):  Default: 0.
        body (UpdateAttackPathRiskBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ApiResponseFinding]
    """

    return (
        await asyncio_detailed(
            attack_path_id=attack_path_id,
            client=client,
            body=body,
            prefer=prefer,
        )
    ).parsed
