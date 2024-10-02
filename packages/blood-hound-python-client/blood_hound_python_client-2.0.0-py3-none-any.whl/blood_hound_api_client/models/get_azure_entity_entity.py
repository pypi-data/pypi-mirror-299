from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_azure_entity_entity_data import GetAzureEntityEntityData


T = TypeVar("T", bound="GetAzureEntityEntity")


@_attrs_define
class GetAzureEntityEntity:
    """This response is used when `related_entity_type` is not set. It returns information
    about a single node. All node types will return with the basic node fields, but the
    additional count properties are dependent on the kind of node returned. Setting
    `counts=true` will populate those count details at the cost of performance.

        Attributes:
            data (Union[Unset, GetAzureEntityEntityData]):
    """

    data: Union[Unset, "GetAzureEntityEntityData"] = UNSET
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
        from ..models.get_azure_entity_entity_data import GetAzureEntityEntityData

        d = src_dict.copy()
        _data = d.pop("data", UNSET)
        data: Union[Unset, GetAzureEntityEntityData]
        if isinstance(_data, Unset):
            data = UNSET
        else:
            data = GetAzureEntityEntityData.from_dict(_data)

        get_azure_entity_entity = cls(
            data=data,
        )

        get_azure_entity_entity.additional_properties = d
        return get_azure_entity_entity

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
