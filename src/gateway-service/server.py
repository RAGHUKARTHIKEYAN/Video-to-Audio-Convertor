import os, gridfs, pika, time
from flask import Flask, request, send_file
from flask_pymongo import PyMongo
from storage import util
from bson.objectid import ObjectId

server = Flask(__name__)

mongo_video = PyMongo(server, uri=os.environ.get('MONGODB_VIDEOS_URI'))

mongo_mp3 = PyMongo(server, uri=os.environ.get('MONGODB_MP3S_URI'))

fs_videos = gridfs.GridFS(mongo_video.db)
fs_mp3s = gridfs.GridFS(mongo_mp3.db)

def connect_to_rabbitmq(retries: int = 6, delay: int = 2):
    """Attempt to connect to RabbitMQ with simple retries.

    Reads RABBITMQ_HOST from environment (default: 'rabbitmq').
    Returns a pika.BlockingConnection or raises the last exception.
    """
    host = os.environ.get("RABBITMQ_HOST", "rabbitmq")
    params = pika.ConnectionParameters(host=host)
    last_exc = None
    for attempt in range(1, retries + 1):
        try:
            conn = pika.BlockingConnection(params)
            print(f"Connected to RabbitMQ at {host}")
            return conn
        except Exception as e:
            last_exc = e
            print(f"RabbitMQ connect attempt {attempt}/{retries} failed: {e}")
            if attempt < retries:
                time.sleep(delay)
    # All retries failed
    raise last_exc


connection = connect_to_rabbitmq()

channel = connection.channel()

@server.route("/upload", methods=["POST"])
def upload():
    if len(request.files) > 1 or len(request.files) < 1:
        return "exactly 1 file required", 400

    for _, f in request.files.items():
        err = util.upload(f, fs_videos, channel, {"admin": True})

        if err:
            return err

    return "success!", 200

@server.route("/download", methods=["GET"])
def download():
    fid_string = request.args.get("fid")

    if not fid_string:
        return "fid is required", 400

    try:
        out = fs_mp3s.get(ObjectId(fid_string))
        return send_file(out, download_name=f"{fid_string}.mp3")
    except Exception as err:
        print(err)
        return "internal server error", 500

@server.route('/')
def home():
    return "Gateway Service is running ✅"

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080)


