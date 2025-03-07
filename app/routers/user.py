from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from .. import models,schemas,utils
from ..database import engine,get_db


router=APIRouter(
    tags=["User"]
)

@router.post("/users",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate,db:Session=Depends(get_db)):
    hashed_password=utils.hash(user.password)
    user.password=hashed_password
    new_user=models.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



@router.get("/user/{id}",response_model=schemas.UserOut)
def get_user(id:int,db:Session=Depends(get_db)):
    #note : when adding '.first' in return statement it make internal error while when putting it at first it solved the internal server error and return the 
    #the wanted error handling
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id {id} is not found")
    return user

    