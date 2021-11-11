from .db import PostgresStorage
from .receiver import KafkaReceiver
from ..common.logger import get_logger

logger = get_logger(__name__)


class DatabaseWriter:
    """
    Database writer implementation.
    Receives website check results from kafka and puts it to postgres storage.
    """

    def __init__(self, consumer: KafkaReceiver, db: PostgresStorage):
        self._consumer = consumer
        self._db = db

    def stop(self) -> None:
        """
        Stops all client instances.
        """
        for client in (self._consumer, self._db):
            client.close()

    def run(self) -> None:
        """
        Starts consuming results from kafka and putting it to postgres.
        """
        for check_result in self._consumer.receive():
            self._db.add(check_result)
