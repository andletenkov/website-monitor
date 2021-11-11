from kafka import KafkaProducer

from ..common.logger import get_logger
from ..common.model import WebsiteCheckResult

logger = get_logger(__name__)


class KafkaSender:
    """
    Basic kafka producer implementation.
    Produces website check results to kafka topic.
    """

    def __init__(self, kafka_config: dict[str, str]):
        config = kafka_config.copy()
        self._topic = config.pop('topic', None)

        self._producer = KafkaProducer(
            **config,
            security_protocol='SSL'
        )
        logger.debug(f'Kafka producer successfully connected to topic: \'{self._topic}\'')

    def close(self):
        """
        Closes producer connection.
        """
        self._producer.close()
        logger.debug('Kafka producer closed.')

    def send(self, data: WebsiteCheckResult) -> None:
        """
        Sends website check result to topic.
        :param data: Website check result instance.
        """
        self._producer.send(self._topic, data.to_bytes())
        logger.debug(f'Sent to topic \'{self._topic}\' > {data}')
        self._producer.flush()
