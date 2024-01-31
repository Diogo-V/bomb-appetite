from pydantic import BaseModel


class EncryptedData(BaseModel):
    iv: str
    ciphertext: str
    tag: str
