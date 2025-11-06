import pika, sys, os, time, json
from moviepy.editor import VideoFileClip

def callback(ch, method, properties, body):
    print("📩 Received message from queue...")
    data = json.loads(body)
    print("Data:", data)
    # Conversion logic placeholder (you can customize this)
    print("🎬 Video conversion completed.")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    # Wait until RabbitMQ is ready
    for i in range(10):
        try:
            print(f"🔁 Attempting to connect to RabbitMQ (rabbitmq)... {i+1}/10")
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host="rabbitmq", heartbeat=0)
            )
            channel = connection.channel()
            break
        except Exception as e:
            print(f"❌ RabbitMQ not ready yet, retrying in 5 seconds... ({e})")
            time.sleep(5)
    else:
        print("❌ Failed to connect to RabbitMQ after 10 attempts. Exiting...")
        sys.exit(1)

    queue_name = os.environ.get("VIDEO_QUEUE", "video")
    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    print("✅ Connected and waiting for messages. To exit press CTRL+C")
    channel.start_consuming()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("👋 Exiting...")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
