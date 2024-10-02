from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelBhGraphNodeLabel")


@_attrs_define
class ModelBhGraphNodeLabel:
    """
    Attributes:
        background_color (Union[Unset, str]):
        bold (Union[Unset, bool]):
        center (Union[Unset, bool]):
        color (Union[Unset, str]):
        font_family (Union[Unset, str]):
        font_size (Union[Unset, int]):
        text (Union[Unset, str]):
    """

    background_color: Union[Unset, str] = UNSET
    bold: Union[Unset, bool] = UNSET
    center: Union[Unset, bool] = UNSET
    color: Union[Unset, str] = UNSET
    font_family: Union[Unset, str] = UNSET
    font_size: Union[Unset, int] = UNSET
    text: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        background_color = self.background_color

        bold = self.bold

        center = self.center

        color = self.color

        font_family = self.font_family

        font_size = self.font_size

        text = self.text

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if background_color is not UNSET:
            field_dict["backgroundColor"] = background_color
        if bold is not UNSET:
            field_dict["bold"] = bold
        if center is not UNSET:
            field_dict["center"] = center
        if color is not UNSET:
            field_dict["color"] = color
        if font_family is not UNSET:
            field_dict["fontFamily"] = font_family
        if font_size is not UNSET:
            field_dict["fontSize"] = font_size
        if text is not UNSET:
            field_dict["text"] = text

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        background_color = d.pop("backgroundColor", UNSET)

        bold = d.pop("bold", UNSET)

        center = d.pop("center", UNSET)

        color = d.pop("color", UNSET)

        font_family = d.pop("fontFamily", UNSET)

        font_size = d.pop("fontSize", UNSET)

        text = d.pop("text", UNSET)

        model_bh_graph_node_label = cls(
            background_color=background_color,
            bold=bold,
            center=center,
            color=color,
            font_family=font_family,
            font_size=font_size,
            text=text,
        )

        model_bh_graph_node_label.additional_properties = d
        return model_bh_graph_node_label

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
