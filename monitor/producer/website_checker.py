import asyncio
import re
import time
from asyncio import CancelledError
from datetime import datetime
from typing import Union

from aiohttp import ClientSession

from ..common.logger import get_logger
from ..common.model import WebsiteCheckResult, MonitoringData
from .sender import KafkaSender

logger = get_logger(__name__)


class WebsiteChecker:
    """
    Async website checker implementation.
    Periodically monitors specified URLs and sends results to kafka topic via producer.
    """

    def __init__(self, producer: KafkaSender, monitor_list: list[dict[str, Union[str, int]]]):
        self._producer = producer
        self._monitor_list = [MonitoringData.parse_obj(data) for data in monitor_list]
        self._loop = asyncio.get_event_loop()

    def run(self) -> None:
        """
        Starts main event loop.
        """
        try:
            self._loop.run_until_complete(self.main())
        except CancelledError:
            logger.debug('Running tasks was cancelled.')

    def stop(self) -> None:
        """
        Stop running tasks and closes producer connection.
        """
        tasks = asyncio.all_tasks(self._loop)
        for t in tasks:
            if not t.done():
                t.cancel()
        self._producer.close()

    async def main(self) -> None:
        """
        Creates monitoring tasks.
        Main method to execute in event loop.
        """
        async with ClientSession() as session:
            tasks = [
                asyncio.create_task(self.monitor(session, params)) for params in self._monitor_list
            ]
            await asyncio.gather(*tasks)

    @staticmethod
    async def check_website(session: ClientSession, params: MonitoringData) -> WebsiteCheckResult:
        """
        Checks website with specified parameters.
        :param session: Aiohttp client session.
        :param params: Monitoring data instance.
        :return: Website check result instance.
        """
        pattern = re.compile(params.regex) if params.regex else None
        start = time.time()
        async with session.get(params.url) as response:
            logger.debug(f'Checking {params.url}...')

            content = await response.text()
            elapsed = (time.time() - start) * 1000
            regex_matched = bool(pattern.search(content)) if pattern else None
            checked_at = str(datetime.now())

            result = WebsiteCheckResult(
                url=params.url,
                status_code=response.status,
                regex_matched=regex_matched,
                response_time=elapsed,
                checked_at=checked_at
            )
            return result

    async def monitor(self, session: ClientSession, params: MonitoringData) -> None:
        """
        Continuously monitors specified website and sends results to kafka via producer.
        :param session: Aiohttp client session.
        :param params: Monitoring data instance.
        :return:
        """
        while True:
            result = await self.check_website(session, params)
            self._producer.send(result)
            await asyncio.sleep(params.interval)
