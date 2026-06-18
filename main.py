import logging

from authx.exceptions import TokenExpiredError
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from routers.file import router_files
from routers.massage import router
from routers.user import router_user
from settings.db import *

logger = logging.getLogger(__name__)

app = FastAPI()


@app.exception_handler(TokenExpiredError)
async def token_expired_handler(request: Request, exc: TokenExpiredError):
    return JSONResponse(
        status_code=401, content={"detail": "Токен не валідний або протермінований"}
    )


app.include_router(router)
app.include_router(router_files)
app.include_router(router_user)
