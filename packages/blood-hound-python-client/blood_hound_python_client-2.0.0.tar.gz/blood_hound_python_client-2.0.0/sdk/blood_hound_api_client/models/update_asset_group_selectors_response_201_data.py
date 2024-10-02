from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.model_asset_group_selector import ModelAssetGroupSelector


T = TypeVar("T", bound="UpdateAssetGroupSelectorsResponse201Data")


@_attrs_define
class UpdateAssetGroupSelectorsResponse201Data:
    """
    Attributes:
        added_selectors (Union[Unset, List['ModelAssetGroupSelector']]):
        removed_selectors (Union[Unset, List['ModelAssetGroupSelector']]):
    """

    added_selectors: Union[Unset, List["ModelAssetGroupSelector"]] = UNSET
    removed_selectors: Union[Unset, List["ModelAssetGroupSelector"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        added_selectors: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.added_selectors, Unset):
            added_selectors = []
            for added_selectors_item_data in self.added_selectors:
                added_selectors_item = added_selectors_item_data.to_dict()
                added_selectors.append(added_selectors_item)

        removed_selectors: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.removed_selectors, Unset):
            removed_selectors = []
            for removed_selectors_item_data in self.removed_selectors:
                removed_selectors_item = removed_selectors_item_data.to_dict()
                removed_selectors.append(removed_selectors_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if added_selectors is not UNSET:
            field_dict["added_selectors"] = added_selectors
        if removed_selectors is not UNSET:
            field_dict["removed_selectors"] = removed_selectors

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.model_asset_group_selector import ModelAssetGroupSelector

        d = src_dict.copy()
        added_selectors = []
        _added_selectors = d.pop("added_selectors", UNSET)
        for added_selectors_item_data in _added_selectors or []:
            added_selectors_item = ModelAssetGroupSelector.from_dict(added_selectors_item_data)

            added_selectors.append(added_selectors_item)

        removed_selectors = []
        _removed_selectors = d.pop("removed_selectors", UNSET)
        for removed_selectors_item_data in _removed_selectors or []:
            removed_selectors_item = ModelAssetGroupSelector.from_dict(removed_selectors_item_data)

            removed_selectors.append(removed_selectors_item)

        update_asset_group_selectors_response_201_data = cls(
            added_selectors=added_selectors,
            removed_selectors=removed_selectors,
        )

        update_asset_group_selectors_response_201_data.additional_properties = d
        return update_asset_group_selectors_response_201_data

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
