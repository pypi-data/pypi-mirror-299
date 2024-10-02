from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.enum_client_type import EnumClientType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.model_client_schedule import ModelClientSchedule


T = TypeVar("T", bound="CreateClientBody")


@_attrs_define
class CreateClientBody:
    """
    Attributes:
        name (Union[Unset, str]):
        domain_controller (Union[Unset, str]):
        type (Union[Unset, EnumClientType]): This enum describes the collector client type.
        events (Union[Unset, List['ModelClientSchedule']]):
    """

    name: Union[Unset, str] = UNSET
    domain_controller: Union[Unset, str] = UNSET
    type: Union[Unset, EnumClientType] = UNSET
    events: Union[Unset, List["ModelClientSchedule"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        domain_controller = self.domain_controller

        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        events: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.events, Unset):
            events = []
            for events_item_data in self.events:
                events_item = events_item_data.to_dict()
                events.append(events_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if domain_controller is not UNSET:
            field_dict["domain_controller"] = domain_controller
        if type is not UNSET:
            field_dict["type"] = type
        if events is not UNSET:
            field_dict["events"] = events

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.model_client_schedule import ModelClientSchedule

        d = src_dict.copy()
        name = d.pop("name", UNSET)

        domain_controller = d.pop("domain_controller", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, EnumClientType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = EnumClientType(_type)

        events = []
        _events = d.pop("events", UNSET)
        for events_item_data in _events or []:
            events_item = ModelClientSchedule.from_dict(events_item_data)

            events.append(events_item)

        create_client_body = cls(
            name=name,
            domain_controller=domain_controller,
            type=type,
            events=events,
        )

        create_client_body.additional_properties = d
        return create_client_body

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
