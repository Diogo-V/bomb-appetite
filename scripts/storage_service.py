import os

from abc import ABC, abstractmethod
from enum import Enum

debug: bool = False


class StorageType(Enum):
    FILE = "file"
    DATABASE = "database"


class StorageService(ABC):
    @abstractmethod
    def store(self, data: bytes, filepath: str) -> ():
        pass

    @abstractmethod
    def load(self, filepath: str) -> bytes:
        pass


class StorageServiceFactory:
    @classmethod
    def get_storage_service(cls, storage_type: StorageType) -> StorageService:
        if storage_type == StorageType.FILE:
            return FileStorageService()
        elif storage_type == StorageType.DATABASE:
            return DatabaseStorageService()
        else:
            raise ValueError(f"Unknown storage type: {storage_type}")


class FileStorageService(StorageService):
    def store(self, data: bytes, filepath: str) -> ():
        try:
            with open(filepath, 'wb') as f:
                f.write(data)
        except Exception as e:
            raise IOError(f"Error writing key: {e}")

    def load(self, filepath: str) -> bytes:
        try:
            with open(filepath, 'rb') as f:
                data = f.read()
        except Exception as e:
            raise IOError(f"Error reading data: {e}.")
        return data


class DatabaseStorageService(StorageService):
    def store(self, data: bytes, filepath: str) -> ():
        # Implement database storage logic here
        pass

    def load(self, filepath: str) -> bytes:
        # Implement database retrieval logic here
        pass


if __name__ == "__main__":
    storage_service = StorageServiceFactory.get_storage_service(StorageType.FILE)

    data = b"test_data"
    filepath = "temp_data.txt"

    storage_service.store(data, filepath)
    data_read = storage_service.load(filepath)

    if debug:
        print(data)
        print(data_read)

    assert data == data_read

    os.remove(filepath)

    print("All tests passed!")
