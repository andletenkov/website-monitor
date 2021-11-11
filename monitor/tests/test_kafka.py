from unittest.mock import MagicMock

import pytest
from pydantic import ValidationError

from ..common.model import WebsiteCheckResult


def test_send_and_receive(kafka_sender, kafka_receiver, check_result):
    kafka_sender.send(check_result)
    data = kafka_receiver.pop()
    assert isinstance(data, WebsiteCheckResult), 'Invalid data type received'
    assert data == check_result, 'Received data should be the same as sent'


def test_send_invalid_data(kafka_sender):
    data = 'test'
    with pytest.raises(AttributeError) as e:
        kafka_sender.send(data)

    assert f"'str' object has no attribute 'to_bytes'" in str(e.value)


def test_receive_invalid_data(kafka_sender, kafka_receiver):
    data = MagicMock()
    data.to_bytes = lambda: str.encode('utf-8')
    kafka_sender.send(data)

    with pytest.raises(ValidationError) as e:
        kafka_receiver.pop()

    assert 'validation error for WebsiteCheckResult' in str(e.value)


