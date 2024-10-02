import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.enum_datapipe_status import EnumDatapipeStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetDatapipeStatusResponse200Data")


@_attrs_define
class GetDatapipeStatusResponse200Data:
    """
    Attributes:
        status (Union[Unset, EnumDatapipeStatus]):
        updated_at (Union[Unset, datetime.datetime]):
        last_complete_analysis_at (Union[Unset, datetime.datetime]):
    """

    status: Union[Unset, EnumDatapipeStatus] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    last_complete_analysis_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        last_complete_analysis_at: Union[Unset, str] = UNSET
        if not isinstance(self.last_complete_analysis_at, Unset):
            last_complete_analysis_at = self.last_complete_analysis_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if status is not UNSET:
            field_dict["status"] = status
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at
        if last_complete_analysis_at is not UNSET:
            field_dict["last_complete_analysis_at"] = last_complete_analysis_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _status = d.pop("status", UNSET)
        status: Union[Unset, EnumDatapipeStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = EnumDatapipeStatus(_status)

        _updated_at = d.pop("updated_at", UNSET)
        updated_at: Union[Unset, datetime.datetime]
        if isinstance(_updated_at, Unset):
            updated_at = UNSET
        else:
            updated_at = isoparse(_updated_at)

        _last_complete_analysis_at = d.pop("last_complete_analysis_at", UNSET)
        last_complete_analysis_at: Union[Unset, datetime.datetime]
        if isinstance(_last_complete_analysis_at, Unset):
            last_complete_analysis_at = UNSET
        else:
            last_complete_analysis_at = isoparse(_last_complete_analysis_at)

        get_datapipe_status_response_200_data = cls(
            status=status,
            updated_at=updated_at,
            last_complete_analysis_at=last_complete_analysis_at,
        )

        get_datapipe_status_response_200_data.additional_properties = d
        return get_datapipe_status_response_200_data

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
