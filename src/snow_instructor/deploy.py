"""This module contains the deployment prepration script for Snow Instructor."""
from typing import Annotated

import typer
from snowflake.snowpark import Session

from snow_instructor import __version__
from snow_instructor.settings import SNOW_INSTRUCTOR_WH
from snow_instructor.utils import LogLevel, create_wh, setup_logging, wh_exists

app = typer.Typer(
    name=f'Snow Instructor {__version__} Deployment',
    help='This prepares everything for your Streamlit Snowflake deployment',
)


@app.command()
def main(
    connection_name: Annotated[str, typer.Option(help='Connection name')] = 'default',
    log_level: Annotated[LogLevel, typer.Option(help='Log level')] = LogLevel.INFO,
):

    setup_logging(log_level)
    Session.builder.config('connection_name', connection_name).create()

    if not wh_exists(SNOW_INSTRUCTOR_WH):
        create_wh(SNOW_INSTRUCTOR_WH, create_mode='IF_NOT_EXISTS')
        print(f'Warehouse {SNOW_INSTRUCTOR_WH} created successfully!')  # noqa: T201
    else:
        print(f'Warehouse {SNOW_INSTRUCTOR_WH} already exists!')  # noqa: T201


if __name__ == '__main__':
    app()
