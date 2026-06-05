"""
ECHelpers.py — Custom Python library for EC Robot Framework tests
Layer 5: Python utilities that cannot be expressed in Robot syntax

Usage in .robot:
    Library    resources/libraries/ECHelpers.py    ${DB_URL}    ${DB_USER}    ${DB_PASS}
"""

import time
import oracledb
from robot.api import logger
from robot.api.deco import keyword


class ECHelpers:
    """Custom Robot Framework library for EC Oracle DB operations."""

    ROBOT_LIBRARY_SCOPE = 'SUITE'   # one instance shared across all tests in suite

    def __init__(self, db_url: str = 'localhost:1521/ORCL',
                 db_user: str = 'ECKERNEL_EC',
                 db_pass: str = 'energy') -> None:
        self._db_url = db_url
        self._db_user = db_user
        self._db_pass = db_pass
        self._conn = None

    def _get_connection(self):
        if self._conn is None:
            self._conn = oracledb.connect(
                user=self._db_user,
                password=self._db_pass,
                dsn=self._db_url
            )
        return self._conn

    @keyword('Generate Unique Name')
    def generate_unique_name(self, prefix: str = 'AUTOTEST') -> str:
        """Return a unique name using prefix + timestamp.
        Example: AUTOTEST_20250101_143052
        """
        ts = time.strftime('%Y%m%d_%H%M%S')
        name = f'{prefix}_{ts}'
        logger.info(f'Generated unique name: {name}')
        return name

    @keyword('Check Rule Exists In DB')
    def check_rule_exists_in_db(self, check_name: str) -> bool:
        """Return True if check rule exists in CTRL_CHECK_RULES, False otherwise."""
        conn = self._get_connection()
        cur = conn.cursor()
        cur.execute(
            'SELECT COUNT(*) FROM TV_CTRL_CHECK_RULES WHERE CHECK_NAME = :n',
            n=check_name
        )
        count = cur.fetchone()[0]
        cur.close()
        logger.info(f'Check rule {check_name}: found {count} rows')
        return count > 0

    @keyword('Query Single Value')
    def query_single_value(self, sql: str, **params) -> str:
        """Execute SQL and return first column of first row as string."""
        conn = self._get_connection()
        cur = conn.cursor()
        cur.execute(sql, params)
        row = cur.fetchone()
        cur.close()
        result = str(row[0]) if row and row[0] is not None else ''
        logger.info(f'Query result: {result}')
        return result

    @keyword('Parse Grid Rows')
    def parse_grid_rows(self, html: str) -> list:
        """Parse HTML datatable rows and return list of text content per row.
        Useful for extracting EC grid data for assertion.
        """
        import re
        # Extract text from <tr data-rk> elements
        rows = re.findall(r'<tr[^>]*data-rk[^>]*>(.*?)</tr>', html, re.DOTALL)
        result = []
        for row in rows:
            # Strip all HTML tags and clean whitespace
            text = re.sub(r'<[^>]+>', ' ', row)
            text = ' '.join(text.split())
            if text:
                result.append(text)
        logger.info(f'Parsed {len(result)} grid rows')
        return result
