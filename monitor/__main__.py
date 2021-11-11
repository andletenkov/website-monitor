import sys
from threading import Thread

from .common.logger import get_logger
from .consumer.receiver import KafkaReceiver
from .consumer.database_writer import DatabaseWriter
from .consumer.db import PostgresStorage
from .producer.sender import KafkaSender
from .producer.website_checker import WebsiteChecker
from .common.settings import settings

if __name__ == '__main__':
    logger = get_logger('main')

    wc = WebsiteChecker(KafkaSender(settings['kafka']), settings['monitoring'])
    dw = DatabaseWriter(
        KafkaReceiver(settings['kafka']),
        PostgresStorage(settings['postgres']['uri'], settings['postgres']['table'])
    )

    try:
        consumer = Thread(target=dw.run, daemon=True)
        producer = Thread(target=wc.run, daemon=True)

        consumer.start()
        producer.start()

        consumer.join()
        producer.join()
    except KeyboardInterrupt:
        logger.info('CTRL + C pressed. Exiting...')

        wc.stop()
        dw.stop()

        sys.exit(0)
