from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_azure_entity_entity_data_properties import GetAzureEntityEntityDataProperties


T = TypeVar("T", bound="GetAzureEntityEntityData")


@_attrs_define
class GetAzureEntityEntityData:
    """
    Attributes:
        kind (Union[Unset, str]):
        properties (Union[Unset, GetAzureEntityEntityDataProperties]):
    """

    kind: Union[Unset, str] = UNSET
    properties: Union[Unset, "GetAzureEntityEntityDataProperties"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        kind = self.kind

        properties: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.properties, Unset):
            properties = self.properties.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if kind is not UNSET:
            field_dict["kind"] = kind
        if properties is not UNSET:
            field_dict["properties"] = properties

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_azure_entity_entity_data_properties import GetAzureEntityEntityDataProperties

        d = src_dict.copy()
        kind = d.pop("kind", UNSET)

        _properties = d.pop("properties", UNSET)
        properties: Union[Unset, GetAzureEntityEntityDataProperties]
        if isinstance(_properties, Unset):
            properties = UNSET
        else:
            properties = GetAzureEntityEntityDataProperties.from_dict(_properties)

        get_azure_entity_entity_data = cls(
            kind=kind,
            properties=properties,
        )

        get_azure_entity_entity_data.additional_properties = d
        return get_azure_entity_entity_data

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
