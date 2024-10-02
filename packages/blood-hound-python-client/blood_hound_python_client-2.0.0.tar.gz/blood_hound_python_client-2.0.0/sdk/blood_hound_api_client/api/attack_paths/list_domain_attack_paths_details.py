import datetime
from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_domain_attack_paths_details_response_200_type_0 import ListDomainAttackPathsDetailsResponse200Type0
from ...models.list_domain_attack_paths_details_response_200_type_1 import ListDomainAttackPathsDetailsResponse200Type1
from ...types import UNSET, Response, Unset


def _get_kwargs(
    domain_id: str,
    *,
    finding: Union[Unset, str] = UNSET,
    sort_by: Union[Unset, str] = UNSET,
    FromPrincipal: Union[Unset, str] = UNSET,
    ToPrincipal: Union[Unset, str] = UNSET,
    from_principal: Union[Unset, str] = UNSET,
    to_principal: Union[Unset, str] = UNSET,
    principals_hash: Union[Unset, str] = UNSET,
    accepted: Union[Unset, str] = UNSET,
    AcceptedUntil: Union[Unset, datetime.datetime] = UNSET,
    accepted_until: Union[Unset, datetime.datetime] = UNSET,
    principal: Union[Unset, str] = UNSET,
    Finding: Union[Unset, str] = UNSET,
    domain_sid: Union[Unset, str] = UNSET,
    id: Union[Unset, int] = UNSET,
    created_at: Union[Unset, datetime.datetime] = UNSET,
    updated_at: Union[Unset, datetime.datetime] = UNSET,
    deleted_at: Union[Unset, datetime.datetime] = UNSET,
    skip: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    if not isinstance(prefer, Unset):
        headers["Prefer"] = str(prefer)

    params: Dict[str, Any] = {}

    params["finding"] = finding

    params["sort_by"] = sort_by

    params["FromPrincipal"] = FromPrincipal

    params["ToPrincipal"] = ToPrincipal

    params["from_principal"] = from_principal

    params["to_principal"] = to_principal

    params["principals_hash"] = principals_hash

    params["Accepted"] = accepted

    json_AcceptedUntil: Union[Unset, str] = UNSET
    if not isinstance(AcceptedUntil, Unset):
        json_AcceptedUntil = AcceptedUntil.isoformat()
    params["AcceptedUntil"] = json_AcceptedUntil

    json_accepted_until: Union[Unset, str] = UNSET
    if not isinstance(accepted_until, Unset):
        json_accepted_until = accepted_until.isoformat()
    params["accepted_until"] = json_accepted_until

    params["Principal"] = principal

    params["Finding"] = Finding

    params["domain_sid"] = domain_sid

    params["id"] = id

    json_created_at: Union[Unset, str] = UNSET
    if not isinstance(created_at, Unset):
        json_created_at = created_at.isoformat()
    params["created_at"] = json_created_at

    json_updated_at: Union[Unset, str] = UNSET
    if not isinstance(updated_at, Unset):
        json_updated_at = updated_at.isoformat()
    params["updated_at"] = json_updated_at

    json_deleted_at: Union[Unset, str] = UNSET
    if not isinstance(deleted_at, Unset):
        json_deleted_at = deleted_at.isoformat()
    params["deleted_at"] = json_deleted_at

    params["skip"] = skip

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/api/v2/domains/{domain_id}/details",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[Any, Union["ListDomainAttackPathsDetailsResponse200Type0", "ListDomainAttackPathsDetailsResponse200Type1"]]
]:
    if response.status_code == HTTPStatus.OK:

        def _parse_response_200(
            data: object,
        ) -> Union["ListDomainAttackPathsDetailsResponse200Type0", "ListDomainAttackPathsDetailsResponse200Type1"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_0 = ListDomainAttackPathsDetailsResponse200Type0.from_dict(data)

                return response_200_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            response_200_type_1 = ListDomainAttackPathsDetailsResponse200Type1.from_dict(data)

            return response_200_type_1

        response_200 = _parse_response_200(response.json())

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
) -> Response[
    Union[Any, Union["ListDomainAttackPathsDetailsResponse200Type0", "ListDomainAttackPathsDetailsResponse200Type1"]]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    domain_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    finding: Union[Unset, str] = UNSET,
    sort_by: Union[Unset, str] = UNSET,
    FromPrincipal: Union[Unset, str] = UNSET,
    ToPrincipal: Union[Unset, str] = UNSET,
    from_principal: Union[Unset, str] = UNSET,
    to_principal: Union[Unset, str] = UNSET,
    principals_hash: Union[Unset, str] = UNSET,
    accepted: Union[Unset, str] = UNSET,
    AcceptedUntil: Union[Unset, datetime.datetime] = UNSET,
    accepted_until: Union[Unset, datetime.datetime] = UNSET,
    principal: Union[Unset, str] = UNSET,
    Finding: Union[Unset, str] = UNSET,
    domain_sid: Union[Unset, str] = UNSET,
    id: Union[Unset, int] = UNSET,
    created_at: Union[Unset, datetime.datetime] = UNSET,
    updated_at: Union[Unset, datetime.datetime] = UNSET,
    deleted_at: Union[Unset, datetime.datetime] = UNSET,
    skip: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Response[
    Union[Any, Union["ListDomainAttackPathsDetailsResponse200Type0", "ListDomainAttackPathsDetailsResponse200Type1"]]
]:
    """List domain attack paths details

     Lists detailed data about attack paths for a domain.

    Args:
        domain_id (str):
        finding (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        sort_by (Union[Unset, str]): Sort by column. Can be used multiple times; prepend a hyphen
            for descending order.
            See parameter description for details about which columns are sortable.
        FromPrincipal (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        ToPrincipal (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        from_principal (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        to_principal (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        principals_hash (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        accepted (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        AcceptedUntil (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        accepted_until (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        principal (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        Finding (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        domain_sid (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        id (Union[Unset, int]): Filter results by column integer value. Valid filter predicates
            are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        created_at (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        updated_at (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        deleted_at (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        skip (Union[Unset, int]): The number of items to skip in a paginated response.
        limit (Union[Unset, int]): The limit of results requested by the client.
        prefer (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Union['ListDomainAttackPathsDetailsResponse200Type0', 'ListDomainAttackPathsDetailsResponse200Type1']]]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
        finding=finding,
        sort_by=sort_by,
        FromPrincipal=FromPrincipal,
        ToPrincipal=ToPrincipal,
        from_principal=from_principal,
        to_principal=to_principal,
        principals_hash=principals_hash,
        accepted=accepted,
        AcceptedUntil=AcceptedUntil,
        accepted_until=accepted_until,
        principal=principal,
        Finding=Finding,
        domain_sid=domain_sid,
        id=id,
        created_at=created_at,
        updated_at=updated_at,
        deleted_at=deleted_at,
        skip=skip,
        limit=limit,
        prefer=prefer,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    domain_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    finding: Union[Unset, str] = UNSET,
    sort_by: Union[Unset, str] = UNSET,
    FromPrincipal: Union[Unset, str] = UNSET,
    ToPrincipal: Union[Unset, str] = UNSET,
    from_principal: Union[Unset, str] = UNSET,
    to_principal: Union[Unset, str] = UNSET,
    principals_hash: Union[Unset, str] = UNSET,
    accepted: Union[Unset, str] = UNSET,
    AcceptedUntil: Union[Unset, datetime.datetime] = UNSET,
    accepted_until: Union[Unset, datetime.datetime] = UNSET,
    principal: Union[Unset, str] = UNSET,
    Finding: Union[Unset, str] = UNSET,
    domain_sid: Union[Unset, str] = UNSET,
    id: Union[Unset, int] = UNSET,
    created_at: Union[Unset, datetime.datetime] = UNSET,
    updated_at: Union[Unset, datetime.datetime] = UNSET,
    deleted_at: Union[Unset, datetime.datetime] = UNSET,
    skip: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Optional[
    Union[Any, Union["ListDomainAttackPathsDetailsResponse200Type0", "ListDomainAttackPathsDetailsResponse200Type1"]]
]:
    """List domain attack paths details

     Lists detailed data about attack paths for a domain.

    Args:
        domain_id (str):
        finding (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        sort_by (Union[Unset, str]): Sort by column. Can be used multiple times; prepend a hyphen
            for descending order.
            See parameter description for details about which columns are sortable.
        FromPrincipal (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        ToPrincipal (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        from_principal (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        to_principal (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        principals_hash (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        accepted (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        AcceptedUntil (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        accepted_until (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        principal (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        Finding (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        domain_sid (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        id (Union[Unset, int]): Filter results by column integer value. Valid filter predicates
            are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        created_at (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        updated_at (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        deleted_at (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        skip (Union[Unset, int]): The number of items to skip in a paginated response.
        limit (Union[Unset, int]): The limit of results requested by the client.
        prefer (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Union['ListDomainAttackPathsDetailsResponse200Type0', 'ListDomainAttackPathsDetailsResponse200Type1']]
    """

    return sync_detailed(
        domain_id=domain_id,
        client=client,
        finding=finding,
        sort_by=sort_by,
        FromPrincipal=FromPrincipal,
        ToPrincipal=ToPrincipal,
        from_principal=from_principal,
        to_principal=to_principal,
        principals_hash=principals_hash,
        accepted=accepted,
        AcceptedUntil=AcceptedUntil,
        accepted_until=accepted_until,
        principal=principal,
        Finding=Finding,
        domain_sid=domain_sid,
        id=id,
        created_at=created_at,
        updated_at=updated_at,
        deleted_at=deleted_at,
        skip=skip,
        limit=limit,
        prefer=prefer,
    ).parsed


async def asyncio_detailed(
    domain_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    finding: Union[Unset, str] = UNSET,
    sort_by: Union[Unset, str] = UNSET,
    FromPrincipal: Union[Unset, str] = UNSET,
    ToPrincipal: Union[Unset, str] = UNSET,
    from_principal: Union[Unset, str] = UNSET,
    to_principal: Union[Unset, str] = UNSET,
    principals_hash: Union[Unset, str] = UNSET,
    accepted: Union[Unset, str] = UNSET,
    AcceptedUntil: Union[Unset, datetime.datetime] = UNSET,
    accepted_until: Union[Unset, datetime.datetime] = UNSET,
    principal: Union[Unset, str] = UNSET,
    Finding: Union[Unset, str] = UNSET,
    domain_sid: Union[Unset, str] = UNSET,
    id: Union[Unset, int] = UNSET,
    created_at: Union[Unset, datetime.datetime] = UNSET,
    updated_at: Union[Unset, datetime.datetime] = UNSET,
    deleted_at: Union[Unset, datetime.datetime] = UNSET,
    skip: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Response[
    Union[Any, Union["ListDomainAttackPathsDetailsResponse200Type0", "ListDomainAttackPathsDetailsResponse200Type1"]]
]:
    """List domain attack paths details

     Lists detailed data about attack paths for a domain.

    Args:
        domain_id (str):
        finding (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        sort_by (Union[Unset, str]): Sort by column. Can be used multiple times; prepend a hyphen
            for descending order.
            See parameter description for details about which columns are sortable.
        FromPrincipal (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        ToPrincipal (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        from_principal (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        to_principal (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        principals_hash (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        accepted (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        AcceptedUntil (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        accepted_until (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        principal (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        Finding (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        domain_sid (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        id (Union[Unset, int]): Filter results by column integer value. Valid filter predicates
            are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        created_at (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        updated_at (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        deleted_at (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        skip (Union[Unset, int]): The number of items to skip in a paginated response.
        limit (Union[Unset, int]): The limit of results requested by the client.
        prefer (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Union['ListDomainAttackPathsDetailsResponse200Type0', 'ListDomainAttackPathsDetailsResponse200Type1']]]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
        finding=finding,
        sort_by=sort_by,
        FromPrincipal=FromPrincipal,
        ToPrincipal=ToPrincipal,
        from_principal=from_principal,
        to_principal=to_principal,
        principals_hash=principals_hash,
        accepted=accepted,
        AcceptedUntil=AcceptedUntil,
        accepted_until=accepted_until,
        principal=principal,
        Finding=Finding,
        domain_sid=domain_sid,
        id=id,
        created_at=created_at,
        updated_at=updated_at,
        deleted_at=deleted_at,
        skip=skip,
        limit=limit,
        prefer=prefer,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    domain_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    finding: Union[Unset, str] = UNSET,
    sort_by: Union[Unset, str] = UNSET,
    FromPrincipal: Union[Unset, str] = UNSET,
    ToPrincipal: Union[Unset, str] = UNSET,
    from_principal: Union[Unset, str] = UNSET,
    to_principal: Union[Unset, str] = UNSET,
    principals_hash: Union[Unset, str] = UNSET,
    accepted: Union[Unset, str] = UNSET,
    AcceptedUntil: Union[Unset, datetime.datetime] = UNSET,
    accepted_until: Union[Unset, datetime.datetime] = UNSET,
    principal: Union[Unset, str] = UNSET,
    Finding: Union[Unset, str] = UNSET,
    domain_sid: Union[Unset, str] = UNSET,
    id: Union[Unset, int] = UNSET,
    created_at: Union[Unset, datetime.datetime] = UNSET,
    updated_at: Union[Unset, datetime.datetime] = UNSET,
    deleted_at: Union[Unset, datetime.datetime] = UNSET,
    skip: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    prefer: Union[Unset, int] = 0,
) -> Optional[
    Union[Any, Union["ListDomainAttackPathsDetailsResponse200Type0", "ListDomainAttackPathsDetailsResponse200Type1"]]
]:
    """List domain attack paths details

     Lists detailed data about attack paths for a domain.

    Args:
        domain_id (str):
        finding (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        sort_by (Union[Unset, str]): Sort by column. Can be used multiple times; prepend a hyphen
            for descending order.
            See parameter description for details about which columns are sortable.
        FromPrincipal (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        ToPrincipal (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        from_principal (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        to_principal (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        principals_hash (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        accepted (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        AcceptedUntil (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        accepted_until (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        principal (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        Finding (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        domain_sid (Union[Unset, str]): Filter results by column string value. Valid filter
            predicates are `eq`, `neq`.
        id (Union[Unset, int]): Filter results by column integer value. Valid filter predicates
            are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        created_at (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        updated_at (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        deleted_at (Union[Unset, datetime.datetime]): Filter results by column timestamp value
            formatted as an RFC-3339 string.
            Valid filter predicates are `eq`, `neq`, `gt`, `gte`, `lt`, `lte`.
        skip (Union[Unset, int]): The number of items to skip in a paginated response.
        limit (Union[Unset, int]): The limit of results requested by the client.
        prefer (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Union['ListDomainAttackPathsDetailsResponse200Type0', 'ListDomainAttackPathsDetailsResponse200Type1']]
    """

    return (
        await asyncio_detailed(
            domain_id=domain_id,
            client=client,
            finding=finding,
            sort_by=sort_by,
            FromPrincipal=FromPrincipal,
            ToPrincipal=ToPrincipal,
            from_principal=from_principal,
            to_principal=to_principal,
            principals_hash=principals_hash,
            accepted=accepted,
            AcceptedUntil=AcceptedUntil,
            accepted_until=accepted_until,
            principal=principal,
            Finding=Finding,
            domain_sid=domain_sid,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            deleted_at=deleted_at,
            skip=skip,
            limit=limit,
            prefer=prefer,
        )
    ).parsed
