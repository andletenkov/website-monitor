from datetime import datetime
import pytz


def test_add_valid_result(pg, check_result):
    result_id = pg.add(check_result)
    row = pg.get(result_id=result_id)
    assert row['id'] == result_id, 'Invalid result id'
    assert row['url'] == check_result.url, 'Invalid result url'
    assert row['status_code'] == check_result.status_code, 'Invalid result status_code'
    assert row['regex_matched'] == check_result.regex_matched, 'Invalid result regex_matched value'
    assert row['response_time'] == check_result.response_time, 'Invalid response time'

    db_time = row['checked_at']
    assert isinstance(db_time, datetime), 'checked_at should be an instance of datetime'
    assert db_time == pytz.timezone(str(db_time.tzinfo)).localize(datetime.fromisoformat(check_result.checked_at)), \
        'Invalid checked_at datetime in db'


def test_add_result_without_regex_matched(pg, check_result):
    check_result.regex_matched = None
    result_id = pg.add(check_result)
    row = pg.get(result_id=result_id)
    assert row['regex_matched'] is None, 'regex_matched should be None'
