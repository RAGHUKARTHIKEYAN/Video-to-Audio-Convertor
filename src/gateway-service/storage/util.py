import os
import pika, json

def upload(f, fs, channel, access):
    try:
        fid = fs.put(f)
    except Exception as err:
        print(err)
        return "internal server error, fs level", 500

    message = {
        "video_fid": str(fid),
        "mp3_fid": None,
        "username": access["username"],
    }

    try:
        # ✅ Use environment variable or default to 'video'
        queue_name = os.environ.get("VIDEO_QUEUE", "video")

        # ✅ Declare the queue before publishing
        channel.queue_declare(queue=queue_name, durable=True)

        channel.basic_publish(
            exchange="",
            routing_key=queue_name,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
    except Exception as err:
        print(err)
        fs.delete(fid)
        return f"internal server error rabbitmq issue, {err}", 500

