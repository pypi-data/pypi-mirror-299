from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.model_bh_graph_font_icon import ModelBhGraphFontIcon
    from ..models.model_bh_graph_item_border import ModelBhGraphItemBorder
    from ..models.model_bh_graph_label import ModelBhGraphLabel


T = TypeVar("T", bound="ModelBhGraphGlyph")


@_attrs_define
class ModelBhGraphGlyph:
    """
    Attributes:
        angle (Union[Unset, int]):
        blink (Union[Unset, bool]):
        border (Union[Unset, ModelBhGraphItemBorder]):
        color (Union[Unset, str]):
        font_icon (Union[Unset, ModelBhGraphFontIcon]):
        image (Union[Unset, str]):
        label (Union[Unset, ModelBhGraphLabel]):
        position (Union[Unset, str]):
        radius (Union[Unset, int]):
        size (Union[Unset, int]):
    """

    angle: Union[Unset, int] = UNSET
    blink: Union[Unset, bool] = UNSET
    border: Union[Unset, "ModelBhGraphItemBorder"] = UNSET
    color: Union[Unset, str] = UNSET
    font_icon: Union[Unset, "ModelBhGraphFontIcon"] = UNSET
    image: Union[Unset, str] = UNSET
    label: Union[Unset, "ModelBhGraphLabel"] = UNSET
    position: Union[Unset, str] = UNSET
    radius: Union[Unset, int] = UNSET
    size: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        angle = self.angle

        blink = self.blink

        border: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.border, Unset):
            border = self.border.to_dict()

        color = self.color

        font_icon: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.font_icon, Unset):
            font_icon = self.font_icon.to_dict()

        image = self.image

        label: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.label, Unset):
            label = self.label.to_dict()

        position = self.position

        radius = self.radius

        size = self.size

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if angle is not UNSET:
            field_dict["angle"] = angle
        if blink is not UNSET:
            field_dict["blink"] = blink
        if border is not UNSET:
            field_dict["border"] = border
        if color is not UNSET:
            field_dict["color"] = color
        if font_icon is not UNSET:
            field_dict["fontIcon"] = font_icon
        if image is not UNSET:
            field_dict["image"] = image
        if label is not UNSET:
            field_dict["label"] = label
        if position is not UNSET:
            field_dict["position"] = position
        if radius is not UNSET:
            field_dict["radius"] = radius
        if size is not UNSET:
            field_dict["size"] = size

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.model_bh_graph_font_icon import ModelBhGraphFontIcon
        from ..models.model_bh_graph_item_border import ModelBhGraphItemBorder
        from ..models.model_bh_graph_label import ModelBhGraphLabel

        d = src_dict.copy()
        angle = d.pop("angle", UNSET)

        blink = d.pop("blink", UNSET)

        _border = d.pop("border", UNSET)
        border: Union[Unset, ModelBhGraphItemBorder]
        if isinstance(_border, Unset):
            border = UNSET
        else:
            border = ModelBhGraphItemBorder.from_dict(_border)

        color = d.pop("color", UNSET)

        _font_icon = d.pop("fontIcon", UNSET)
        font_icon: Union[Unset, ModelBhGraphFontIcon]
        if isinstance(_font_icon, Unset):
            font_icon = UNSET
        else:
            font_icon = ModelBhGraphFontIcon.from_dict(_font_icon)

        image = d.pop("image", UNSET)

        _label = d.pop("label", UNSET)
        label: Union[Unset, ModelBhGraphLabel]
        if isinstance(_label, Unset):
            label = UNSET
        else:
            label = ModelBhGraphLabel.from_dict(_label)

        position = d.pop("position", UNSET)

        radius = d.pop("radius", UNSET)

        size = d.pop("size", UNSET)

        model_bh_graph_glyph = cls(
            angle=angle,
            blink=blink,
            border=border,
            color=color,
            font_icon=font_icon,
            image=image,
            label=label,
            position=position,
            radius=radius,
            size=size,
        )

        model_bh_graph_glyph.additional_properties = d
        return model_bh_graph_glyph

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
