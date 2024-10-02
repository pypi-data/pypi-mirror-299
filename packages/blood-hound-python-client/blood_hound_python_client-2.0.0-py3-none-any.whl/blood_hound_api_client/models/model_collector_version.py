from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelCollectorVersion")


@_attrs_define
class ModelCollectorVersion:
    """
    Attributes:
        version (Union[Unset, str]):
        sha256sum (Union[Unset, str]):
        deprecated (Union[Unset, bool]):
    """

    version: Union[Unset, str] = UNSET
    sha256sum: Union[Unset, str] = UNSET
    deprecated: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        version = self.version

        sha256sum = self.sha256sum

        deprecated = self.deprecated

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if version is not UNSET:
            field_dict["version"] = version
        if sha256sum is not UNSET:
            field_dict["sha256sum"] = sha256sum
        if deprecated is not UNSET:
            field_dict["deprecated"] = deprecated

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        version = d.pop("version", UNSET)

        sha256sum = d.pop("sha256sum", UNSET)

        deprecated = d.pop("deprecated", UNSET)

        model_collector_version = cls(
            version=version,
            sha256sum=sha256sum,
            deprecated=deprecated,
        )

        model_collector_version.additional_properties = d
        return model_collector_version

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
