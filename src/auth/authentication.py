from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.database.connection import get_db
from src.database import schemas
from src.auth.hashing import verify_hash_password
from src.auth.token_access import create_access_token
from src.database.models import Token


router = APIRouter(
    tags=["Authentication"]
)


@router.post('/token')
def user_login(request: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    user = db.query(schemas.User).filter(schemas.User.username == request.username.lower()).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Login Credentials")
    if not verify_hash_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect Password")
    
    # create a token
    token = create_access_token(data={"uname":user.username})
    return Token(access_token=token, token_type="Bearer")
