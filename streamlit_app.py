import streamlit as st

from snow_instructor.utils import LogLevel, setup_logging, streamlit_on_snowflake

st.set_page_config(page_title='Snowflake Instructor', page_icon='⛷️')
setup_logging(LogLevel(st.config.get_option('logger.level').lower()))

st.title('❄️ Your Snowflake Instructor ❄️')
_, center, _ = st.columns([1, 3, 1])
center.image('assets/snow-instructor.png', width=300)

if center.columns((1, 8, 1))[1].button('Start the Snowflake Quiz!'):
    if not streamlit_on_snowflake():
        st.switch_page('pages/snow_quiz.py')
    else:
        st.success('⬅️ Click on `snow quiz` in the sidebar to start the quiz!')
