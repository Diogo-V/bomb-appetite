const fs = require('fs');

const debug = false;

class StorageType {
    static FILE = "file";
    static DATABASE = "database";
}

class StorageService {
    store(data, filepath) {
        try {
            fs.writeFileSync(filepath, data);
        } catch (error) {
            throw new Error(`Error writing data: ${error}`);
        }
    }

    load(filepath) {
        try {
            const data = fs.readFileSync(filepath);
            return data;
        } catch (error) {
            throw new Error(`Error reading data: ${error}`);
        }
    }
}

class StorageServiceFactory {
    static getStorageService(storageType) {
        if (storageType === StorageType.FILE) {
            return new FileStorageService();
        } else if (storageType === StorageType.DATABASE) {
            return new DatabaseStorageService();
        } else {
            throw new Error(`Unknown storage type: ${storageType}`);
        }
    }
}

class FileStorageService extends StorageService {
    store(data, filepath) {
        try {
            fs.writeFileSync(filepath, data);
        } catch (error) {
            throw new Error(`Error writing data: ${error}`);
        }
    }

    load(filepath) {
        try {
            const data = fs.readFileSync(filepath);
            return data;
        } catch (error) {
            throw new Error(`Error reading data: ${error}`);
        }
    }
}

class DatabaseStorageService extends StorageService {
    store(data, filepath) {
        // Implement database storage logic here
    }

    load(filepath) {
        // Implement database retrieval logic here
    }
}

module.exports = {
    StorageType,
    StorageServiceFactory,
};

if (require.main === module) {
    const storageService = StorageServiceFactory.getStorageService(StorageType.FILE);

    const data = Buffer.from("test_data");
    const filepath = "temp_data.txt";

    storageService.store(data, filepath);
    const dataRead = storageService.load(filepath);

    if (debug) {
        console.log(data.toString());
        console.log(dataRead.toString());
    }

    console.assert(data.equals(dataRead));

    fs.unlinkSync(filepath);

    console.log("All tests passed!");
}
