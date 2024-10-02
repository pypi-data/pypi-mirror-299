from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.model_client_schedule import ModelClientSchedule
from ...models.update_client_event_response_200 import UpdateClientEventResponse200
from ...types import Response, Unset


def _get_kwargs(
    event_id: int,
    *,
    body: ModelClientSchedule,
    prefer: Union[Unset, int] = 0,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    if not isinstance(prefer, Unset):
        headers["Prefer"] = str(prefer)

    _kwargs: Dict[str, Any] = {
        "method": "put",
        "url": f"/api/v2/events/{event_id}",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, UpdateClientEventResponse200]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = UpdateClientEventResponse200.from_dict(response.json())

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
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = cast(Any, None)
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, UpdateClientEventResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    event_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: ModelClientSchedule,
    prefer: Union[Unset, int] = 0,
) -> Response[Union[Any, UpdateClientEventResponse200]]:
    """Update Event

     Updates a scheduled event

    Args:
        event_id (int):
        prefer (Union[Unset, int]):  Default: 0.
        body (ModelClientSchedule):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, UpdateClientEventResponse200]]
    """

    kwargs = _get_kwargs(
        event_id=event_id,
        body=body,
        prefer=prefer,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    event_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: ModelClientSchedule,
    prefer: Union[Unset, int] = 0,
) -> Optional[Union[Any, UpdateClientEventResponse200]]:
    """Update Event

     Updates a scheduled event

    Args:
        event_id (int):
        prefer (Union[Unset, int]):  Default: 0.
        body (ModelClientSchedule):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, UpdateClientEventResponse200]
    """

    return sync_detailed(
        event_id=event_id,
        client=client,
        body=body,
        prefer=prefer,
    ).parsed


async def asyncio_detailed(
    event_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: ModelClientSchedule,
    prefer: Union[Unset, int] = 0,
) -> Response[Union[Any, UpdateClientEventResponse200]]:
    """Update Event

     Updates a scheduled event

    Args:
        event_id (int):
        prefer (Union[Unset, int]):  Default: 0.
        body (ModelClientSchedule):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, UpdateClientEventResponse200]]
    """

    kwargs = _get_kwargs(
        event_id=event_id,
        body=body,
        prefer=prefer,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    event_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: ModelClientSchedule,
    prefer: Union[Unset, int] = 0,
) -> Optional[Union[Any, UpdateClientEventResponse200]]:
    """Update Event

     Updates a scheduled event

    Args:
        event_id (int):
        prefer (Union[Unset, int]):  Default: 0.
        body (ModelClientSchedule):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, UpdateClientEventResponse200]
    """

    return (
        await asyncio_detailed(
            event_id=event_id,
            client=client,
            body=body,
            prefer=prefer,
        )
    ).parsed
