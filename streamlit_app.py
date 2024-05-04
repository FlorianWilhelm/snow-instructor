import streamlit as st

from snow_instructor.utils import LogLevel, setup_logging

st.set_page_config(page_title='Snowflake Instructor', page_icon='⛷️')
setup_logging(LogLevel(st.config.get_option('logger.level').lower()))

st.title('❄️ Your Snowflake Instructor ❄️')
_, center, _ = st.columns([1, 3, 1])
center.image('assets/snow-instructor.png', width=300)

if center.columns((1, 8, 1))[1].button('Start the Snowflake Quiz!'):
    st.switch_page('pages/snow_quiz.py')
