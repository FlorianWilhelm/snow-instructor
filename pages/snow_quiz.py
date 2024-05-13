import logging
import time
from concurrent.futures import Future, ThreadPoolExecutor
from random import choice
from typing import Union

import streamlit as st
from snowflake.snowpark import Session
from streamlit.runtime.state import SessionState

import snow_instructor
from snow_instructor.settings import CORRECT_COMMENTS, INCORRECT_COMMENTS, START_COMMENTS
from snow_instructor.utils import streamlit_on_snowflake

_logger = logging.getLogger(__name__)
_executor = ThreadPoolExecutor(max_workers=1)


@st.cache_data
def get_snowdocs_table():
    _logger.info('Fetching Snowflake documentation...')
    return snow_instructor.get_snowdocs_table()


def generate_quiz(*, sync: bool) -> Union[Future, snow_instructor.QuizQuestion]:
    """Generate a quiz question based on the content of the Snowflake documentation"""
    _logger.info('Generating a quiz question...')

    if sync:
        placeholder = st.empty()
        with placeholder, st.spinner('Connecting to Snowflake...'):
            try:
                Session.builder.getOrCreate()
            except Exception:
                Session.builder.config('connection_name', 'default').create()
        with placeholder, st.spinner('Reading Snowflake documentation...'):
            snowdocs = get_snowdocs_table()
        with placeholder, st.spinner('Generating a quiz question...'):
            return snow_instructor.generate_quiz(snowdocs)
    else:
        snowdocs = get_snowdocs_table()
        return _executor.submit(snow_instructor.generate_quiz, snowdocs)


def prefetch_generate_quiz(state: SessionState) -> None:
    """version of `generate_quiz` with prefetching of the next question."""
    if state.next_quiz is None:
        state.curr_quiz = generate_quiz(sync=True)
    elif not state.next_quiz.done():
        with st.empty(), st.spinner('Generating a quiz question...'):
            state.curr_quiz = state.next_quiz.result()
    else:
        state.curr_quiz = state.next_quiz.result()
    state.next_quiz = generate_quiz(sync=False)


class ButtonPress:
    def __init__(self, correct_answer_id: int) -> None:
        self.correct_answer_id = correct_answer_id

    def __call__(self, button_id: int):
        st.session_state.correct_answer = button_id == self.correct_answer_id
        st.session_state.round_finished = True


def refresh():
    time.sleep(0.1)  # this avoids slow fade out effect
    if streamlit_on_snowflake():
        st.experimental_rerun()
    else:
        st.rerun()


def main():
    st.set_page_config(page_title='Snowflake Instructor', layout='centered', page_icon='⛷️')
    st.session_state.setdefault('round_finished', False)
    st.session_state.setdefault('comments_chosen', False)
    st.session_state.setdefault('correct_answer', None)
    st.session_state.setdefault('curr_quiz', None)
    st.session_state.setdefault('next_quiz', None)
    st.session_state.setdefault('fails', 0)
    st.session_state.setdefault('wins', 0)

    if not st.session_state.comments_chosen:
        st.session_state.comments = choice(START_COMMENTS), choice(CORRECT_COMMENTS), choice(INCORRECT_COMMENTS)  # noqa: S311
        st.session_state.comments_chosen = True

    start, correct, incorrect = st.session_state.comments

    left, center, right = st.columns([2, 3, 2])
    right.header(f'**❄️: {st.session_state.wins}&nbsp;&nbsp;&nbsp;🤦‍♀️: {st.session_state.fails}**')
    # right.header(f'**✔️: {st.session_state.wins}&nbsp;&nbsp;&nbsp;✖️: {st.session_state.fails}**')
    center.image('assets/snow-instructor.png', use_column_width=True)
    chat = center.empty()
    if st.session_state.correct_answer is None:
        chat.write(f'*{start}*')

    placeholder = st.empty()
    with placeholder.container():
        if st.session_state.curr_quiz is None:
            prefetch_generate_quiz(st.session_state)
            placeholder.empty()
            refresh()

    quiz = st.session_state.curr_quiz

    button_press = ButtonPress(quiz.correct_answer)

    with placeholder.container():
        st.markdown(f'**Question:** {quiz.question}')

        for idx, (button, answer) in enumerate(zip(('A:', 'B:', 'C:', 'D:'), quiz.answers)):
            with st.container():
                left, right = st.columns([1, 10])
                left.button(button, disabled=st.session_state.round_finished, on_click=button_press, args=(idx,))
                right.markdown(answer)

        if st.session_state.correct_answer is True:
            st.success(f'Correct! [Find out more]({quiz.source["url"]})...')
            chat.write(f'*{correct}*')
            st.balloons()
        elif st.session_state.correct_answer is False:
            st.error(
                f'Incorrect! The correct answer is **{chr(65 + quiz.correct_answer)}**. '
                f'[Find out more]({quiz.source["url"]})...'
            )
            chat.write(f'*{incorrect}*')

        if st.session_state.round_finished and st.button('Next Question'):
            st.session_state.curr_quiz = None
            if st.session_state.correct_answer:
                st.session_state.wins += 1
            else:
                st.session_state.fails += 1
            st.session_state.correct_answer = None
            st.session_state.round_finished = False
            st.session_state.comments_chosen = False
            placeholder.empty()
            refresh()


if __name__ == '__main__':
    main()
