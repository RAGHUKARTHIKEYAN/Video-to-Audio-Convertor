# Quick Reference: MongoDB Database Creation

## 🚀 Quick Start

### Option 1: Using Python Script (Recommended)

**Docker Compose:**
```bash
python create_mongodb_databases.py --docker
```

**Kubernetes:**
```bash
python create_mongodb_databases.py --kubernetes --node-ip <YOUR_NODE_IP> --username nasi --password nasi1234
```

### Option 2: Using Shell Script (Docker Compose only)

```bash
# Windows (PowerShell)
bash create_mongodb_databases.sh

# Linux/Mac
./create_mongodb_databases.sh
```

### Option 3: Manual MongoDB Shell

**Docker Compose:**
```bash
docker exec -it mongo mongosh
```

Then run:
```javascript
use auth_db
db.createCollection("users")

use mp3s
db.createCollection("fs.files")
db.createCollection("fs.chunks")

use videos
db.createCollection("fs.files")
db.createCollection("fs.chunks")

show dbs
```

**Kubernetes:**
```bash
mongosh mongodb://nasi:nasi1234@<NODE_IP>:30005/admin?authSource=admin
```

Then run the same JavaScript commands as above.

### Option 4: Using JavaScript Script

**Docker Compose:**
```bash
docker exec -i mongo mongosh < create-databases.js
```

**Kubernetes:**
```bash
mongosh mongodb://nasi:nasi1234@<NODE_IP>:30005/admin?authSource=admin < create-databases.js
```

---

## 📋 Required Databases

| Database | Collections | Used By |
|----------|-------------|---------|
| `auth_db` | `users` | auth-service |
| `mp3s` | `fs.files`, `fs.chunks` | gateway-service, converter-service |
| `videos` | `fs.files`, `fs.chunks` | gateway-service |

---

## ✅ Verification

After creation, verify with:
```javascript
show dbs
```

You should see: `admin`, `auth_db`, `config`, `local`, `mp3s`, `videos`

---

## 📖 Full Documentation

See `MONGODB_DATABASE_SETUP.md` for detailed step-by-step instructions.




