import streamlit as st
from streamlit_navigation import sbar, navigation

st.set_page_config(layout="wide")

# st.write('# Применение ML для ускорения switchback A/B тестирования')

col_cdf, col_power_hist, activ_names_test, std_coef, zones_corr, effect_size = sbar()
navigation(col_cdf, col_power_hist, activ_names_test, std_coef, zones_corr, effect_size)
