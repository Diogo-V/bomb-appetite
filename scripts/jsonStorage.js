const fs = require('fs');
const path = require('path');
const storageService = require('./storageService');

const debug = false;
const jsonStorageService = storageService.StorageServiceFactory.getStorageService(storageService.StorageType.FILE)

function storeJson(jsonData, filename) {
    try {
        const jsonStr = JSON.stringify(jsonData);
        jsonStorageService.store(jsonStr, filename);
    } catch (error) {
        throw new Error(`Invalid file ${filename}. Expected JSON file`);
    }
}

function loadJson(filename) {
    const jsonStr = jsonStorageService.load(filename);
    try {
        const jsonData = JSON.parse(jsonStr);
        return jsonData;
    } catch (error) {
        throw new Error(`Invalid format ${filename}. Expected JSON format`);
    }
}

module.exports = {
    storeJson,
    loadJson,
};

if (require.main === module) {
    const filename = 'example.json';

    const jsonData = {
        header: {
            author: 'Ultron',
            version: 2,
            tags: ['robot', 'autonomy'],
        },
        body: '1231241342',
    };

    storeJson(jsonData, filename);

    const jsonReadData = loadJson(filename);

    console.assert(JSON.stringify(jsonData) === JSON.stringify(jsonReadData));

    fs.unlinkSync(path.join(__dirname, filename));

    console.log('All tests passed!');
}
