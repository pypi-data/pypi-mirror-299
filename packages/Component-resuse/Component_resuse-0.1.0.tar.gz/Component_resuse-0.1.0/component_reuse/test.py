from component_reuse.main import hello
from component_reuse.abstract_rabbitmq_adapter import RabbitMQAdapter
from settings import rabbitmq_adapter_settings
import json

hello()


def on_message_callback(body):
    try:
        message = body.decode("utf-8")
        json_message = json.loads(message)
        print(f"Received message: {json.dumps(json_message, indent=2)}")
    except json.JSONDecodeError:
        print(f"Received message: {body.decode('utf-8')}")


# Initialize the RabbitMQAdapter
adapter = RabbitMQAdapter(
    host=rabbitmq_adapter_settings.RABBITMQ_HOST,
    port=rabbitmq_adapter_settings.RABBITMQ_PORT,
    username=rabbitmq_adapter_settings.RABBITMQ_USERNAME,
    password=rabbitmq_adapter_settings.RABBITMQ_PASSWORD.get_secret_value(),
    ssl_options=None,
    queue_name=rabbitmq_adapter_settings.RABBITMQ_CONSUME_QUEUE_NAME,
    on_message_callback=on_message_callback,
)

# Test the connection to RabbitMQ
try:
    if adapter.connect():
        adapter.consume()
except Exception as e:
    print(f"Connection failed: {e}")
