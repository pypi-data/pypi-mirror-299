from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_meta_entity_response_200_data_props import GetMetaEntityResponse200DataProps


T = TypeVar("T", bound="GetMetaEntityResponse200Data")


@_attrs_define
class GetMetaEntityResponse200Data:
    """
    Attributes:
        props (Union[Unset, GetMetaEntityResponse200DataProps]):
    """

    props: Union[Unset, "GetMetaEntityResponse200DataProps"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        props: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.props, Unset):
            props = self.props.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if props is not UNSET:
            field_dict["props"] = props

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_meta_entity_response_200_data_props import GetMetaEntityResponse200DataProps

        d = src_dict.copy()
        _props = d.pop("props", UNSET)
        props: Union[Unset, GetMetaEntityResponse200DataProps]
        if isinstance(_props, Unset):
            props = UNSET
        else:
            props = GetMetaEntityResponse200DataProps.from_dict(_props)

        get_meta_entity_response_200_data = cls(
            props=props,
        )

        get_meta_entity_response_200_data.additional_properties = d
        return get_meta_entity_response_200_data

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
