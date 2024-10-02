from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.model_bh_graph_font_icon import ModelBhGraphFontIcon
    from ..models.model_bh_graph_glyph import ModelBhGraphGlyph
    from ..models.model_bh_graph_item_data import ModelBhGraphItemData
    from ..models.model_bh_graph_node_border import ModelBhGraphNodeBorder
    from ..models.model_bh_graph_node_coordinates import ModelBhGraphNodeCoordinates
    from ..models.model_bh_graph_node_halos_item import ModelBhGraphNodeHalosItem
    from ..models.model_bh_graph_node_label import ModelBhGraphNodeLabel


T = TypeVar("T", bound="ModelBhGraphNode")


@_attrs_define
class ModelBhGraphNode:
    """
    Attributes:
        color (Union[Unset, str]):
        fade (Union[Unset, bool]):
        data (Union[Unset, ModelBhGraphItemData]):
        glyphs (Union[Unset, List['ModelBhGraphGlyph']]):
        border (Union[Unset, ModelBhGraphNodeBorder]):
        coordinates (Union[Unset, ModelBhGraphNodeCoordinates]):
        cutout (Union[Unset, bool]):
        font_icon (Union[Unset, ModelBhGraphFontIcon]):
        halos (Union[Unset, List['ModelBhGraphNodeHalosItem']]):
        image (Union[Unset, str]):
        label (Union[Unset, ModelBhGraphNodeLabel]):
        shape (Union[Unset, str]):
        size (Union[Unset, int]):
    """

    color: Union[Unset, str] = UNSET
    fade: Union[Unset, bool] = UNSET
    data: Union[Unset, "ModelBhGraphItemData"] = UNSET
    glyphs: Union[Unset, List["ModelBhGraphGlyph"]] = UNSET
    border: Union[Unset, "ModelBhGraphNodeBorder"] = UNSET
    coordinates: Union[Unset, "ModelBhGraphNodeCoordinates"] = UNSET
    cutout: Union[Unset, bool] = UNSET
    font_icon: Union[Unset, "ModelBhGraphFontIcon"] = UNSET
    halos: Union[Unset, List["ModelBhGraphNodeHalosItem"]] = UNSET
    image: Union[Unset, str] = UNSET
    label: Union[Unset, "ModelBhGraphNodeLabel"] = UNSET
    shape: Union[Unset, str] = UNSET
    size: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        color = self.color

        fade = self.fade

        data: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.data, Unset):
            data = self.data.to_dict()

        glyphs: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.glyphs, Unset):
            glyphs = []
            for glyphs_item_data in self.glyphs:
                glyphs_item = glyphs_item_data.to_dict()
                glyphs.append(glyphs_item)

        border: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.border, Unset):
            border = self.border.to_dict()

        coordinates: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.coordinates, Unset):
            coordinates = self.coordinates.to_dict()

        cutout = self.cutout

        font_icon: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.font_icon, Unset):
            font_icon = self.font_icon.to_dict()

        halos: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.halos, Unset):
            halos = []
            for halos_item_data in self.halos:
                halos_item = halos_item_data.to_dict()
                halos.append(halos_item)

        image = self.image

        label: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.label, Unset):
            label = self.label.to_dict()

        shape = self.shape

        size = self.size

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if color is not UNSET:
            field_dict["color"] = color
        if fade is not UNSET:
            field_dict["fade"] = fade
        if data is not UNSET:
            field_dict["data"] = data
        if glyphs is not UNSET:
            field_dict["glyphs"] = glyphs
        if border is not UNSET:
            field_dict["border"] = border
        if coordinates is not UNSET:
            field_dict["coordinates"] = coordinates
        if cutout is not UNSET:
            field_dict["cutout"] = cutout
        if font_icon is not UNSET:
            field_dict["fontIcon"] = font_icon
        if halos is not UNSET:
            field_dict["halos"] = halos
        if image is not UNSET:
            field_dict["image"] = image
        if label is not UNSET:
            field_dict["label"] = label
        if shape is not UNSET:
            field_dict["shape"] = shape
        if size is not UNSET:
            field_dict["size"] = size

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.model_bh_graph_font_icon import ModelBhGraphFontIcon
        from ..models.model_bh_graph_glyph import ModelBhGraphGlyph
        from ..models.model_bh_graph_item_data import ModelBhGraphItemData
        from ..models.model_bh_graph_node_border import ModelBhGraphNodeBorder
        from ..models.model_bh_graph_node_coordinates import ModelBhGraphNodeCoordinates
        from ..models.model_bh_graph_node_halos_item import ModelBhGraphNodeHalosItem
        from ..models.model_bh_graph_node_label import ModelBhGraphNodeLabel

        d = src_dict.copy()
        color = d.pop("color", UNSET)

        fade = d.pop("fade", UNSET)

        _data = d.pop("data", UNSET)
        data: Union[Unset, ModelBhGraphItemData]
        if isinstance(_data, Unset):
            data = UNSET
        else:
            data = ModelBhGraphItemData.from_dict(_data)

        glyphs = []
        _glyphs = d.pop("glyphs", UNSET)
        for glyphs_item_data in _glyphs or []:
            glyphs_item = ModelBhGraphGlyph.from_dict(glyphs_item_data)

            glyphs.append(glyphs_item)

        _border = d.pop("border", UNSET)
        border: Union[Unset, ModelBhGraphNodeBorder]
        if isinstance(_border, Unset):
            border = UNSET
        else:
            border = ModelBhGraphNodeBorder.from_dict(_border)

        _coordinates = d.pop("coordinates", UNSET)
        coordinates: Union[Unset, ModelBhGraphNodeCoordinates]
        if isinstance(_coordinates, Unset):
            coordinates = UNSET
        else:
            coordinates = ModelBhGraphNodeCoordinates.from_dict(_coordinates)

        cutout = d.pop("cutout", UNSET)

        _font_icon = d.pop("fontIcon", UNSET)
        font_icon: Union[Unset, ModelBhGraphFontIcon]
        if isinstance(_font_icon, Unset):
            font_icon = UNSET
        else:
            font_icon = ModelBhGraphFontIcon.from_dict(_font_icon)

        halos = []
        _halos = d.pop("halos", UNSET)
        for halos_item_data in _halos or []:
            halos_item = ModelBhGraphNodeHalosItem.from_dict(halos_item_data)

            halos.append(halos_item)

        image = d.pop("image", UNSET)

        _label = d.pop("label", UNSET)
        label: Union[Unset, ModelBhGraphNodeLabel]
        if isinstance(_label, Unset):
            label = UNSET
        else:
            label = ModelBhGraphNodeLabel.from_dict(_label)

        shape = d.pop("shape", UNSET)

        size = d.pop("size", UNSET)

        model_bh_graph_node = cls(
            color=color,
            fade=fade,
            data=data,
            glyphs=glyphs,
            border=border,
            coordinates=coordinates,
            cutout=cutout,
            font_icon=font_icon,
            halos=halos,
            image=image,
            label=label,
            shape=shape,
            size=size,
        )

        model_bh_graph_node.additional_properties = d
        return model_bh_graph_node

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
