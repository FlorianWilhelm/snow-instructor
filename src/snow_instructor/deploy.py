"""This module contains the deployment prepration script for Snow Instructor."""

import typer
from snowflake.snowpark import Session
from typing_extensions import Annotated

from snow_instructor import __version__
from snow_instructor.settings import SNOWINSTRUCTOR_DB, SNOWINSTRUCTOR_WH
from snow_instructor.utils import LogLevel, create_wh, setup_logging, wh_exists

app = typer.Typer(
    name=f'Snow Instructor {__version__} Deployment',
    help='This prepares everything for your Streamlit Snowflake deployment',
)


def grant_public_role():
    """Grant the public role to the warehouse"""
    session = Session.builder.getOrCreate()
    query = f"""
        GRANT USAGE ON DATABASE {SNOWINSTRUCTOR_DB} TO ROLE PUBLIC;
        GRANT USAGE ON SCHEMA {SNOWINSTRUCTOR_DB}.PUBLIC TO ROLE PUBLIC;
        GRANT CREATE STREAMLIT ON SCHEMA {SNOWINSTRUCTOR_DB}.PUBLIC TO ROLE PUBLIC;
        GRANT CREATE STAGE ON SCHEMA {SNOWINSTRUCTOR_DB}.PUBLIC TO ROLE PUBLIC;
        GRANT USAGE ON WAREHOUSE {SNOWINSTRUCTOR_WH} TO ROLE PUBLIC;
    """
    for statement in query.strip().split(';'):
        if statement := statement.strip():
            session.sql(statement).collect()


@app.command()
def main(
    connection_name: Annotated[str, typer.Option(help='Connection name')] = 'default',
    log_level: Annotated[LogLevel, typer.Option(help='Log level')] = LogLevel.INFO,
):
    setup_logging(log_level)
    Session.builder.config('connection_name', connection_name).create()

    if not wh_exists(SNOWINSTRUCTOR_WH):
        create_wh(SNOWINSTRUCTOR_WH, create_mode='IF_NOT_EXISTS')
        print(f'Warehouse {SNOWINSTRUCTOR_WH} created successfully!')  # noqa: T201
    else:
        print(f'Warehouse {SNOWINSTRUCTOR_WH} already exists!')  # noqa: T201

    print('Granting public role...')  # noqa: T201
    grant_public_role()

    print('Deployment completed successfully!')  # noqa: T201
    print('You can now deploy the Streamlit app using `hatch run snow streamlit deploy --replace`')  # noqa: T201


if __name__ == '__main__':
    app()
