from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_asset_group_members_response_200_data import ListAssetGroupMembersResponse200Data


T = TypeVar("T", bound="ListAssetGroupMembersResponse200")


@_attrs_define
class ListAssetGroupMembersResponse200:
    """
    Attributes:
        count (Union[Unset, int]): The total number of results.
        skip (Union[Unset, int]): The number of items to skip in a paginated response.
        limit (Union[Unset, int]): The limit of results requested by the client.
        data (Union[Unset, ListAssetGroupMembersResponse200Data]):
    """

    count: Union[Unset, int] = UNSET
    skip: Union[Unset, int] = UNSET
    limit: Union[Unset, int] = UNSET
    data: Union[Unset, "ListAssetGroupMembersResponse200Data"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        count = self.count

        skip = self.skip

        limit = self.limit

        data: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.data, Unset):
            data = self.data.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if count is not UNSET:
            field_dict["count"] = count
        if skip is not UNSET:
            field_dict["skip"] = skip
        if limit is not UNSET:
            field_dict["limit"] = limit
        if data is not UNSET:
            field_dict["data"] = data

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_asset_group_members_response_200_data import ListAssetGroupMembersResponse200Data

        d = src_dict.copy()
        count = d.pop("count", UNSET)

        skip = d.pop("skip", UNSET)

        limit = d.pop("limit", UNSET)

        _data = d.pop("data", UNSET)
        data: Union[Unset, ListAssetGroupMembersResponse200Data]
        if isinstance(_data, Unset):
            data = UNSET
        else:
            data = ListAssetGroupMembersResponse200Data.from_dict(_data)

        list_asset_group_members_response_200 = cls(
            count=count,
            skip=skip,
            limit=limit,
            data=data,
        )

        list_asset_group_members_response_200.additional_properties = d
        return list_asset_group_members_response_200

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
