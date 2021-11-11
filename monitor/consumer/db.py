import psycopg2
from psycopg2.extras import RealDictCursor, RealDictRow

from ..common.logger import get_logger
from ..common.model import WebsiteCheckResult

logger = get_logger(__name__)


class PostgresStorage:
    """
    PostgreSQL client implementation for storing website check results.
    """

    def __init__(self, uri: str, table: str):
        self._table = table
        self._conn = psycopg2.connect(uri)
        self._conn.autocommit = True
        self._cur = self._conn.cursor(cursor_factory=RealDictCursor)
        self._init_db()
        logger.debug('Successfully connected to Postgres DB')

    def close(self) -> None:
        """
        Closes database connection.
        """
        self._conn.close()
        logger.debug(f'Postgres connection closed.')

    def _init_db(self) -> None:
        """
        Creates table structure.
        """
        self._cur.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {self._table} (
                id SERIAL PRIMARY KEY,
                url VARCHAR NOT NULL,
                status_code INTEGER NOT NULL,
                regex_matched BOOLEAN,
                response_time INTEGER NOT NULL,
                checked_at TIMESTAMP WITH TIME ZONE NOT NULL
            );
            """
        )

    def clear(self) -> None:
        """
        Deletes all rows from table and refreshes primary id.
        """
        self._cur.execute(f'TRUNCATE {self._table} RESTART IDENTITY;')

    def add(self, result: WebsiteCheckResult) -> int:
        """
        Inserts specified result to table.
        :param result: Website check result instance.
        :return: Row id.
        """
        self._cur.execute(
            f"""
            INSERT INTO {self._table} (url, status_code, regex_matched, response_time, checked_at)
            VALUES (%(url)s, %(status_code)s, %(regex_matched)s, %(response_time)s, %(checked_at)s) RETURNING id; 
            """,
            result.dict()
        )
        result_id = self._cur.fetchall()[0]['id']
        logger.debug(f'Added to DB table \'{self._table}\' > id={result_id} {result}')
        return result_id

    def get(self, result_id: int) -> RealDictRow:
        """
        Gets row from table for specified id.
        :param result_id: Row id.
        :return: Dict with row data.
        """
        self._cur.execute(f'SELECT * FROM {self._table} WHERE id={result_id};')
        return self._cur.fetchone()

    def drop(self) -> None:
        """
        Drops table with results.
        """
        self._cur.execute(f'DROP TABLE {self._table};')
