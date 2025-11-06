import jwt, datetime, os, bcrypt
import psycopg2
import psycopg2.extras
from psycopg2 import sql
from flask import Flask, request, jsonify
from flask_cors import CORS

server = Flask(__name__)
CORS(server)  # Enable CORS for all routes

# PostgreSQL configuration - expects a DATABASE_URL env var or falls back to localhost
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/authdb")


def get_conn():
    return psycopg2.connect(DATABASE_URL)


def ensure_users_table():
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        email TEXT UNIQUE NOT NULL,
        password BYTEA NOT NULL,
        created_at TIMESTAMPTZ NOT NULL DEFAULT now()
    );
    """
    conn = None
    try:
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute(create_table_sql)
            conn.commit()
    finally:
        if conn:
            conn.close()


ensure_users_table()

def hash_password(password):
    """Hash a password using bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)

def check_password(password, hashed):
    """Verify a password against its hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

@server.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400
    email = data['email']
    password = data['password']

    conn = None
    try:
        conn = get_conn()
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SELECT id FROM users WHERE email = %s", (email,))
            if cur.fetchone():
                return jsonify({'error': 'User already exists'}), 409

            hashed_password = hash_password(password)
            cur.execute(
                "INSERT INTO users (email, password, created_at) VALUES (%s, %s, %s)",
                (email, psycopg2.Binary(hashed_password), datetime.datetime.utcnow()),
            )
            conn.commit()
            return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        return jsonify({'error': 'Registration failed', 'details': str(e)}), 500
    finally:
        if conn:
            conn.close()

@server.route('/login', methods=['POST'])
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return 'Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'}
    conn = None
    try:
        conn = get_conn()
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SELECT password FROM users WHERE email = %s", (auth.username,))
            row = cur.fetchone()
            if not row:
                return 'User not found', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'}

            stored = row['password']
            # stored is bytes (BYTEA), bcrypt expects bytes
            if check_password(auth.password, stored.tobytes() if hasattr(stored, 'tobytes') else stored):
                return CreateJWT(auth.username, os.environ.get('JWT_SECRET', 'your-secret-key'), True)

            return 'Invalid password', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'}
    except Exception as e:
        return (f'Login error: {e}'), 500
    finally:
        if conn:
            conn.close()

def CreateJWT(username, secret, authz):
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=1),
            "iat": datetime.datetime.now(tz=datetime.timezone.utc),
            "admin": authz,
        },
        secret,
        algorithm="HS256",
    )

@server.route('/validate', methods=['POST'])
def validate():
    encoded_jwt = request.headers.get('Authorization')
    
    if not encoded_jwt:
        return 'Unauthorized', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'}

    encoded_jwt = encoded_jwt.split(' ')[1]
    try:
        decoded = jwt.decode(
            encoded_jwt, 
            os.environ.get('JWT_SECRET', 'your-secret-key'),
            algorithms=["HS256"]
        )
        return decoded, 200
    except jwt.InvalidTokenError:
        return 'Invalid token', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'}

if __name__ == '__main__':
    server.run(host='0.0.0.0', port=5000)
