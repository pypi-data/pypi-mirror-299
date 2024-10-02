from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delete_saved_query_permissions_body import DeleteSavedQueryPermissionsBody
from ...types import Response, Unset


def _get_kwargs(
    saved_query_id: int,
    *,
    body: DeleteSavedQueryPermissionsBody,
    prefer: Union[Unset, int] = 0,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    if not isinstance(prefer, Unset):
        headers["Prefer"] = str(prefer)

    _kwargs: Dict[str, Any] = {
        "method": "delete",
        "url": f"/api/v2/saved-queries/{saved_query_id}/permissions",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Any]:
    if response.status_code == HTTPStatus.NO_CONTENT:
        return None
    if response.status_code == HTTPStatus.BAD_REQUEST:
        return None
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        return None
    if response.status_code == HTTPStatus.FORBIDDEN:
        return None
    if response.status_code == HTTPStatus.NOT_FOUND:
        return None
    if response.status_code == HTTPStatus.TOO_MANY_REQUESTS:
        return None
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        return None
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    saved_query_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: DeleteSavedQueryPermissionsBody,
    prefer: Union[Unset, int] = 0,
) -> Response[Any]:
    """Revokes permission of a saved query from users

     Revokes permission of a saved query from a given set of users

    Args:
        saved_query_id (int):
        prefer (Union[Unset, int]):  Default: 0.
        body (DeleteSavedQueryPermissionsBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        saved_query_id=saved_query_id,
        body=body,
        prefer=prefer,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    saved_query_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: DeleteSavedQueryPermissionsBody,
    prefer: Union[Unset, int] = 0,
) -> Response[Any]:
    """Revokes permission of a saved query from users

     Revokes permission of a saved query from a given set of users

    Args:
        saved_query_id (int):
        prefer (Union[Unset, int]):  Default: 0.
        body (DeleteSavedQueryPermissionsBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        saved_query_id=saved_query_id,
        body=body,
        prefer=prefer,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
