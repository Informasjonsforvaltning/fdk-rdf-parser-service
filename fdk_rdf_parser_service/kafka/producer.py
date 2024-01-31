import asyncio
import logging
import confluent_kafka
from confluent_kafka import KafkaException
from aiohttp import web
from threading import Thread

from fdk_rdf_parser_service import config


class AIOProducer:
    def __init__(self, configs, loop=None):
        self._loop = loop or asyncio.get_event_loop()
        self._producer = confluent_kafka.Producer(configs)
        self._cancelled = False
        self._poll_thread = Thread(target=self._poll_loop)
        self._poll_thread.start()

    def _poll_loop(self):
        while not self._cancelled:
            self._producer.poll(0.1)

    def close(self):
        self._cancelled = True
        self._poll_thread.join()

    def produce(self, topic, value):
        """
        An awaitable produce method.
        """
        result = self._loop.create_future()

        def ack(err, msg):
            if err:
                self._loop.call_soon_threadsafe(
                    result.set_exception, KafkaException(err)
                )
            else:
                self._loop.call_soon_threadsafe(result.set_result, msg)

        self._producer.produce(topic, value, on_delivery=ack)
        return result


async def create(app: web.Application):
    try:
        logging.info("Producer connecting to Kafka")
        app["kafka_producer"] = AIOProducer(config.kafka_config())
    except Exception as e:
        logging.info(f"Failed to create kafka producer: {e}")
        raise
    logging.info("Producer succesfully connected to Kafka")


async def shutdown(app: web.Application):
    app["kafka_producer"].close()
