from fastapi import HTTPException,Depends,status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError,jwt
from datetime import datetime,timedelta
from . import schemas
from .config import settings

oath2_scheme=OAuth2PasswordBearer(tokenUrl="login")


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES =60


#not best understanding all of these functions and what does it import or what does it contain

# is the three functions are connected with each other because in verification how the id is the comparing unit


def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt
    

def verify_access_token(token:str,credentials_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])

        id:int=payload.get("user_id")

        if id is None:
            raise credentials_exception
        
        token_data=schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(token:str=Depends(oath2_scheme)):
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Unable to authorize credentials",
                                        headers={"WWW-Authenticate":"Bearer"})
    
    return verify_access_token(token,credentials_exception)


#so the token is connected to the dependency function which is the 'passwordbearer' so it what makes connection between them or what?
