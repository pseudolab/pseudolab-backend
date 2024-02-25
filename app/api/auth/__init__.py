from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

router = APIRouter(prefix="/auth")

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# OAuth2SchemeDepends = Annotated[str, Depends(oauth2_scheme)]
