"""Utility functions for handling Snowflake/Snowpark

In most functions we assume that a Snowflake session is already created.
"""
import enum
import logging
import sys
from typing import Dict, List

from snowflake.core import CreateMode, Root
from snowflake.core.warehouse import Warehouse, WarehouseCollection, WarehouseResource
from snowflake.snowpark import Session

from snow_instructor.settings import SNOWDOCS_TABLE


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
    """Check if a table exists in the current Snowflake session"""
    session = Session.builder.getOrCreate()
    try:
        session.table(table_name).count()
    except Exception:
        return False
    return True


def get_snowdocs_table() -> List[Dict[str, str]]:
    if not table_exists(SNOWDOCS_TABLE):
        msg = f'Table {SNOWDOCS_TABLE} does not exist. Create it using `crawl-snow-docs` command.'
        raise ValueError(msg)

    session = Session.builder.getOrCreate()
    rows = session.table(SNOWDOCS_TABLE).collect()
    return [{k.lower(): v for k, v in row.asDict().items()} for row in rows]


def show_warehouses() -> List[str]:
    """Retrieve all warehouses in the current Snowflake session

    This should be also possible with `root.warehouses` but it's not working in the current version.
    """
    session = Session.builder.getOrCreate()
    rows = session.sql('SHOW WAREHOUSES').collect()
    return [row['name'] for row in rows]


def wh_exists(warehouse_name: str) -> bool:
    """Check if a warehouse exists in the current Snowflake session"""
    return warehouse_name in show_warehouses()


def create_wh(name: str, *, create_mode: CreateMode = 'IF_NOT_EXISTS', **kwargs) -> WarehouseResource:
    """Create a warehouse in the current Snowflake session"""
    root = Root(Session.builder.getOrCreate())
    wh_cfg = Warehouse(name=name, **kwargs)
    # This should work according to the Snowflake documentation but it's not working in the current version.
    # Raises: NotImplementedError: create_or_update is not yet supported for warehouse. Updating warehouse objects\
    # is not supported yet; use create() for creating a warehouse.
    # wh = root.warehouses[name].create_or_update(wh_cfg)
    wh_collection = WarehouseCollection(root)
    return wh_collection.create(wh_cfg, mode=create_mode)


def get_wh(name: str) -> WarehouseResource:
    """Retrieve a warehouse in the current Snowflake session"""
    root = Root(Session.builder.getOrCreate())
    wh_collection = WarehouseCollection(root)
    return wh_collection[name]


def streamlit_on_snowflake() -> bool:
    """Check if Streamlit is available in the current Snowflake session"""
    import streamlit as st  # noqa: PLC0415

    # Basically check if the `switch_page` function is available in the `st` module
    # Check also https://docs.snowflake.com/en/developer-guide/streamlit/limitations
    return not hasattr(st, 'switch_page')
