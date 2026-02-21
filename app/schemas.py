from pydantic import BaseModel, ConfigDict
from datetime import datetime
from enum import StrEnum
from typing import Optional



#resource

class ResourceTypes(StrEnum):
    room = "room"
    desk = "desk"
    equipment = "equipment"


class ResourceCreate(BaseModel):
    name: str
    description: str
    resource_type: ResourceTypes = ResourceTypes.room
    capacity: int


class ResourceRead(BaseModel):
    id: int
    name: str
    description: str
    resource_type: ResourceTypes 
    capacity: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ResourceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    resource_type: Optional[ResourceTypes] = None
    capacity: Optional[int] = None
    is_active: Optional[bool] = None



#booking

class BookingStatus(StrEnum):
    pending = "pending"
    approved = "approved"
    cancelled = "cancelled"


class BookCreate(BaseModel):
    resource_id: int
    start_time: datetime
    end_time: datetime
    status: BookingStatus = BookingStatus.pending
    comment: Optional[str] = ''


class BookRead(BaseModel):
    id: int
    resource_id: int
    start_time: datetime
    end_time: datetime
    status: BookingStatus
    comment: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BookUpdate(BaseModel):
    status: Optional[BookingStatus] = None
    comment: Optional[str] = None