from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_file_upload_job_response_201 import CreateFileUploadJobResponse201
from ...types import Response, Unset


def _get_kwargs(
    *,
    prefer: Union[Unset, int] = 0,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    if not isinstance(prefer, Unset):
        headers["Prefer"] = str(prefer)

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/api/v2/file-upload/start",
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, CreateFileUploadJobResponse201]]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = CreateFileUploadJobResponse201.from_dict(response.json())

        return response_201
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
) -> Response[Union[Any, CreateFileUploadJobResponse201]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    prefer: Union[Unset, int] = 0,
) -> Response[Union[Any, CreateFileUploadJobResponse201]]:
    """Create File Upload Job

     Creates a file upload job for sending collection files

    Args:
        prefer (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, CreateFileUploadJobResponse201]]
    """

    kwargs = _get_kwargs(
        prefer=prefer,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    prefer: Union[Unset, int] = 0,
) -> Optional[Union[Any, CreateFileUploadJobResponse201]]:
    """Create File Upload Job

     Creates a file upload job for sending collection files

    Args:
        prefer (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, CreateFileUploadJobResponse201]
    """

    return sync_detailed(
        client=client,
        prefer=prefer,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    prefer: Union[Unset, int] = 0,
) -> Response[Union[Any, CreateFileUploadJobResponse201]]:
    """Create File Upload Job

     Creates a file upload job for sending collection files

    Args:
        prefer (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, CreateFileUploadJobResponse201]]
    """

    kwargs = _get_kwargs(
        prefer=prefer,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    prefer: Union[Unset, int] = 0,
) -> Optional[Union[Any, CreateFileUploadJobResponse201]]:
    """Create File Upload Job

     Creates a file upload job for sending collection files

    Args:
        prefer (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, CreateFileUploadJobResponse201]
    """

    return (
        await asyncio_detailed(
            client=client,
            prefer=prefer,
        )
    ).parsed
