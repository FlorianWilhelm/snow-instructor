import logging

import typer
from markdownify import markdownify
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.utils.project import get_project_settings
from snowflake.snowpark import Session
from typing_extensions import Annotated

from snow_instructor import __version__
from snow_instructor.settings import SNOWDOCS_TABLE
from snow_instructor.utils import LogLevel, table_exists

_logger = logging.getLogger(__name__)


class SnowSpider(CrawlSpider):
    name = 'Snowflake Documentation'
    allowed_domains = ['docs.snowflake.com']
    start_urls = ['https://docs.snowflake.com/guides', 'https://docs.snowflake.com/developer']

    rules = (
        Rule(LinkExtractor(allow=('/en/user-guide/', '/en/developer-guide/')),
             callback='parse_item', follow=True),
    )
    items = []

    def parse_item(self, response):
        crumbs = response.css('#scrolltarget div div nav span::text, #scrolltarget div div nav a::text').getall()
        html = response.css('#scrolltarget').get()
        url = response.url
        title = response.xpath('//title/text()').get().split('|')[0]

        if html:
            markdown = markdownify(html)
            self.items.append({'title': title, 'url': url, 'toc': crumbs, 'content': markdown})


def assert_snowdocs_table():
    session = Session.builder.getOrCreate()
    current_database = session.get_current_database()
    session.sql(f'CREATE DATABASE IF NOT EXISTS {current_database}').collect()

    if not table_exists(SNOWDOCS_TABLE):
        session.sql(f"""
            CREATE TABLE {SNOWDOCS_TABLE} (
                title STRING,
                url STRING,
                toc VARIANT,
                content STRING
            )
        """).collect()


def add_items_to_snowdocs_table(items):
    session = Session.builder.getOrCreate()
    df = session.create_dataframe(items)
    df.write.mode('append').save_as_table(SNOWDOCS_TABLE)


app = typer.Typer(
    name=f'Snow Instructor {__version__} Crawler',
    help="This spider crawls Snowflake's docs to generate quiz questions."
)


@app.command()
def main(log_level: Annotated[LogLevel, typer.Option(help='Log level')] = LogLevel.WARNING,
         connection_name: Annotated[str, typer.Option(help='Connection name')] = 'default'):
    Session.builder.config('connection_name', connection_name).create()
    assert_snowdocs_table()
    cfg = get_project_settings()
    cfg['LOG_LEVEL'] = log_level.name
    process = CrawlerProcess(cfg)
    process.crawl(SnowSpider)
    process.start()
    add_items_to_snowdocs_table(SnowSpider.items)


if __name__ == '__main__':
    main()
