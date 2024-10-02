from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.model_file_upload_job import ModelFileUploadJob


T = TypeVar("T", bound="ListFileUploadJobsResponse200")


@_attrs_define
class ListFileUploadJobsResponse200:
    """
    Attributes:
        count (Union[Unset, int]): The total number of results.
        skip (Union[Unset, int]): The number of items to skip in a paginated response.
        limit (Union[Unset, int]): The limit of results requested by the client.
        data (Union[Unset, List['ModelFileUploadJob']]):
    """

    count: Union[Unset, int] = UNSET
    skip: Union[Unset, int] = UNSET
    limit: Union[Unset, int] = UNSET
    data: Union[Unset, List["ModelFileUploadJob"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        count = self.count

        skip = self.skip

        limit = self.limit

        data: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.data, Unset):
            data = []
            for data_item_data in self.data:
                data_item = data_item_data.to_dict()
                data.append(data_item)

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
        from ..models.model_file_upload_job import ModelFileUploadJob

        d = src_dict.copy()
        count = d.pop("count", UNSET)

        skip = d.pop("skip", UNSET)

        limit = d.pop("limit", UNSET)

        data = []
        _data = d.pop("data", UNSET)
        for data_item_data in _data or []:
            data_item = ModelFileUploadJob.from_dict(data_item_data)

            data.append(data_item)

        list_file_upload_jobs_response_200 = cls(
            count=count,
            skip=skip,
            limit=limit,
            data=data,
        )

        list_file_upload_jobs_response_200.additional_properties = d
        return list_file_upload_jobs_response_200

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
