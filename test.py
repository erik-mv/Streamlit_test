import streamlit as st
import numpy as np

from plot import plot_ecdf_dict, plot_power_dict, plot_hist

st.write('# Применение ML для ускорения А/В тестирования')

st.write(
    """
Всем, привет! В данной работе рассмотрены способы ускорения
__switch-back A/B__ тестов. Работу выполнили студенты академии
больших данных __MADE__ в качестве выпускного проекта. 

- __Шевчук Анастасия__ – EDA, классические методы
- __Чаусов Дмитрий__ – EDA, ML-методы
- __Гудков Дмитрий__ – EDA, ML-методы
- __Дронов Артем__ – EDA, разработка пайплайна, визуализация
- __Муллагалиев Эрик__ – EDA, разработка пайплайна, визуализация

Автором идеи и ментор выступил __Максимов Иван__ - Data Scientist в __Delivery Club__.

Исследование проводится на синтетических данных, сгенерированных на основе реальных данных, предоставленных __Delivery Club__.
    """
)

st.write(
    """
## Оглавление
* __Вводная часть:__
    * [1. Введение](#introduction)
    * [2. Постановка задачи](#problem_statement)
    * [3. Baseline](#baseline)
* __Классические методы ускорения:__
    * [4. Фильтрация выбросов распределения](#filtering)
    * [5. Стратификация](#stratification)
    * [6. CUPED](#cuped)
    * [7. Линеаризация](#linearization)
* __ML-метод ускорения:__
    * [7. CUPAC](#cupac)
    """
)

st.write(
    """
## Baseline <a name = 'baseline'></a>
    """,
    unsafe_allow_html=True,
)


container_cdf = st.container()
container_param_power_hist = st.container()

col_power_hist, _, col_param = container_param_power_hist.columns([6, 1, 4])
col_cdf_AB, col_cdf_AA = container_cdf.columns(2)

col_param.write("#### Параметры")
std_coef = col_param.slider("Стандортное отклонение", 0.001, 0.01, step=0.00225, format='%f')
zones_corr = col_param.slider("Корреляцмя м/у соседними зонами", 0.1, 0.8, step=0.175, format='%f')
effect_size = col_param.slider("Effect size", 0.002, 0.006, step=0.001, format='%f')
col_param.write("#### Тесты")
checkbox_ttest = col_param.checkbox('ttest', value = True)
checkbox_mannwhitneyu = col_param.checkbox('mannwhitneyu', value = False)
checkbox_bootstrap = col_param.checkbox('bootstrap', value = False)

baseline_test = []
if checkbox_ttest:
    baseline_test.append('ttest')
if checkbox_mannwhitneyu:
    baseline_test.append('mannwhitneyu')
if checkbox_bootstrap:
    baseline_test.append('bootstrap')

if checkbox_ttest + checkbox_mannwhitneyu + checkbox_bootstrap:
    tests_dict={}
    for name_test in baseline_test:
        file_name_AB_test = 'baseline/std_coef_%f_zones_corr_%f_effect_size_%f_%s'%(
                std_coef,
                zones_corr,
                effect_size,
                name_test,
        )
        file = open(file_name_AB_test, 'r')
        power = float(file.readline())
        AB_test = np.array(file.readline().split()).astype(float)
        AB_cdf_x = np.array(file.readline().split()).astype(float)
        AB_cdf_y = np.array(file.readline().split()).astype(float)
        file.close()
        
        file_name_AA_test = 'baseline/std_coef_%f_zones_corr_%f_effect_size_%f_%s'%(
                std_coef,
                zones_corr,
                0.0,
                name_test,
        )
        file = open(file_name_AA_test, 'r')
        alfa = float(file.readline())
        AA_test = np.array(file.readline().split()).astype(float)
        AA_cdf_x = np.array(file.readline().split()).astype(float)
        AA_cdf_y = np.array(file.readline().split()).astype(float)
        file.close()

        tests_dict[name_test]={
            'power': power,
            'AB_test': AB_test,
            'AB_cdf_x': AB_cdf_x,
            'AB_cdf_y': AB_cdf_y,
            'alfa': alfa,
            'AA_test': AA_test,
            'AA_cdf_x': AA_cdf_x,
            'AA_cdf_y': AA_cdf_y,
        }

    col_cdf_AB.write("#### Simulated p-value CDFs under H1")
    col_cdf_AB.pyplot(plot_ecdf_dict(tests_dict=tests_dict, test_v='AB', plot_legend=True))
    col_cdf_AA.write("#### Simulated p-value CDFs under H0")
    col_cdf_AA.pyplot(plot_ecdf_dict(tests_dict=tests_dict, test_v='AA'))
    col_power_hist.write("#### Power")
    col_power_hist.pyplot(plot_power_dict(tests_dict=tests_dict))

    file_name_hist = 'hist/std_coef_%f_zones_corr_%f_effect_size_%f'%(
                std_coef,
                zones_corr,
                effect_size,
    )
    file = open(file_name_hist, 'r')
    value = np.array(file.readline().split()).astype(float)
    file.close()

    col_power_hist.write("#### Hist")
    col_power_hist.pyplot(plot_hist(value))
