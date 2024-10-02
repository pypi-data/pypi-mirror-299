from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="NullInt64")


@_attrs_define
class NullInt64:
    """
    Attributes:
        int64 (Union[Unset, int]):
        valid (Union[Unset, bool]): Valid is true if `int64` is not `null`.
    """

    int64: Union[Unset, int] = UNSET
    valid: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        int64 = self.int64

        valid = self.valid

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if int64 is not UNSET:
            field_dict["int64"] = int64
        if valid is not UNSET:
            field_dict["valid"] = valid

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        int64 = d.pop("int64", UNSET)

        valid = d.pop("valid", UNSET)

        null_int_64 = cls(
            int64=int64,
            valid=valid,
        )

        null_int_64.additional_properties = d
        return null_int_64

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
