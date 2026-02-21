from fastapi import FastAPI, HTTPException, status, Depends
from app.services.crud import (
    create_book, get_book, get_book_by_id, updated_book_by_id, 
    deleted_resource_by_id, create_resource, get_resources, 
    resources_get_by_id, updated_resource_by_id, cancelled_book_by_id
)
from database.db import get_db, engine
from database.models import Base
from app.schemas import (
    ResourceCreate, ResourceRead, ResourceUpdate,
    BookCreate, BookRead, BookUpdate
)
import uvicorn
from sqlalchemy.orm import Session


Base.metadata.create_all(engine)

app = FastAPI()

#resource
@app.post('/resource', response_model=ResourceRead)
def post_resource(resource: ResourceCreate, db: Session = Depends(get_db)):
    return create_resource(db, resource)


@app.get('/resource', response_model=list[ResourceRead])
def get_resource(db: Session = Depends(get_db)):
    return get_resources(db)



@app.get('/resource/{resource_id}', response_model=ResourceRead)
def get_resource_by_id(resource_id: int, db: Session = Depends(get_db)):
    resourc = resources_get_by_id(db, resource_id)
    if not resourc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not found')
    return resourc


@app.put('/resource/{resource_id}', response_model=ResourceRead)
def update_resource(resource_id: int, resource: ResourceUpdate, db: Session = Depends(get_db)):
    return updated_resource_by_id(db, resource_id, resource)


@app.delete('/resource/{resource_id}')
def deleted_resource(resource_id: int, db: Session = Depends(get_db)):
    return deleted_resource_by_id(db, resource_id)


#book

@app.post('/book', response_model=BookRead)
def post_book(book: BookCreate, db: Session = Depends(get_db)):
    return create_book(db, book)


@app.get('/book', response_model=list[BookRead])
def book_get(db: Session = Depends(get_db)):
    return get_book(db)



@app.get('/book/{book_id}', response_model=BookRead)
def get_booking(book_id: int, db: Session = Depends(get_db)):
    book = get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="not found")
    return book


@app.put('/book/{book_id}', response_model=BookRead)
def update_book(book_id: int, book: BookUpdate, db: Session = Depends(get_db)):
    return updated_book_by_id(db, book_id, book)


@app.post('/book/{book_id}/cancel')
def cancel_booking(book_id: int, db: Session = Depends(get_db)):
    return cancelled_book_by_id(db, book_id)



if __name__ == '__main__':
    uvicorn.run(app=app)
