import random
from typing import Dict, List

import typer
from snowflake.snowpark import Session
from typing_extensions import Annotated

from snow_instructor import __version__
from snow_instructor.arctic import QuizQuestion, chunk, query_quiz_prompt
from snow_instructor.utils import LogLevel, get_snowdocs_table, setup_logging

MIN_TEXT_LEN_FOR_QUESTION = 2000  # we assume that's long enough to generate a good question


def generate_quiz(snowdocs: List[Dict[str, str]]) -> QuizQuestion:
    """Generate a quiz question based on the content of the Snowflake documentation"""
    while True:
        page = random.choice(snowdocs)  # noqa: S311
        content = random.choice(chunk(page['content']))  # noqa: S311
        if len(content) > MIN_TEXT_LEN_FOR_QUESTION:
            try:
                question = query_quiz_prompt(content)
            except ValueError:
                continue

            if question.is_valid:
                question.source = page
                return question


app = typer.Typer(
    name=f'Snow Instructor {__version__}',
    help="LLM instructor that teaches you about Snowflake's capabilities.",
)


@app.command()
def main(
    connection_name: Annotated[str, typer.Option(help='Connection name')] = 'default',
    log_level: Annotated[LogLevel, typer.Option(help='Log level')] = LogLevel.INFO,
):
    """Wrapper allowing :func:`fib` to be called with string arguments in a CLI fashion

    Instead of returning the value from :func:`fib`, it prints the result to the
    `stdout` in a nicely formatted message.
    """
    setup_logging(log_level)
    Session.builder.config('connection_name', connection_name).create()

    snowdocs = get_snowdocs_table()
    question = generate_quiz(snowdocs)
    print(f'Question: {question.question}')  # noqa: T201
    for i, answer in enumerate(question.answers):
        print(f'{chr(65 + i)}: {answer}')  # noqa: T201
    answer = input('Enter the correct answer (A, B, C, D): ')
    if answer.upper() == chr(65 + question.correct_answer):
        print('Correct!')  # noqa: T201
    else:
        print('Incorrect! The correct answer is:', chr(65 + question.correct_answer))  # noqa: T201

    print(f'Source: {question.source["url"]}')  # noqa: T201


if __name__ == '__main__':
    app()
