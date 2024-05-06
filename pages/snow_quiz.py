import logging
import time
from random import choice

import streamlit as st
from snowflake.snowpark import Session

import snow_instructor
from snow_instructor.settings import CORRECT_COMMENTS, INCORRECT_COMMENTS, START_COMMENTS
from snow_instructor.utils import streamlit_on_snowflake

_logger = logging.getLogger(__name__)


@st.cache_data
def get_snowdocs_table():
    _logger.info('Fetching Snowflake documentation...')
    return snow_instructor.get_snowdocs_table()


def generate_quiz() -> snow_instructor.QuizQuestion:
    """Generate a quiz question based on the content of the Snowflake documentation"""
    _logger.info('Generating a quiz question...')

    placeholder = st.empty()
    with placeholder, st.spinner('Connecting to Snowflake...'):
        Session.builder.config('connection_name', 'default').getOrCreate()
    with placeholder, st.spinner('Reading Snowflake documentation...'):
        snowdocs = get_snowdocs_table()
    with placeholder, st.spinner('Generating a quiz question...'):
        question = snow_instructor.generate_quiz(snowdocs)
    return question


class ButtonPress:
    def __init__(self, correct_answer_id: int) -> None:
        self.correct_answer_id = correct_answer_id

    def __call__(self, button_id: int):
        if st.session_state.correct_answer is None:
            st.session_state.correct_answer = button_id == self.correct_answer_id


def refresh():
    time.sleep(0.1)  # this avoids slow fade out effect
    if streamlit_on_snowflake():
        st.experimental_rerun()
    else:
        st.rerun()


def main():
    st.set_page_config(page_title='Snowflake Instructor', layout='centered', page_icon='⛷️')
    st.session_state.setdefault('new_round', True)
    st.session_state.setdefault('correct_answer', None)
    st.session_state.setdefault('curr_quiz', None)
    st.session_state.setdefault('refresh', False)
    st.session_state.setdefault('ballons', True)

    if st.session_state.new_round:
        st.session_state.comments = choice(START_COMMENTS), choice(CORRECT_COMMENTS), choice(INCORRECT_COMMENTS)  # noqa: S311
        st.session_state.new_round = False

    start, correct, incorrect = st.session_state.comments

    left, center, right = st.columns([2, 3, 2])
    center.image('assets/snow-instructor.png', use_column_width=True)
    chat = center.empty()
    if st.session_state.correct_answer is None:
        chat.write(f'*{start}*')

    placeholder = st.empty()
    with placeholder.container():
        if st.session_state.curr_quiz is None:
            st.session_state.curr_quiz = generate_quiz()
            placeholder.empty()
            refresh()

    quiz = st.session_state.curr_quiz

    button_press = ButtonPress(quiz.correct_answer)

    with placeholder.container():
        st.markdown(f'**Question:** {quiz.question}')

        for idx, (button, answer) in enumerate(zip(('A:', 'B:', 'C:', 'D:'), quiz.answers)):
            with st.container():
                left, right = st.columns([1, 10])
                if left.button(button):
                    button_press(idx)
                right.markdown(answer)

        if st.session_state.correct_answer is True:
            st.success(f'Correct! [Find out more]({quiz.source["url"]})...')
            chat.write(f'*{correct}*')
            if st.session_state.ballons:
                st.balloons()
                st.session_state.ballons = False
        elif st.session_state.correct_answer is False:
            st.error(
                f'Incorrect! The correct answer is **{chr(65 + quiz.correct_answer)}**. '
                f'[Find out more]({quiz.source["url"]})...'
            )
            chat.write(f'*{incorrect}*')

        if st.session_state.correct_answer is not None and st.button('Next Question'):
            st.session_state.curr_quiz = None
            st.session_state.correct_answer = None
            st.session_state.refresh = True

    if st.session_state.refresh:
        st.session_state.refresh = False
        st.session_state.new_round = True
        st.session_state.ballons = True
        placeholder.empty()
        refresh()


if __name__ == '__main__':
    main()
