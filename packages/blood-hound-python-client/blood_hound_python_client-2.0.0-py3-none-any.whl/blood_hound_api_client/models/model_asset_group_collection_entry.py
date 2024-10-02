import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.model_asset_group_collection_entry_properties import ModelAssetGroupCollectionEntryProperties
    from ..models.null_time import NullTime


T = TypeVar("T", bound="ModelAssetGroupCollectionEntry")


@_attrs_define
class ModelAssetGroupCollectionEntry:
    """
    Attributes:
        id (Union[Unset, int]): This is the unique identifier for this object.
        created_at (Union[Unset, datetime.datetime]):
        updated_at (Union[Unset, datetime.datetime]):
        deleted_at (Union[Unset, NullTime]):
        asset_group_collection_id (Union[Unset, int]):
        object_id (Union[Unset, str]):
        node_label (Union[Unset, str]):
        properties (Union[Unset, ModelAssetGroupCollectionEntryProperties]):
    """

    id: Union[Unset, int] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    deleted_at: Union[Unset, "NullTime"] = UNSET
    asset_group_collection_id: Union[Unset, int] = UNSET
    object_id: Union[Unset, str] = UNSET
    node_label: Union[Unset, str] = UNSET
    properties: Union[Unset, "ModelAssetGroupCollectionEntryProperties"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        deleted_at: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.deleted_at, Unset):
            deleted_at = self.deleted_at.to_dict()

        asset_group_collection_id = self.asset_group_collection_id

        object_id = self.object_id

        node_label = self.node_label

        properties: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.properties, Unset):
            properties = self.properties.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at
        if deleted_at is not UNSET:
            field_dict["deleted_at"] = deleted_at
        if asset_group_collection_id is not UNSET:
            field_dict["asset_group_collection_id"] = asset_group_collection_id
        if object_id is not UNSET:
            field_dict["object_id"] = object_id
        if node_label is not UNSET:
            field_dict["node_label"] = node_label
        if properties is not UNSET:
            field_dict["properties"] = properties

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.model_asset_group_collection_entry_properties import ModelAssetGroupCollectionEntryProperties
        from ..models.null_time import NullTime

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        _created_at = d.pop("created_at", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        _updated_at = d.pop("updated_at", UNSET)
        updated_at: Union[Unset, datetime.datetime]
        if isinstance(_updated_at, Unset):
            updated_at = UNSET
        else:
            updated_at = isoparse(_updated_at)

        _deleted_at = d.pop("deleted_at", UNSET)
        deleted_at: Union[Unset, NullTime]
        if isinstance(_deleted_at, Unset):
            deleted_at = UNSET
        else:
            deleted_at = NullTime.from_dict(_deleted_at)

        asset_group_collection_id = d.pop("asset_group_collection_id", UNSET)

        object_id = d.pop("object_id", UNSET)

        node_label = d.pop("node_label", UNSET)

        _properties = d.pop("properties", UNSET)
        properties: Union[Unset, ModelAssetGroupCollectionEntryProperties]
        if isinstance(_properties, Unset):
            properties = UNSET
        else:
            properties = ModelAssetGroupCollectionEntryProperties.from_dict(_properties)

        model_asset_group_collection_entry = cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            deleted_at=deleted_at,
            asset_group_collection_id=asset_group_collection_id,
            object_id=object_id,
            node_label=node_label,
            properties=properties,
        )

        model_asset_group_collection_entry.additional_properties = d
        return model_asset_group_collection_entry

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
