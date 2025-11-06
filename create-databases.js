// MongoDB Database Creation Script
// This script can be used with mongosh or mongo shell
// Usage: mongosh < connection_string > create-databases.js

print("==========================================");
print("MongoDB Database Creation Script");
print("==========================================");
print("");

// Databases configuration
const databases = {
    'auth_db': ['users'],
    'mp3s': ['fs.files', 'fs.chunks'],
    'videos': ['fs.files', 'fs.chunks']
};

// Create databases and collections
let createdCount = 0;
let failedCount = 0;

for (const [dbName, collections] of Object.entries(databases)) {
    try {
        print(`📦 Creating database: ${dbName}`);
        
        // Switch to database
        const db = db.getSiblingDB(dbName);
        
        // Create collections
        collections.forEach(collectionName => {
            if (!db.getCollectionNames().includes(collectionName)) {
                db.createCollection(collectionName);
                print(`  ✓ Created collection: ${collectionName}`);
            } else {
                print(`  ℹ Collection already exists: ${collectionName}`);
            }
        });
        
        // Verify database exists by inserting and deleting a test document
        const testCollection = db[collections[0]];
        testCollection.insertOne({ __temp: true });
        testCollection.deleteOne({ __temp: true });
        
        createdCount++;
        print(`  ✅ Database '${dbName}' created successfully\n`);
        
    } catch (error) {
        failedCount++;
        print(`  ❌ Failed to create database '${dbName}': ${error.message}\n`);
    }
}

// Summary
print("==========================================");
print("Summary");
print("==========================================");
print(`✅ Successfully created: ${createdCount} database(s)`);
if (failedCount > 0) {
    print(`❌ Failed: ${failedCount} database(s)`);
}

// Verify databases
print("\n📋 Verifying databases...");
print("\nAll databases:");
db.adminCommand('listDatabases').databases.forEach(database => {
    const dbName = database.name;
    if (Object.keys(databases).includes(dbName)) {
        print(`  ✓ ${dbName} (required)`);
    } else {
        print(`  - ${dbName}`);
    }
});

print("\n==========================================");
print("✅ Script completed!");
print("==========================================");


