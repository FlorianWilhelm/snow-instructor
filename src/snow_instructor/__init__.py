"""Ultimate Notion provides a pythonic, high-level API for Notion

Notion-API: https://developers.notion.com/reference/intro
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__: str = version('snow-instructor')
except PackageNotFoundError:  # pragma: no cover
    __version__ = 'unknown'
finally:
    del version, PackageNotFoundError

from snow_instructor.llm import QuizQuestion
from snow_instructor.main import generate_quiz
from snow_instructor.utils import get_snowdocs_table

__all__ = ['QuizQuestion', 'generate_quiz', 'get_snowdocs_table']
