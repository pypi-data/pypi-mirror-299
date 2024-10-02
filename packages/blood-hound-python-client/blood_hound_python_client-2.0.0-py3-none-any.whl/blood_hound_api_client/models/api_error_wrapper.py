import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.api_error_detail import ApiErrorDetail


T = TypeVar("T", bound="ApiErrorWrapper")


@_attrs_define
class ApiErrorWrapper:
    """
    Attributes:
        http_status (Union[Unset, int]): The HTTP status code
        timestamp (Union[Unset, datetime.datetime]): The RFC-3339 timestamp in which the error response was sent
        request_id (Union[Unset, str]): The unique identifier of the request that failed
        errors (Union[Unset, List['ApiErrorDetail']]): The error(s) that occurred from processing the request
    """

    http_status: Union[Unset, int] = UNSET
    timestamp: Union[Unset, datetime.datetime] = UNSET
    request_id: Union[Unset, str] = UNSET
    errors: Union[Unset, List["ApiErrorDetail"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        http_status = self.http_status

        timestamp: Union[Unset, str] = UNSET
        if not isinstance(self.timestamp, Unset):
            timestamp = self.timestamp.isoformat()

        request_id = self.request_id

        errors: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.errors, Unset):
            errors = []
            for errors_item_data in self.errors:
                errors_item = errors_item_data.to_dict()
                errors.append(errors_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if http_status is not UNSET:
            field_dict["http_status"] = http_status
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp
        if request_id is not UNSET:
            field_dict["request_id"] = request_id
        if errors is not UNSET:
            field_dict["errors"] = errors

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.api_error_detail import ApiErrorDetail

        d = src_dict.copy()
        http_status = d.pop("http_status", UNSET)

        _timestamp = d.pop("timestamp", UNSET)
        timestamp: Union[Unset, datetime.datetime]
        if isinstance(_timestamp, Unset):
            timestamp = UNSET
        else:
            timestamp = isoparse(_timestamp)

        request_id = d.pop("request_id", UNSET)

        errors = []
        _errors = d.pop("errors", UNSET)
        for errors_item_data in _errors or []:
            errors_item = ApiErrorDetail.from_dict(errors_item_data)

            errors.append(errors_item)

        api_error_wrapper = cls(
            http_status=http_status,
            timestamp=timestamp,
            request_id=request_id,
            errors=errors,
        )

        api_error_wrapper.additional_properties = d
        return api_error_wrapper

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
