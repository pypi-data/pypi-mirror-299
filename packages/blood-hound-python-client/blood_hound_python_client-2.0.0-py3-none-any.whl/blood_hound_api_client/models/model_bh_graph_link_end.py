from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.model_bh_graph_glyph import ModelBhGraphGlyph
    from ..models.model_bh_graph_label import ModelBhGraphLabel


T = TypeVar("T", bound="ModelBhGraphLinkEnd")


@_attrs_define
class ModelBhGraphLinkEnd:
    """
    Attributes:
        arrow (Union[Unset, bool]):
        back_off (Union[Unset, int]):
        color (Union[Unset, str]):
        glyphs (Union[Unset, List['ModelBhGraphGlyph']]):
        label (Union[Unset, ModelBhGraphLabel]):
    """

    arrow: Union[Unset, bool] = UNSET
    back_off: Union[Unset, int] = UNSET
    color: Union[Unset, str] = UNSET
    glyphs: Union[Unset, List["ModelBhGraphGlyph"]] = UNSET
    label: Union[Unset, "ModelBhGraphLabel"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        arrow = self.arrow

        back_off = self.back_off

        color = self.color

        glyphs: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.glyphs, Unset):
            glyphs = []
            for glyphs_item_data in self.glyphs:
                glyphs_item = glyphs_item_data.to_dict()
                glyphs.append(glyphs_item)

        label: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.label, Unset):
            label = self.label.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if arrow is not UNSET:
            field_dict["arrow"] = arrow
        if back_off is not UNSET:
            field_dict["backOff"] = back_off
        if color is not UNSET:
            field_dict["color"] = color
        if glyphs is not UNSET:
            field_dict["glyphs"] = glyphs
        if label is not UNSET:
            field_dict["label"] = label

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.model_bh_graph_glyph import ModelBhGraphGlyph
        from ..models.model_bh_graph_label import ModelBhGraphLabel

        d = src_dict.copy()
        arrow = d.pop("arrow", UNSET)

        back_off = d.pop("backOff", UNSET)

        color = d.pop("color", UNSET)

        glyphs = []
        _glyphs = d.pop("glyphs", UNSET)
        for glyphs_item_data in _glyphs or []:
            glyphs_item = ModelBhGraphGlyph.from_dict(glyphs_item_data)

            glyphs.append(glyphs_item)

        _label = d.pop("label", UNSET)
        label: Union[Unset, ModelBhGraphLabel]
        if isinstance(_label, Unset):
            label = UNSET
        else:
            label = ModelBhGraphLabel.from_dict(_label)

        model_bh_graph_link_end = cls(
            arrow=arrow,
            back_off=back_off,
            color=color,
            glyphs=glyphs,
            label=label,
        )

        model_bh_graph_link_end.additional_properties = d
        return model_bh_graph_link_end

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
