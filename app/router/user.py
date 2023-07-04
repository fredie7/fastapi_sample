from .. import models,schemas,utils,oauth2
from fastapi import Depends,status,FastAPI,Response,HTTPException,Depends,APIRouter
from typing import List
from sqlalchemy.orm import Session
from ..database import engine,get_db

router = APIRouter(
    tags=["Users"]
)
# router = APIRouter(prefix="/posts")


@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
# def createUser(user: schemas.UserCreate, db: Session=Depends(get_db),get_current_user: int= Depends(oauth2.get_current_user)):
def createUser(user: schemas.UserCreate, db: Session=Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    user = models.User(**user.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/users/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def getUser(id: int, db: Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user with id {id} does not exist")
    return user