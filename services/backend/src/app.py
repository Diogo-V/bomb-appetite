import uvicorn
import logging
from fastapi import FastAPI, Request, status, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from src.endpoints.api import v1_api_router
from src.utils.config import config

app = FastAPI()

@app.middleware("http")
async def enforce_https(request: Request, call_next):
    if not request.url.scheme == "https":
        # Construct HTTPS URL and raise a redirect HTTPException
        secure_url = request.url.replace(scheme="https")
        raise HTTPException(status_code=307, headers={"Location": str(secure_url)})
    
    # Continue processing if already using HTTPS
    return await call_next(request)

app.include_router(v1_api_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    exc_str = f"{exc}".replace("\n", " ").replace("   ", " ")
    logging.error(f"{request}: {exc_str}")
    content = {"status_code": 422, "message": exc_str, "data": None}
    return JSONResponse(
        content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )


if __name__ == "__main__":
    uvicorn.run(
        "app:app", 
        host=config.HOST,
        port=config.PORT,
        log_level="info",
        ssl_keyfile="/home/vagrant/server-ssl/server-backend-key.pem",
        ssl_certfile="/home/vagrant/server-ssl/server-backend-cert.pem",
        ssl_ca_certs="/home/vagrant/server-ssl/ca-backend-cert.pem",  
        reload=True
    )
