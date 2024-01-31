import json
import storage_service
import os

debug: bool = False
json_storage_service = storage_service.StorageServiceFactory.get_storage_service(storage_service.StorageType.FILE)


def store_json(json_data: dict, filename: str) -> ():
    try:
        json_str = json.dumps(json_data)
    except Exception: 
        raise ValueError(f"Invalid file {filename}. Excepted json file")
    json_storage_service.store(json_str.encode(), filename)


def load_json(filename) -> dict:
    json_str = json_storage_service.load(filename)
    try:
        json_data = json.loads(json_str.decode())
    except Exception: 
        raise ValueError(f"Invalid format {filename}. Excepted json format")

    return json_data


if __name__ == "__main__":
    filename = "example.json"

    json_data = {
        'header': {
            "author": "Ultron",
            "version": 2,
            "tags": ["robot", "autonomy"]
        },
        "body": "1231241342"
    }

    store_json(json_data, filename)

    json_data_read = load_json(filename)

    assert json_data == json_data_read

    os.remove(filename)

    print("All tests passed!")
