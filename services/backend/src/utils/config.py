import platform
from os import getenv
from typing import Optional

from pydantic import BaseModel

def get_database_url() -> Optional[str]:
    user = getenv("DATABASE_USER", "user")
    password = getenv("DATABASE_PASSWORD", "password")
    host = getenv("DATABASE_HOST", "db")
    name = getenv("DATABASE_NAME", "db")
    return f"mysql+pymysql://{user}:{password}@{host}/{name}"

def get_ssl_params() -> dict:
    ssl_ca = "/home/vagrant/client-ssl/ca-db-cert.pem"
    client_cert = "/home/vagrant/client-ssl/client-cert.pem"
    client_key = "/home/vagrant/client-ssl/client-key.pem"
    return {'ssl': {'ca': ssl_ca, 'cert': client_cert, 'key': client_key}}

class Config(BaseModel):
    ENV: str = getenv("ENV", "dev")
    VERSION: str = getenv("VERSION", "0.0.1")
    HOST: str = getenv("HOST", "0.0.0.0")
    PORT: int = int(getenv("PORT", 8000))
    DATABASE_URL: Optional[str] = get_database_url()
    SSL_PARAMS: Optional[str] = get_ssl_params()
    SERVER_PRIVATE_KEY_PATH: str = "secrets/server_private_key.pem"
    USER_KEYS_TEMPLATE_PATH: str = "secrets/user_{id}_public_key.pem" 

config = Config()
