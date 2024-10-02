from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RunCypherQueryBody")


@_attrs_define
class RunCypherQueryBody:
    """
    Attributes:
        query (Union[Unset, str]):
        include_properties (Union[Unset, bool]):
    """

    query: Union[Unset, str] = UNSET
    include_properties: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        query = self.query

        include_properties = self.include_properties

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if query is not UNSET:
            field_dict["query"] = query
        if include_properties is not UNSET:
            field_dict["include_properties"] = include_properties

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        query = d.pop("query", UNSET)

        include_properties = d.pop("include_properties", UNSET)

        run_cypher_query_body = cls(
            query=query,
            include_properties=include_properties,
        )

        run_cypher_query_body.additional_properties = d
        return run_cypher_query_body

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
