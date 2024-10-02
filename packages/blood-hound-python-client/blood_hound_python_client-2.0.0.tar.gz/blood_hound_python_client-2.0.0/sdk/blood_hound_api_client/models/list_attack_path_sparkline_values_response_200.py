import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.model_risk_counts import ModelRiskCounts


T = TypeVar("T", bound="ListAttackPathSparklineValuesResponse200")


@_attrs_define
class ListAttackPathSparklineValuesResponse200:
    """
    Attributes:
        start (Union[Unset, datetime.datetime]): The RFC-3339 timestamp to describe the beginning of a time range
        end (Union[Unset, datetime.datetime]): The RFC-3339 timestamp to describe the end of a time range
        data (Union[Unset, List['ModelRiskCounts']]):
    """

    start: Union[Unset, datetime.datetime] = UNSET
    end: Union[Unset, datetime.datetime] = UNSET
    data: Union[Unset, List["ModelRiskCounts"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        start: Union[Unset, str] = UNSET
        if not isinstance(self.start, Unset):
            start = self.start.isoformat()

        end: Union[Unset, str] = UNSET
        if not isinstance(self.end, Unset):
            end = self.end.isoformat()

        data: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.data, Unset):
            data = []
            for data_item_data in self.data:
                data_item = data_item_data.to_dict()
                data.append(data_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if start is not UNSET:
            field_dict["start"] = start
        if end is not UNSET:
            field_dict["end"] = end
        if data is not UNSET:
            field_dict["data"] = data

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.model_risk_counts import ModelRiskCounts

        d = src_dict.copy()
        _start = d.pop("start", UNSET)
        start: Union[Unset, datetime.datetime]
        if isinstance(_start, Unset):
            start = UNSET
        else:
            start = isoparse(_start)

        _end = d.pop("end", UNSET)
        end: Union[Unset, datetime.datetime]
        if isinstance(_end, Unset):
            end = UNSET
        else:
            end = isoparse(_end)

        data = []
        _data = d.pop("data", UNSET)
        for data_item_data in _data or []:
            data_item = ModelRiskCounts.from_dict(data_item_data)

            data.append(data_item)

        list_attack_path_sparkline_values_response_200 = cls(
            start=start,
            end=end,
            data=data,
        )

        list_attack_path_sparkline_values_response_200.additional_properties = d
        return list_attack_path_sparkline_values_response_200

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
