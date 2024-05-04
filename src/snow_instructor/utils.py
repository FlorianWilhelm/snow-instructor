import enum
import logging
import sys

from snowflake.snowpark import Session

SNOWDOCS_TABLE = 'SNOWDOCS'


class LogLevel(str, enum.Enum):
    CRITICAL = 'critical'
    ERROR = 'error'
    WARNING = 'warning'
    INFO = 'info'
    DEBUG = 'debug'


def setup_logging(log_level: LogLevel):
    """Setup basic logging"""
    log_format = '[%(asctime)s] %(levelname)s:%(name)s:%(message)s'
    numeric_level = getattr(logging, log_level.name.upper(), None)
    logging.basicConfig(level=numeric_level, stream=sys.stdout, format=log_format, datefmt='%Y-%m-%d %H:%M:%S')


def table_exists(table_name: str) -> bool:
    session = Session.builder.getOrCreate()
    try:
        session.table(table_name).count()
    except Exception:
        return False
    return True


def get_snowdocs_table() -> list[dict[str, str]]:
    if not table_exists(SNOWDOCS_TABLE):
        msg = f'Table {SNOWDOCS_TABLE} does not exist. Create it using `crawl-snow-docs` command.'
        raise ValueError(msg)

    session = Session.builder.getOrCreate()
    rows = session.table(SNOWDOCS_TABLE).collect()
    return [{k.lower(): v for k, v in row.asDict().items()} for row in rows]
