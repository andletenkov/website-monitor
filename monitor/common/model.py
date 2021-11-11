from typing import Optional
from pydantic import BaseModel


class MonitoringData(BaseModel):
    """
    Monitoring data representation.
    """
    url: str
    interval: int
    regex: Optional[str]


class WebsiteCheckResult(BaseModel):
    """
    Website check result representation.
    """
    url: str
    status_code: int
    regex_matched: Optional[bool]
    response_time: int
    checked_at: str

    @classmethod
    def from_bytes(cls, data: bytes) -> 'WebsiteCheckResult':
        """
        Deserializes received bytes to model instance.
        :param data: Bytes data.
        :return: New model instance.
        """
        return cls.parse_raw(data.decode())

    def to_bytes(self) -> bytes:
        """
        Serializes model instance to bytes.
        :return: Bytes data.
        """
        return self.json().encode('utf-8')
