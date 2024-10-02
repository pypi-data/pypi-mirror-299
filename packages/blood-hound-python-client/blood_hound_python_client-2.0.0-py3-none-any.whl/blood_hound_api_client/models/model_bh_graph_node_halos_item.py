from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelBhGraphNodeHalosItem")


@_attrs_define
class ModelBhGraphNodeHalosItem:
    """
    Attributes:
        color (Union[Unset, str]):
        radius (Union[Unset, int]):
        width (Union[Unset, int]):
    """

    color: Union[Unset, str] = UNSET
    radius: Union[Unset, int] = UNSET
    width: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        color = self.color

        radius = self.radius

        width = self.width

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if color is not UNSET:
            field_dict["color"] = color
        if radius is not UNSET:
            field_dict["radius"] = radius
        if width is not UNSET:
            field_dict["width"] = width

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        color = d.pop("color", UNSET)

        radius = d.pop("radius", UNSET)

        width = d.pop("width", UNSET)

        model_bh_graph_node_halos_item = cls(
            color=color,
            radius=radius,
            width=width,
        )

        model_bh_graph_node_halos_item.additional_properties = d
        return model_bh_graph_node_halos_item

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
