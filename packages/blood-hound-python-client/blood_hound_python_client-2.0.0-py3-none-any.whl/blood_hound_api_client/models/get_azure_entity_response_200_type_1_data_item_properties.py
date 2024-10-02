from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.get_azure_entity_response_200_type_1_data_item_properties_additional_property import (
        GetAzureEntityResponse200Type1DataItemPropertiesAdditionalProperty,
    )


T = TypeVar("T", bound="GetAzureEntityResponse200Type1DataItemProperties")


@_attrs_define
class GetAzureEntityResponse200Type1DataItemProperties:
    """ """

    additional_properties: Dict[str, "GetAzureEntityResponse200Type1DataItemPropertiesAdditionalProperty"] = (
        _attrs_field(init=False, factory=dict)
    )

    def to_dict(self) -> Dict[str, Any]:
        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_azure_entity_response_200_type_1_data_item_properties_additional_property import (
            GetAzureEntityResponse200Type1DataItemPropertiesAdditionalProperty,
        )

        d = src_dict.copy()
        get_azure_entity_response_200_type_1_data_item_properties = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = GetAzureEntityResponse200Type1DataItemPropertiesAdditionalProperty.from_dict(
                prop_dict
            )

            additional_properties[prop_name] = additional_property

        get_azure_entity_response_200_type_1_data_item_properties.additional_properties = additional_properties
        return get_azure_entity_response_200_type_1_data_item_properties

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "GetAzureEntityResponse200Type1DataItemPropertiesAdditionalProperty":
        return self.additional_properties[key]

    def __setitem__(
        self, key: str, value: "GetAzureEntityResponse200Type1DataItemPropertiesAdditionalProperty"
    ) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
