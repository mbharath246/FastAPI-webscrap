from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database.connection import get_db
from src.database import models, schemas
from src.auth import hashing


router = APIRouter(
    prefix="/user",
    tags=['Users'],
)


@router.get('/', response_model=list[models.User], status_code=status.HTTP_200_OK)
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(schemas.User).all()
    if users:
        return users
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Details Not Found")


@router.get('/get-user-id', status_code=status.HTTP_200_OK)
def get_user_by_id(id:int, db:Session = Depends(get_db)):
    user = db.query(schemas.User).filter(schemas.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Details Not Found")
    return user   


@router.post('/create', response_model=models.User, status_code=status.HTTP_201_CREATED)
def create_user(request: models.UserIn, db: Session = Depends(get_db)):
    username = db.query(schemas.User).filter(schemas.User.username == request.username).first()
    if username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User Already Exists")
    password = hashing.get_hashed_password(request.password)
    new_user = schemas.User(name=request.name,phone=request.phone,username=request.username.lower(),password=password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.put('/update/{old_username}', status_code=status.HTTP_201_CREATED)
def update_user(old_username:str, new_username:str, new_password:str, db: Session = Depends(get_db)):
    user = db.query(schemas.User).filter(schemas.User.username == old_username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User Details Not Found")
    user.username = new_username.lower()
    user.password = hashing.get_hashed_password(new_password)
    db.commit()
    return {"message":"Details Updated"}


@router.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id:int, db: Session = Depends(get_db)):
    user = db.query(schemas.User).filter(schemas.User.id == id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User DetailsNot Found")
    user.delete()
    return {"message":"user deleted sucessfully"}