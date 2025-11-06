#!/bin/bash

# MongoDB Database Creation Script for Docker Compose
# This script creates the required databases in MongoDB running in Docker

set -e

echo "=========================================="
echo "MongoDB Database Creation Script"
echo "=========================================="
echo ""

# Check if MongoDB container is running
if ! docker ps | grep -q "mongo"; then
    echo "❌ Error: MongoDB container is not running"
    echo "   Please start it with: docker-compose up -d mongo"
    exit 1
fi

echo "✅ MongoDB container is running"
echo ""

# Function to execute MongoDB command
execute_mongo_command() {
    docker exec -i mongo mongosh --quiet <<EOF
$1
EOF
}

# Create databases
echo "📦 Creating databases..."

# Create auth_db
echo "  Creating auth_db database..."
execute_mongo_command "
use auth_db
db.createCollection('users')
print('✅ Database auth_db created')
"

# Create mp3s database
echo "  Creating mp3s database..."
execute_mongo_command "
use mp3s
db.createCollection('fs.files')
db.createCollection('fs.chunks')
print('✅ Database mp3s created')
"

# Create videos database
echo "  Creating videos database..."
execute_mongo_command "
use videos
db.createCollection('fs.files')
db.createCollection('fs.chunks')
print('✅ Database videos created')
"

# Verify databases
echo ""
echo "📋 Verifying databases..."
execute_mongo_command "
print('\\nAll databases:')
show dbs
"

echo ""
echo "=========================================="
echo "✅ Database creation completed!"
echo "=========================================="


