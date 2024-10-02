from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_azure_entity_response_200_type_1_data_item_properties import (
        GetAzureEntityResponse200Type1DataItemProperties,
    )


T = TypeVar("T", bound="GetAzureEntityResponse200Type1DataItem")


@_attrs_define
class GetAzureEntityResponse200Type1DataItem:
    """
    Attributes:
        kind (Union[Unset, str]):
        properties (Union[Unset, GetAzureEntityResponse200Type1DataItemProperties]):
        additional_properties (Union[Unset, int]):
    """

    kind: Union[Unset, str] = UNSET
    properties: Union[Unset, "GetAzureEntityResponse200Type1DataItemProperties"] = UNSET
    additional_properties: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        kind = self.kind

        properties: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.properties, Unset):
            properties = self.properties.to_dict()

        additional_properties = self.additional_properties

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if kind is not UNSET:
            field_dict["kind"] = kind
        if properties is not UNSET:
            field_dict["properties"] = properties
        if additional_properties is not UNSET:
            field_dict["additionalProperties"] = additional_properties

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_azure_entity_response_200_type_1_data_item_properties import (
            GetAzureEntityResponse200Type1DataItemProperties,
        )

        d = src_dict.copy()
        kind = d.pop("kind", UNSET)

        _properties = d.pop("properties", UNSET)
        properties: Union[Unset, GetAzureEntityResponse200Type1DataItemProperties]
        if isinstance(_properties, Unset):
            properties = UNSET
        else:
            properties = GetAzureEntityResponse200Type1DataItemProperties.from_dict(_properties)

        additional_properties = d.pop("additionalProperties", UNSET)

        get_azure_entity_response_200_type_1_data_item = cls(
            kind=kind,
            properties=properties,
            additional_properties=additional_properties,
        )

        get_azure_entity_response_200_type_1_data_item.additional_properties = d
        return get_azure_entity_response_200_type_1_data_item

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
