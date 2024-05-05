import logging
import re
from dataclasses import dataclass
from typing import Dict, List, Tuple, Union

from snowflake import cortex
from snowflake.snowpark import Session
from transformers import GPT2Tokenizer

_logger = logging.getLogger(__name__)


QUIZ_PROMPT = ('Based on the following excerpt from the Snowflake documentation, generate a multiple-choice question '
               'that tests understanding of the key concept discussed. Include four answer choices and indicate the '
               'correct answer.\n{text}')


@dataclass
class QuizQuestion:
    question: str
    answers: Tuple[str, str, str, str]
    correct_answer: int
    source: Union[Dict[str, str], None] = None

    @property
    def is_valid(self) -> bool:
        return len(self.answers) == 4 and 0 <= self.correct_answer <= 3  # noqa: PLR2004


def chunk(text: str, max_tokens: Union[int, None] = None) -> List[str]:
    if max_tokens is None:
        max_tokens = int(0.9 * 4096)  # 90% of the arctic's max token length

    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')  # assuming that arctic tokenizes the same way
    tokens = tokenizer.tokenize(text)
    chunks = [tokens[i:i + max_tokens] for i in range(0, len(tokens), max_tokens)]
    return [tokenizer.convert_tokens_to_string(chunk) for chunk in chunks]


def query_arctic(prompt: str) -> str:
    session = Session.builder.getOrCreate()
    return cortex.Complete(model='snowflake-arctic', prompt=prompt, session=session)


def parse_arctic_response(text: str) -> QuizQuestion:
    parts = re.split(r'\n\s*\n+', text.strip())
    if len(parts) != 3:  # noqa: PLR2004
        msg = 'Reponse of Arctic does not have the expected format. We have {len(parts)} parts instead of 3.'
        raise ValueError(msg)
    question, answers, correct_answer = parts

    match = re.search(r'[Aa][:).] (.+?)\n[Bb][:).] (.+?)\n[Cc][:).] (.+?)\n[Dd][:).] (.+?)$', answers)
    if match is None:
        msg = f'Could not parse the quiz answers from Arctic. Answers:\n{answers}'
        raise ValueError(msg)
    answers = match.groups()

    match = re.search(r'Correct.*: ([A-Da-d])', correct_answer)
    if match is None:
        msg = f'Could not parse the correct answer from Arctic. Correct answer:\n{correct_answer}'
        raise ValueError(msg)
    correct_answer = match.groups()[0].upper()

    return QuizQuestion(question=question, answers=tuple(answers), correct_answer=ord(correct_answer) - 65)


def query_quiz_prompt(text: str) -> QuizQuestion:
    prompt = QUIZ_PROMPT.format(text=text)
    _logger.debug(f'Querying Arctic with prompt:\n{prompt}]')
    response = query_arctic(prompt=prompt)
    _logger.debug(f'Arctic response:\n{response}')
    return parse_arctic_response(response)
