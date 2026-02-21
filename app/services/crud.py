from sqlalchemy.orm import Session
from ..schemas import (
                        ResourceCreate, ResourceRead, ResourceUpdate,
                        BookCreate, BookRead, BookUpdate
                )
from database.models import Resource, Booking, BookingHistory
from fastapi import HTTPException, status
import enum
from datetime import datetime

# resorce
def create_resource(db: Session, resource: ResourceCreate):
    new_resource = Resource(
        name=resource.name,
        description=resource.description,
        resource_type=resource.resource_type.value,
        capacity=resource.capacity
    )
    db.add(new_resource)
    db.commit()
    db.refresh(new_resource)
    return new_resource


def get_resources(db: Session):
    return db.query(Resource).filter(Resource.is_active == True).all()


def resources_get_by_id(db: Session, resource_id: int):
    return db.query(Resource).filter(Resource.id == resource_id).first()


def updated_resource_by_id(db: Session, resource_id: int, resource_data: ResourceUpdate):
    db_resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not db_resource:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not found')
    if not db_resource.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='invalid resource')
    update_data = resource_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_resource, field, value)
    db.commit()
    db.refresh(db_resource)
    return db_resource


def deleted_resource_by_id(db: Session, resource_id: int):
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not found')
    if not resource.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='invalid resource')
    resource.is_active = False
    db.commit()
    db.refresh(resource)
    return {"detail": "Resource deactivated"}


#book

class BookingStatus(enum.Enum):
    pending = "pending"
    approved = "approved"
    cancelled = "cancelled"


def create_book(db: Session, book: BookCreate):
    new_book = Booking(
        start_time=book.start_time,
        end_time=book.end_time,
        status=book.status,
        comment=book.comment,
        resource_id=book.resource_id
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


def get_book(db: Session):
    return db.query(Booking).all()


def get_book_by_id(db: Session, book_id: int):
    return db.query(Booking).filter(Booking.id == book_id).first()


def updated_book_by_id(db: Session, book_id: int, book_data: BookUpdate):
    db_book = db.query(Booking).filter(Booking.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not found')
    if not db_book.resource.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Resource is inactive')
    old_status = db_book.status
    update_data = book_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_book, field, value)

    if 'status' in update_data and old_status != db_book.status:
        history = BookingHistory(
            old_status=old_status,
            new_status=db_book.status,
            changed_at=datetime.utcnow()
        )
        db.add(history)
    db.commit()
    db.refresh(db_book)
    return db_book


def cancelled_book_by_id(db: Session, book_id: int):
    db_book = db.query(Booking).filter(Booking.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail='Booking not found')
    if not db_book.resource.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Resource is inactive")
    if db_book.status == BookingStatus.cancelled.value:
        raise HTTPException(status_code=400, detail='Booking already cancelled')

    old_status = db_book.status
    db_book.status = BookingStatus.cancelled.value 

    history = BookingHistory(
        old_status=old_status,
        new_status=BookingStatus.cancelled.value,
        changed_at=datetime.utcnow()
    )
    db.add(history)
    db.commit()
    db.refresh(db_book)
    return {"detail": "Booking cancelled"}
