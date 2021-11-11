import asyncio
from unittest.mock import MagicMock, AsyncMock

from aiohttp import ClientSession

from ..common.model import WebsiteCheckResult
from ..producer.website_checker import WebsiteChecker


def test_check_website(mocker, run_async):
    monitor_data = {'url': 'test', 'interval': 1}
    sender = MagicMock()
    response = AsyncMock()
    response.status = 200

    mocker.patch('aiohttp.ClientSession._request', return_value=response)

    checker = WebsiteChecker(sender, [monitor_data])
    result = run_async(checker.check_website(ClientSession(), checker._monitor_list[0]))

    assert isinstance(result, WebsiteCheckResult), 'Invalid website check result object'
    assert result.url == monitor_data['url'], 'Invalid url'
    assert result.status_code == response.status, 'Invalid status code'


def test_check_website_with_regex(mocker, run_async):
    monitor_data = {'url': 'test', 'interval': 1, 'regex': 'Lore.'}
    sender = MagicMock()
    response = AsyncMock()
    response.text = AsyncMock(return_value='Lorem ipsum dolor sit amet')

    mocker.patch('aiohttp.ClientSession._request', return_value=response)

    checker = WebsiteChecker(sender, [monitor_data])
    result = run_async(checker.check_website(ClientSession(), checker._monitor_list[0]))

    assert isinstance(result, WebsiteCheckResult), 'Invalid website check result object'
    assert result.regex_matched is True, 'Regex should be matched'
