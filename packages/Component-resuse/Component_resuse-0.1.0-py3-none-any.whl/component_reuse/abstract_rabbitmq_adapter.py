from time import sleep
from typing import Any, Union
import pika
from .queue_adapter_abc import QueueAdapterABC
from .logger import LOG


class RabbitMQAdapter(QueueAdapterABC):
    """A class to manage RabbitMQ queue operations."""

    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        ssl_options: Union[pika.SSLOptions, None],
        queue_name: str,
        has_error_queue: bool = False,
        error_queue_name: str = None,
        has_dead_letter_queue: bool = False,
        dead_letter_queue_name: str = None,
        max_retries: int = 0,
        on_message_callback: Any = None,
        consumption_limit: int = -1,
    ) -> None:
        """Initialize the RabbitMQAdapter with RabbitMQ connection parameters."""
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.ssl_options = ssl_options
        self.connection = None
        self.channel = None
        self.on_message_callback = on_message_callback
        self.queue_name = queue_name
        self.has_error_queue = has_error_queue
        self.error_queue_name = error_queue_name
        self.has_dead_letter_queue = has_dead_letter_queue
        self.dead_letter_queue_name = dead_letter_queue_name
        self.max_retries = max_retries
        self.consumption_limit = consumption_limit
        self.consumed_messages = 0

    def connect(self) -> bool:
        """Establish a connection to the RabbitMQ server."""
        try:
            # Create credentials and parameters for connecting to RabbitMQ
            credentials = pika.PlainCredentials(self.username, self.password)
            parameters = pika.ConnectionParameters(
                host=self.host, port=self.port, credentials=credentials
            )
            parameters.ssl_options = self.ssl_options

            # Open a blocking connection and channel
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()

            # Declare the main queue and error/dead-letter queues if needed
            self.channel.queue_declare(queue=self.queue_name, durable=True)
            if self.has_error_queue:
                self.channel.queue_declare(queue=self.error_queue_name, durable=True)
            if self.has_dead_letter_queue:
                self.channel.queue_declare(
                    queue=self.dead_letter_queue_name, durable=True
                )
            LOG.info(f"Connected to RabbitMQ server on {self.host}:{self.port}")
            return True
        except pika.exceptions.AMQPError as e:
            # If connection fails, disconnect and log the error
            self.disconnect()
            LOG.error(f"Error connecting to RabbitMQ: {e}")
            raise e

    def consume(self) -> None:
        """Begin consuming messages from the RabbitMQ queue."""
        try:
            self.channel.basic_consume(
                queue=self.queue_name,
                auto_ack=False,  # Manual acknowledgment required
                on_message_callback=self.run,  # Use the run method to process messages
            )
            self.channel.start_consuming()  # Keep consuming indefinitely
        except Exception as e:
            LOG.error(f"Error consuming the message: {e}")
            raise e

    def consume_with_limits(self) -> None:
        """Consume messages from the RabbitMQ queue with a message limit."""
        try:
            while self.consumed_messages < self.consumption_limit:
                method_frame, properties, body = self.channel.basic_get(
                    queue=self.queue_name, auto_ack=False  # Manual acknowledgment
                )
                if method_frame:
                    # Process the message
                    self.run(self.channel, method_frame, properties, body)
                    self.consumed_messages += 1
                else:
                    LOG.info("Heartbeat - No message in queue.")
                    sleep(5)  # Pause to avoid spamming logs if the queue is empty
            LOG.info(
                f"Consumed the maximum number of messages: {self.consumption_limit}"
            )
        except Exception as e:
            LOG.error(f"Error consuming the message: {e}")
            raise e

    def run(self, channel: Any, method: Any, properties: Any, body: bytes) -> None:
        """Process the incoming message, handle retries, and dispatch to error queue if needed."""
        try:
            # Process the message using the provided callback
            self.on_message_callback(body)
            # Manually acknowledge the message after processing
            channel.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            LOG.error(f"Error processing the message: {e}")
            LOG.exception(e)
            # Check and handle message requeueing based on retries
            requeue_count = (
                properties.headers.get("requeue_count", 0) if properties.headers else 0
            )
            if requeue_count < self.max_retries:
                # Requeue the message for further attempts
                headers = {"requeue_count": requeue_count + 1}
                channel.basic_publish(
                    exchange="",
                    routing_key=self.queue_name,
                    body=body,
                    properties=pika.BasicProperties(
                        delivery_mode=2,  # Persistent message
                        headers=headers,
                    ),
                )
                LOG.info(f"Message requeued to {self.queue_name}.")
            else:
                # If max retries are reached, move the message to the error queue if configured
                if self.has_error_queue:
                    channel.basic_publish(
                        exchange="",
                        routing_key=self.error_queue_name,
                        body=body,
                        properties=pika.BasicProperties(
                            delivery_mode=2,  # Persistent message
                            headers={"requeue_count": 0},  # Reset requeue count
                        ),
                    )
                    LOG.info(f"Message moved to error queue {self.error_queue_name}.")
                else:
                    # Log and requeue to the original queue if no error queue is available
                    channel.basic_publish(
                        exchange="",
                        routing_key=self.queue_name,
                        body=body,
                        properties=pika.BasicProperties(
                            delivery_mode=2,  # Persistent message
                            headers={"requeue_count": 0},  # Reset requeue count
                        ),
                    )
                    LOG.info(
                        f"Message exceeded retries, requeued to {self.queue_name}."
                    )

    def dispatch(self, body: Any) -> None:
        """Send a message to the RabbitMQ queue."""
        retries = 0
        while retries < 3:
            try:
                # Ensure connection is active before dispatching
                if not self.connection or self.connection.is_closed:
                    LOG.debug(f"Reconnecting to {self.queue_name}.")
                    self.connect()
                # Publish the message to the queue
                self.channel.basic_publish(
                    exchange="",
                    routing_key=self.queue_name,
                    body=body,
                    properties=pika.BasicProperties(
                        delivery_mode=2,  # Persistent message
                    ),
                )
                break
            except Exception as e:
                # Retry if publishing fails
                sleep(0.5)
                self.connect()
                LOG.error(
                    f"Error dispatching to queue {self.queue_name}, retrying: {e}"
                )
                retries += 1
                if retries >= 3:
                    LOG.error(
                        f"Max retries reached for dispatch to {self.queue_name}: {e}"
                    )
                    raise e

    def disconnect(self) -> bool:
        """Close the connection to the RabbitMQ server."""
        try:
            # Stop consuming and close the channel
            if self.channel:
                self.channel.stop_consuming()
            if self.connection and not self.connection.is_closed:
                self.connection.close()
                LOG.info(f"Disconnected from RabbitMQ on {self.host}:{self.port}")
                return True
        except Exception as e:
            LOG.error("Error during disconnection.")
            raise e
