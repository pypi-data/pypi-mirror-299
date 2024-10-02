import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.model_ad_data_quality_aggregation import ModelAdDataQualityAggregation
    from ..models.model_azure_data_quality_aggregation import ModelAzureDataQualityAggregation


T = TypeVar("T", bound="ApiResponseDataQualityPlatformAggregateData")


@_attrs_define
class ApiResponseDataQualityPlatformAggregateData:
    """
    Attributes:
        count (Union[Unset, int]): The total number of results.
        skip (Union[Unset, int]): The number of items to skip in a paginated response.
        limit (Union[Unset, int]): The limit of results requested by the client.
        start (Union[Unset, datetime.datetime]): The RFC-3339 timestamp to describe the beginning of a time range
        end (Union[Unset, datetime.datetime]): The RFC-3339 timestamp to describe the end of a time range
        data (Union[Unset, List[Union['ModelAdDataQualityAggregation', 'ModelAzureDataQualityAggregation']]]):
    """

    count: Union[Unset, int] = UNSET
    skip: Union[Unset, int] = UNSET
    limit: Union[Unset, int] = UNSET
    start: Union[Unset, datetime.datetime] = UNSET
    end: Union[Unset, datetime.datetime] = UNSET
    data: Union[Unset, List[Union["ModelAdDataQualityAggregation", "ModelAzureDataQualityAggregation"]]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.model_ad_data_quality_aggregation import ModelAdDataQualityAggregation

        count = self.count

        skip = self.skip

        limit = self.limit

        start: Union[Unset, str] = UNSET
        if not isinstance(self.start, Unset):
            start = self.start.isoformat()

        end: Union[Unset, str] = UNSET
        if not isinstance(self.end, Unset):
            end = self.end.isoformat()

        data: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.data, Unset):
            data = []
            for data_item_data in self.data:
                data_item: Dict[str, Any]
                if isinstance(data_item_data, ModelAdDataQualityAggregation):
                    data_item = data_item_data.to_dict()
                else:
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
        if start is not UNSET:
            field_dict["start"] = start
        if end is not UNSET:
            field_dict["end"] = end
        if data is not UNSET:
            field_dict["data"] = data

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.model_ad_data_quality_aggregation import ModelAdDataQualityAggregation
        from ..models.model_azure_data_quality_aggregation import ModelAzureDataQualityAggregation

        d = src_dict.copy()
        count = d.pop("count", UNSET)

        skip = d.pop("skip", UNSET)

        limit = d.pop("limit", UNSET)

        _start = d.pop("start", UNSET)
        start: Union[Unset, datetime.datetime]
        if isinstance(_start, Unset):
            start = UNSET
        else:
            start = isoparse(_start)

        _end = d.pop("end", UNSET)
        end: Union[Unset, datetime.datetime]
        if isinstance(_end, Unset):
            end = UNSET
        else:
            end = isoparse(_end)

        data = []
        _data = d.pop("data", UNSET)
        for data_item_data in _data or []:

            def _parse_data_item(
                data: object,
            ) -> Union["ModelAdDataQualityAggregation", "ModelAzureDataQualityAggregation"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    data_item_type_0 = ModelAdDataQualityAggregation.from_dict(data)

                    return data_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                data_item_type_1 = ModelAzureDataQualityAggregation.from_dict(data)

                return data_item_type_1

            data_item = _parse_data_item(data_item_data)

            data.append(data_item)

        api_response_data_quality_platform_aggregate_data = cls(
            count=count,
            skip=skip,
            limit=limit,
            start=start,
            end=end,
            data=data,
        )

        api_response_data_quality_platform_aggregate_data.additional_properties = d
        return api_response_data_quality_platform_aggregate_data

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
