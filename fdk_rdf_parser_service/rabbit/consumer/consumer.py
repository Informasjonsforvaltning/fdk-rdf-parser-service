"""Rabbit MQ consumer."""
from json.decoder import JSONDecodeError
import logging
import time
from typing import Optional

import pika
from pika.adapters.utils.connection_workflow import (
    AMQPConnectionWorkflowFailed,
    AMQPConnectorSocketConnectError,
)
from pika.exceptions import AMQPChannelError, AMQPConnectionError, AMQPError

from fdk_rdf_parser_service.config import RABBITMQ
from fdk_rdf_parser_service.rabbit.consumer.parser_ingest import ingest_for_index


class Listener:
    """Class for the rabbit consumer."""

    TYPE = RABBITMQ["TYPE"]
    EXCHANGE = RABBITMQ["EXCHANGE"]
    ROUTING_KEY = RABBITMQ["LISTENER_ROUTING_KEY"]

    def __init__(self) -> None:
        """Init Listener."""
        logging.debug("Initializing rabbit listener")
        self._conn: Optional[pika.BlockingConnection] = None
        self._channel: Optional[pika.channel.BlockingChannel] = None
        self._credentials = pika.PlainCredentials(
            username=RABBITMQ.get("USERNAME"), password=RABBITMQ.get("PASSWORD")
        )
        self._host = RABBITMQ.get("HOST")

    def connect(self) -> None:
        """Connect to rabbit exchange."""
        if not self._conn or self._conn.is_closed:
            logging.info("Establishing RabbitMQ connection ...")
            self._conn = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=self._host, credentials=self._credentials
                )
            )
        else:
            logging.info("RabbitMQ connection has already been established.")

        self._channel = self._conn.channel()
        self._channel.exchange_declare(exchange=self.EXCHANGE, exchange_type=self.TYPE)

        logging.info("RabbitMQ successfully connected to host.")

    def consume(self) -> None:
        """Bind to queue and start consuming messages."""
        if self._channel is None:
            raise AMQPChannelError("Channel is not established.")

        declaration = self._channel.queue_declare("", exclusive=True, auto_delete=True)
        queue_name = declaration.method.queue

        logging.info(f"RabbitMQ queue declared: {queue_name}")

        self._channel.queue_bind(
            exchange=self.EXCHANGE, queue=queue_name, routing_key=self.ROUTING_KEY
        )
        self._channel.basic_consume(
            queue=queue_name,
            auto_ack=True,
            on_message_callback=self.on_receive,
        )

        logging.info(
            f"RabbitMQ consumer starting (TYPE={self.TYPE}, EXCHANGE={self.EXCHANGE} "
            f"KEY={self.ROUTING_KEY}) ..."
        )

        self._channel.start_consuming()

    @staticmethod
    def on_receive(
        ch: pika.channel.Channel,
        method: pika.spec.Basic.Deliver,
        properties: pika.spec.BasicProperties,
        body: bytes,
    ) -> None:
        """Handler for received messages."""
        routing_key = method.routing_key

        try:
            logging.info(f"FROM: {routing_key}")
            ingest_for_index(routing_key.split(".")[0])
        except KeyError as err:
            logging.error(err, exc_info=True)
            logging.error(
                f"RabbitMQ: Received invalid operation type:  {str(body.decode())}"
            )
        except JSONDecodeError as err:
            logging.error(err, exc_info=True)
            logging.error(f"RabbitMQ: Received invalid JSON:\n {str(body.decode())}")


async def start_rabbit_listener() -> None:
    """Create and start rabbit listener."""
    listener = Listener()

    # try:
    #     logging.info("Connecting to rabbit exchange.")
    #     listener.connect()
    #     listener.consume()
    # except AMQPChannelError as err:
    #     logging.error(err, exc_info=True)
    #     logging.error("RabbitMQ channel error.")
    #     raise err
    # except (AMQPError, AMQPConnectorSocketConnectError, AMQPConnectionError) as err:
    #     logging.error(err, exc_info=True)
    #     logging.error("RabbitMQ connection error.")
    #     raise err
    # # Log unknown exception and exit
    # except Exception as err:
    #     logging.error(err, exc_info=True)
    #     raise err

    while True:
        retry_sleep = 10
        try:
            listener.connect()
            listener.consume()

        # Do not recover on channel errors
        except AMQPChannelError as err:
            logging.error(err, exc_info=True)
            logging.error("RabbitMQ channel error.")
            raise err
        # Recover on all other connection errors
        except (
            AMQPError,
            AMQPConnectorSocketConnectError,
            AMQPConnectionError,
            AMQPConnectionWorkflowFailed,
        ) as err:
            logging.error(err, exc_info=True)
            logging.error(
                f"RabbitMQ connection error. Retrying in {retry_sleep} seconds ..."
            )
            time.sleep(retry_sleep)
            continue
        # Log unknown exception and exit
        except Exception as err:
            logging.error(err, exc_info=True)
            raise err
        finally:
            if listener._channel:
                listener._channel.cancel()
            if listener._conn:
                listener._conn.close()
