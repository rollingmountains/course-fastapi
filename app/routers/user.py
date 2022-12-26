from fastapi import FastAPI, Response, status, HTTPException, APIRouter
from fastapi.params import Body, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, utils, oauth2
from ..database import get_db 


router = APIRouter(prefix="/users", tags=['users'])




@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.CreateUser ,db: Session = Depends(get_db)):

    # hashing the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db), get_user: int=(Depends(oauth2.get_current_user))):
    get_user = db.query(models.User).filter(models.User.id == id).first()

    if get_user == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id {id} was not found." )

    return get_user

@router.get("/", response_model=List[schemas.UserResponse])
def get_users(db: Session = Depends(get_db), get_user: int=(Depends(oauth2.get_current_user))):
    get_users = db.query(models.User).all()
    return get_users


