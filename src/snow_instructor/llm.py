import logging
import re
from dataclasses import dataclass
from typing import Dict, List, Tuple, Union

from snowflake import cortex
from snowflake.snowpark import Session
from transformers import GPT2Tokenizer

from snow_instructor.settings import LLM_MODEL, LLM_MODEL_WINDOW_SIZE, QUIZ_PROMPT

_logger = logging.getLogger(__name__)


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
        max_tokens = int(0.8 * LLM_MODEL_WINDOW_SIZE)  # 80% of the LLM's max token length to be sure!

    # Following code downloads the tokenizer from Hugging Face's model hub
    # tokenizer = GPT2Tokenizer.from_pretrained('gpt2')  # assuming that the LLM tokenizes the same way
    # tokenizer.save_pretrained('assets/gpt2-tokenizer')  # save the tokenizer to disk
    tokenizer = GPT2Tokenizer.from_pretrained('assets')  # load the tokenizer from disk
    tokens = tokenizer.tokenize(text)
    chunks = [tokens[i : i + max_tokens] for i in range(0, len(tokens), max_tokens)]
    return [tokenizer.convert_tokens_to_string(chunk) for chunk in chunks]


def query_llm(prompt: str) -> str:
    session = Session.builder.getOrCreate()
    return cortex.Complete(model=LLM_MODEL, prompt=prompt, session=session)


def parse_llm_response(text: str) -> QuizQuestion:
    # Extract the question
    question_pattern = r'\*\*Question:\*\* (.+)'
    question_match = re.search(question_pattern, text)
    question = question_match.group(1).strip() if question_match else ''

    # Extract the answers
    answers_pattern = r'\*\*(A|B|C|D)\)\*\* (.+)'
    answers_matches = re.findall(answers_pattern, text)
    answers = tuple(answer for _, answer in answers_matches)

    # Extract the correct answer
    correct_answer_pattern = r'\*\*Correct answer:\*\* (A|B|C|D)'
    correct_answer_match = re.search(correct_answer_pattern, text)
    correct_answer = ord(correct_answer_match.group(1)) - ord('A') if correct_answer_match else -1

    return QuizQuestion(question=question, answers=answers, correct_answer=correct_answer)


def query_quiz_prompt(text: str) -> QuizQuestion:
    prompt = QUIZ_PROMPT.format(text=text)
    _logger.debug(f'Querying LLM with prompt:\n{prompt}]')
    response = query_llm(prompt=prompt)
    _logger.debug(f'LLM response:\n{response}')
    return parse_llm_response(response)
