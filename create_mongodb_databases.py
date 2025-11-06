#!/usr/bin/env python3
"""
MongoDB Database Creation Script

This script automatically creates the required MongoDB databases for the microservices application.
Supports both Docker Compose and Kubernetes deployments.

Usage:
    Docker Compose: python create_mongodb_databases.py --docker
    Kubernetes:    python create_mongodb_databases.py --kubernetes --node-ip <IP> --username <user> --password <pass>
"""

import argparse
import sys
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError


def create_databases(client, databases_config):
    """
    Create MongoDB databases and collections.
    
    Args:
        client: MongoDB client instance
        databases_config: Dictionary mapping database names to list of collections
    """
    print("=" * 60)
    print("MongoDB Database Creation Script")
    print("=" * 60)
    
    created_dbs = []
    failed_dbs = []
    
    for db_name, collections in databases_config.items():
        try:
            print(f"\n📦 Creating database: {db_name}")
            db = client[db_name]
            
            # Create collections
            for collection_name in collections:
                if collection_name not in db.list_collection_names():
                    db.create_collection(collection_name)
                    print(f"  ✓ Created collection: {collection_name}")
                else:
                    print(f"  ℹ Collection already exists: {collection_name}")
            
            # Verify database exists by creating a dummy document and deleting it
            # This ensures the database is actually created
            test_collection = db[collections[0]]
            test_collection.insert_one({"__temp": True})
            test_collection.delete_one({"__temp": True})
            
            created_dbs.append(db_name)
            print(f"  ✅ Database '{db_name}' created successfully")
            
        except Exception as e:
            print(f"  ❌ Failed to create database '{db_name}': {str(e)}")
            failed_dbs.append((db_name, str(e)))
    
    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    
    if created_dbs:
        print(f"\n✅ Successfully created {len(created_dbs)} database(s):")
        for db in created_dbs:
            print(f"   - {db}")
    
    if failed_dbs:
        print(f"\n❌ Failed to create {len(failed_dbs)} database(s):")
        for db, error in failed_dbs:
            print(f"   - {db}: {error}")
    
    # Verify all databases
    print("\n📋 Verifying databases...")
    try:
        existing_dbs = client.list_database_names()
        required_dbs = list(databases_config.keys())
        missing_dbs = [db for db in required_dbs if db not in existing_dbs]
        
        if missing_dbs:
            print(f"⚠️  Warning: Some databases are missing: {', '.join(missing_dbs)}")
        else:
            print("✅ All required databases exist!")
            
        print("\nAll databases in MongoDB:")
        for db in existing_dbs:
            if db in required_dbs:
                print(f"   ✓ {db} (required)")
            else:
                print(f"   - {db}")
                
    except Exception as e:
        print(f"❌ Error verifying databases: {str(e)}")
    
    return len(failed_dbs) == 0


def main():
    parser = argparse.ArgumentParser(
        description='Create MongoDB databases for microservices application',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Docker Compose (no authentication)
  python create_mongodb_databases.py --docker
  
  # Kubernetes with authentication
  python create_mongodb_databases.py --kubernetes --node-ip 192.168.1.100 --username nasi --password nasi1234
  
  # Custom connection string
  python create_mongodb_databases.py --connection "mongodb://user:pass@host:port/admin"
        """
    )
    
    parser.add_argument('--docker', action='store_true',
                       help='Use Docker Compose connection (mongodb://localhost:27017)')
    parser.add_argument('--kubernetes', action='store_true',
                       help='Use Kubernetes connection')
    parser.add_argument('--connection', type=str,
                       help='Custom MongoDB connection string')
    parser.add_argument('--node-ip', type=str,
                       help='Kubernetes node IP address (required for --kubernetes)')
    parser.add_argument('--username', type=str, default='nasi',
                       help='MongoDB username (default: nasi)')
    parser.add_argument('--password', type=str, default='nasi1234',
                       help='MongoDB password (default: nasi1234)')
    parser.add_argument('--port', type=int, default=30005,
                       help='Kubernetes NodePort (default: 30005)')
    
    args = parser.parse_args()
    
    # Determine connection string
    if args.connection:
        connection_string = args.connection
    elif args.docker:
        connection_string = 'mongodb://localhost:27017/'
    elif args.kubernetes:
        if not args.node_ip:
            print("❌ Error: --node-ip is required when using --kubernetes")
            sys.exit(1)
        connection_string = f'mongodb://{args.username}:{args.password}@{args.node_ip}:{args.port}/admin?authSource=admin'
    else:
        print("❌ Error: Must specify --docker, --kubernetes, or --connection")
        parser.print_help()
        sys.exit(1)
    
    # Database configuration
    databases_config = {
        'auth_db': ['users'],
        'mp3s': ['fs.files', 'fs.chunks'],
        'videos': ['fs.files', 'fs.chunks']
    }
    
    print(f"\n🔗 Connecting to MongoDB...")
    print(f"   Connection string: {connection_string.replace(args.password, '***') if args.password in connection_string else connection_string}")
    
    try:
        # Connect to MongoDB
        client = MongoClient(connection_string, serverSelectionTimeoutMS=5000)
        
        # Test connection
        client.admin.command('ping')
        print("✅ Successfully connected to MongoDB")
        
        # Create databases
        success = create_databases(client, databases_config)
        
        # Close connection
        client.close()
        
        if success:
            print("\n✅ Database creation completed successfully!")
            sys.exit(0)
        else:
            print("\n⚠️  Database creation completed with some errors.")
            sys.exit(1)
            
    except ConnectionFailure:
        print("❌ Error: Could not connect to MongoDB")
        print("   Please ensure MongoDB is running and accessible")
        sys.exit(1)
    except ServerSelectionTimeoutError:
        print("❌ Error: MongoDB server selection timeout")
        print("   Please check your connection settings and network")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()


