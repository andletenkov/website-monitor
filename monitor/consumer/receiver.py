from typing import Iterator

from kafka import KafkaConsumer

from ..common.logger import get_logger
from ..common.model import WebsiteCheckResult

logger = get_logger(__name__)


class KafkaReceiver:
    """
    Basic kafka consumer implementation.
    Consumes website check results from kafka topic.
    """

    def __init__(self, kafka_config: dict[str, str]):
        config = kafka_config.copy()
        kafka_topic = config.pop('topic', None)

        self._consumer = KafkaConsumer(
            kafka_topic,
            **config,
            client_id='website-checks-client-1',
            group_id='website-checks-group',
            security_protocol='SSL',
        )
        logger.debug(f'Kafka consumer successfully connected to topic \'{kafka_topic}\'.')

    def pop(self) -> WebsiteCheckResult:
        """
        Get latest result from topic.
        :return: Website check result instance.
        """
        return WebsiteCheckResult.from_bytes(next(self._consumer).value)

    def close(self) -> None:
        """
        Closes consumer connection.
        """
        self._consumer.close()
        logger.debug(f'Kafka consumer closed.')

    def receive(self) -> Iterator[WebsiteCheckResult]:
        """
        Starts continuously yielding website check results from topic.
        :return: Website check results generator.
        """
        for message in self._consumer:
            logger.debug(f'Received from topic \'{message.topic}\' < {message.value}')
            yield WebsiteCheckResult.from_bytes(message.value)
