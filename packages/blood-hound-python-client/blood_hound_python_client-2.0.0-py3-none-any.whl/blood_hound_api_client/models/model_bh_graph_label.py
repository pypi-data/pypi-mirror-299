from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelBhGraphLabel")


@_attrs_define
class ModelBhGraphLabel:
    """
    Attributes:
        bold (Union[Unset, bool]):
        color (Union[Unset, str]):
        font_family (Union[Unset, str]):
        text (Union[Unset, str]):
    """

    bold: Union[Unset, bool] = UNSET
    color: Union[Unset, str] = UNSET
    font_family: Union[Unset, str] = UNSET
    text: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        bold = self.bold

        color = self.color

        font_family = self.font_family

        text = self.text

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if bold is not UNSET:
            field_dict["bold"] = bold
        if color is not UNSET:
            field_dict["color"] = color
        if font_family is not UNSET:
            field_dict["fontFamily"] = font_family
        if text is not UNSET:
            field_dict["text"] = text

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        bold = d.pop("bold", UNSET)

        color = d.pop("color", UNSET)

        font_family = d.pop("fontFamily", UNSET)

        text = d.pop("text", UNSET)

        model_bh_graph_label = cls(
            bold=bold,
            color=color,
            font_family=font_family,
            text=text,
        )

        model_bh_graph_label.additional_properties = d
        return model_bh_graph_label

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
