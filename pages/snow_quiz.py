import logging
import time

import streamlit as st
from snowflake.snowpark import Session

import snow_instructor

_logger = logging.getLogger(__name__)


# def show_timer():
#     st.toast("Time's up!", icon="⏰")
#     with st.empty():
#         for seconds in range(60):
#             st.write(f"⏳ {seconds} seconds have passed")
#             time.sleep(1)
#         st.write("✔️ 1 minute over!")


@st.cache_data
def get_snowdocs_table():
    _logger.info('Fetching Snowflake documentation...')
    return snow_instructor.get_snowdocs_table()


def generate_quiz() -> snow_instructor.QuizQuestion:
    """Generate a quiz question based on the content of the Snowflake documentation"""
    _logger.info('Generating a quiz question...')
    Session.builder.config('connection_name', 'default').getOrCreate()
    snowdocs = get_snowdocs_table()
    question = snow_instructor.generate_quiz(snowdocs)
    return question


class ButtonPress:
    def __init__(self, correct_answer_id: int) -> None:
        self.correct_answer_id = correct_answer_id

    def __call__(self, button_id: int):
        if st.session_state.correct_answer is None:
            st.session_state.correct_answer = button_id == self.correct_answer_id


def main():
    st.set_page_config(page_title='Snowflake Instructor', layout='centered', page_icon='⛷️')
    st.session_state.setdefault('correct_answer', None)
    st.session_state.setdefault('curr_quiz', None)

    left, center, right = st.columns([1, 3, 1])
    center.image('assets/snow-instructor.png', use_column_width=True)
    with center.chat_message('ai'):
        st.write("Let's start the quiz! You have 1 minute to answer the questions.")

    if st.session_state.curr_quiz is None:
        st.session_state.curr_quiz = generate_quiz()

    quiz = st.session_state.curr_quiz

    button_press = ButtonPress(quiz.correct_answer)
    placeholder = st.empty()
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
            st.balloons()
        elif st.session_state.correct_answer is False:
            st.error(f'Incorrect! The correct answer is **{chr(65 + quiz.correct_answer)}**. '
                    f'[Find out more]({quiz.source["url"]})...')

        if st.session_state.correct_answer is not None and st.button('Next Question'):
            st.session_state.curr_quiz = None
            st.session_state.correct_answer = None
            #st.rerun()
            st.experimental_rerun()


if __name__ == '__main__':
    main()
