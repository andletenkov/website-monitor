import asyncio
import random
import string
from datetime import datetime
from typing import Callable

import pytest

from ..common.model import WebsiteCheckResult
from ..common.settings import settings
from ..consumer.db import PostgresStorage
from ..consumer.receiver import KafkaReceiver
from ..producer.sender import KafkaSender


@pytest.fixture(scope='session')
def pg_session() -> PostgresStorage:
    """
    Creates and yields PostgresStorage instance.
    Does clean up at the end of test session.
    """
    pg = PostgresStorage(settings['postgres']['uri'], 'test')
    yield pg
    pg.drop()
    pg.close()


@pytest.fixture
def pg(pg_session) -> PostgresStorage:
    """
    PostgresStorage function scoped fixture.
    """
    yield pg_session
    pg_session.clear()


@pytest.fixture
def check_result() -> WebsiteCheckResult:
    """
    Generates and yields random website check result instance.
    """
    yield WebsiteCheckResult(
        url=f'https://{"".join([random.choice(string.ascii_lowercase) for _ in range(10)])}.com',
        status_code=random.randint(100, 600),
        regex_matched=random.choice([True, False]),
        response_time=random.randint(1, 1000),
        checked_at=str(datetime.now())
    )


@pytest.fixture
def kafka_sender() -> KafkaSender:
    """
    Creates and yields KafkaSender instance.
    """
    sender = KafkaSender(settings['kafka'])
    yield sender
    sender.close()


@pytest.fixture
def kafka_receiver() -> KafkaReceiver:
    """
    Creates and yields KafkaReceiver instance.
    """
    receiver = KafkaReceiver(settings['kafka'])
    yield receiver
    receiver.close()


@pytest.fixture(scope='session')
def run_async() -> Callable:
    """
    Factory fixture that simplifies async function execution.
    """
    loops = []

    def inner(future):
        loop = asyncio.get_event_loop()
        loops.append(loop)
        task = loop.create_task(future)
        loop.run_until_complete(task)
        return task.result()

    yield inner
    for loop in loops:
        loop.stop()
        loop.close()
