from sqlalchemy import (
               Column, String, Integer, 
               ForeignKey, Boolean, DateTime, Enum)
from datetime import datetime
from sqlalchemy.orm import Session, DeclarativeBase, relationship
from sqlalchemy import Enum
import enum

class Base(DeclarativeBase):
    pass


class ResourceTypes(enum.Enum):
    room = "room"
    desk = "desk"
    equipment = "equipment"


class BookingStatus(enum.Enum):
    pending = "pending"
    approved = "approved"
    cancelled = "cancelled"


class HistoryStatus(enum.Enum):
    new = "new"
    old = "old"


class UserRole(enum.Enum):
    guest = 'guest'
    manager = 'manager'
    admin = 'admin'


class Resource(Base):
    __tablename__ = 'resource'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    resource_type = Column(Enum(ResourceTypes))
    capacity = Column(Integer)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    bookings = relationship(
    "Booking",
    back_populates="resource",
    cascade="all, delete-orphan"
)
    

class Booking(Base):
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum(BookingStatus, name="bookingstatus"), nullable=False)
    comment = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    user = relationship('User', back_populates='users')
    resource_id = Column(Integer, ForeignKey("resource.id"), nullable=False)
    resource = relationship("Resource", back_populates="bookings")


class BookingHistory(Base):
    __tablename__ = "booking_history"
    
    id = Column(Integer, primary_key=True)
    old_status = Column(
        Enum(BookingStatus, name="bookingstatus"),
        nullable=False
    )
    new_status = Column(
        Enum(BookingStatus, name="bookingstatus"),
        nullable=False
    )
    changed_by_user_id = Column(Integer, ForeignKey('users.id'))
    changed_at = Column(DateTime, default=datetime.utcnow)


