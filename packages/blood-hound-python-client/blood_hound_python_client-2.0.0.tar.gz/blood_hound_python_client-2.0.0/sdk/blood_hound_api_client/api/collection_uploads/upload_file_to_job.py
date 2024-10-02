from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.upload_file_to_job_body import UploadFileToJobBody
from ...models.upload_file_to_job_content_type import UploadFileToJobContentType
from ...types import Response, Unset


def _get_kwargs(
    file_upload_job_id: int,
    *,
    body: UploadFileToJobBody,
    prefer: Union[Unset, int] = 0,
    content_type: UploadFileToJobContentType,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    if not isinstance(prefer, Unset):
        headers["Prefer"] = str(prefer)

    headers["Content-Type"] = str(content_type)

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": f"/api/v2/file-upload/{file_upload_job_id}",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Any]:
    if response.status_code == HTTPStatus.ACCEPTED:
        return None
    if response.status_code == HTTPStatus.BAD_REQUEST:
        return None
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        return None
    if response.status_code == HTTPStatus.NOT_FOUND:
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
    file_upload_job_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UploadFileToJobBody,
    prefer: Union[Unset, int] = 0,
    content_type: UploadFileToJobContentType,
) -> Response[Any]:
    """Upload File To Job

     Saves a collection file to a file upload job

    Args:
        file_upload_job_id (int):
        prefer (Union[Unset, int]):  Default: 0.
        content_type (UploadFileToJobContentType):
        body (UploadFileToJobBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        file_upload_job_id=file_upload_job_id,
        body=body,
        prefer=prefer,
        content_type=content_type,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    file_upload_job_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UploadFileToJobBody,
    prefer: Union[Unset, int] = 0,
    content_type: UploadFileToJobContentType,
) -> Response[Any]:
    """Upload File To Job

     Saves a collection file to a file upload job

    Args:
        file_upload_job_id (int):
        prefer (Union[Unset, int]):  Default: 0.
        content_type (UploadFileToJobContentType):
        body (UploadFileToJobBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        file_upload_job_id=file_upload_job_id,
        body=body,
        prefer=prefer,
        content_type=content_type,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
