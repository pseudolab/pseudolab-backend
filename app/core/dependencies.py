"""
공용 Depends 모음
"""
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
OAuth2SchemeDepends = Annotated[str, Depends(oauth2_scheme)]
