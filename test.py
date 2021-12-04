import streamlit as st
from streamlit_navigation import sbar, navigation

sidebar, cheak_name = sbar()

st.write('# Применение ML для ускорения А/В тестирования')

navigation(sidebar, cheak_name=cheak_name)
