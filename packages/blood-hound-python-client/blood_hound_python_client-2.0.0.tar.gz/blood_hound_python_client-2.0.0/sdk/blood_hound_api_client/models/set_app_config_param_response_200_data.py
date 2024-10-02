from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.set_app_config_param_response_200_data_value import SetAppConfigParamResponse200DataValue


T = TypeVar("T", bound="SetAppConfigParamResponse200Data")


@_attrs_define
class SetAppConfigParamResponse200Data:
    """
    Attributes:
        key (Union[Unset, str]):
        value (Union[Unset, SetAppConfigParamResponse200DataValue]):
    """

    key: Union[Unset, str] = UNSET
    value: Union[Unset, "SetAppConfigParamResponse200DataValue"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        key = self.key

        value: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.value, Unset):
            value = self.value.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if key is not UNSET:
            field_dict["key"] = key
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.set_app_config_param_response_200_data_value import SetAppConfigParamResponse200DataValue

        d = src_dict.copy()
        key = d.pop("key", UNSET)

        _value = d.pop("value", UNSET)
        value: Union[Unset, SetAppConfigParamResponse200DataValue]
        if isinstance(_value, Unset):
            value = UNSET
        else:
            value = SetAppConfigParamResponse200DataValue.from_dict(_value)

        set_app_config_param_response_200_data = cls(
            key=key,
            value=value,
        )

        set_app_config_param_response_200_data.additional_properties = d
        return set_app_config_param_response_200_data

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
