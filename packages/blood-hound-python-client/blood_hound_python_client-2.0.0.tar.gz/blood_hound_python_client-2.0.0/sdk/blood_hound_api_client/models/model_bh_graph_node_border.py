from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelBhGraphNodeBorder")


@_attrs_define
class ModelBhGraphNodeBorder:
    """
    Attributes:
        color (Union[Unset, str]):
        line_style (Union[Unset, str]):
        width (Union[Unset, int]):
    """

    color: Union[Unset, str] = UNSET
    line_style: Union[Unset, str] = UNSET
    width: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        color = self.color

        line_style = self.line_style

        width = self.width

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if color is not UNSET:
            field_dict["color"] = color
        if line_style is not UNSET:
            field_dict["lineStyle"] = line_style
        if width is not UNSET:
            field_dict["width"] = width

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        color = d.pop("color", UNSET)

        line_style = d.pop("lineStyle", UNSET)

        width = d.pop("width", UNSET)

        model_bh_graph_node_border = cls(
            color=color,
            line_style=line_style,
            width=width,
        )

        model_bh_graph_node_border.additional_properties = d
        return model_bh_graph_node_border

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
