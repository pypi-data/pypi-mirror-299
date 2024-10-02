from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.api_response_data_quality_platform_aggregate_data import ApiResponseDataQualityPlatformAggregateData


T = TypeVar("T", bound="ApiResponseDataQualityPlatformAggregate")


@_attrs_define
class ApiResponseDataQualityPlatformAggregate:
    """
    Attributes:
        data (Union[Unset, ApiResponseDataQualityPlatformAggregateData]):
    """

    data: Union[Unset, "ApiResponseDataQualityPlatformAggregateData"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.data, Unset):
            data = self.data.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if data is not UNSET:
            field_dict["data"] = data

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.api_response_data_quality_platform_aggregate_data import (
            ApiResponseDataQualityPlatformAggregateData,
        )

        d = src_dict.copy()
        _data = d.pop("data", UNSET)
        data: Union[Unset, ApiResponseDataQualityPlatformAggregateData]
        if isinstance(_data, Unset):
            data = UNSET
        else:
            data = ApiResponseDataQualityPlatformAggregateData.from_dict(_data)

        api_response_data_quality_platform_aggregate = cls(
            data=data,
        )

        api_response_data_quality_platform_aggregate.additional_properties = d
        return api_response_data_quality_platform_aggregate

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
