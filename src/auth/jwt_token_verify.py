from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer
from jose import jwt

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

class JwtBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auto_error = self.auto_error
        credentials = await super().__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or Expired Token")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or Expired Token")
            return credentials.credentials
        else:
            if auto_error:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or Expired Token")
            return None

    def verify_jwt(self, jwtoken: str):
        payload = jwt.decode(jwtoken, SECRET_KEY, algorithms=[ALGORITHM])
        user = payload.get("uname")
        if not user:
            return False
        return True
        