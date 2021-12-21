import streamlit as st
import numpy as np
from plot import plot_ecdf_dict, plot_power_dict, plot_hist
import os

def sbar():
    sidebar = st.sidebar

    sidebar.write("# Масштабирование графиков")
    scale = sidebar.slider("Масштаб", 1, 20, step=1)
    scale = int(scale)

    sidebar.write('# Навигатор')
    cheak_name = sidebar.radio('', ('Baseline', 'Оптимизации'))

    sidebar.write("# Параметры")
    std_coef = sidebar.slider(
        "Стандартное отклонение",
        0.001,
        0.01,
        step=0.00225,
        format='%f',
    )

    zones_corr = sidebar.slider(
        "Корреляция между соседними зонами",
        0.1,
        0.8,
        step=0.175,
        format='%f',
    )
    effect_size = sidebar.slider(
        "Размер эффекта",
        0.002,
        0.006,
        step=0.001,
        format='%f',
    )

    _, col_cdf, _, col_power_hist, _ = st.columns((scale, 11, 2, 14, scale))

    activ_names_test = []
    sidebar.write("# Тесты")
    if cheak_name == 'Baseline':
        checkbox_ttest = sidebar.checkbox('T-тест', value = True)
        checkbox_mannwhitneyu = sidebar.checkbox('U-тест', value = False)
        checkbox_bootstrap = sidebar.checkbox('Bootstrap', value = False)

        if checkbox_ttest:
            activ_names_test.append(['T-тест', 'baseline/', 'ttest'])
        if checkbox_mannwhitneyu:
            activ_names_test.append(['U-тест', 'baseline/', 'mannwhitneyu'])
        if checkbox_bootstrap:
            activ_names_test.append(['Bootstrap', 'baseline/', 'bootstrap'])
    else:
        checkbox_baseline = sidebar.checkbox('Baseline', value = True)
        checkbox_outliers = sidebar.checkbox('Фильтрация выбросов', value = False)
        checkbox_stratification = sidebar.checkbox('Стратификация', value = False)
        checkbox_cuped = sidebar.checkbox('CUPED', value = False)
        checkbox_cupac = sidebar.checkbox('CUPAC', value = False)

        if checkbox_baseline:
            activ_names_test.append(['Baseline', 'baseline/', 'bootstrap'])
        if checkbox_outliers:
            activ_names_test.append(['Фильтрация', 'outliers/', 'bootstrap'])
        if checkbox_stratification:
            activ_names_test.append(['Стратификация', 'stratification/', 'bootstrap'])
        if checkbox_cuped:
            activ_names_test.append(['CUPED', 'cuped/', 'bootstrap'])
        if checkbox_cupac:
            activ_names_test.append(['CUPAC', 'cupac/', 'bootstrap'])

    return col_cdf, col_power_hist, activ_names_test, std_coef, zones_corr, effect_size

def get_file_name_test(path_folder, std_coef, zones_corr, effect_size, name_test):
    return '%sstd_coef_%f_zones_corr_%f_effect_size_%f_%s'%(
        path_folder,
        std_coef,
        zones_corr,
        effect_size,
        name_test,
    )

def read_file_test(file_name_test):
    file = open(file_name_test, 'r')
    power = float(file.readline())
    test = np.array(file.readline().split()).astype(float)
    cdf_x = np.array(file.readline().split()).astype(float)
    cdf_y = np.array(file.readline().split()).astype(float)
    file.close()

    return power, test, cdf_x, cdf_y

def plot_power_and_hist(col_power_hist, tests_dict, file_name_hist):
    col_power_hist.write("Мощность критериев")
    col_power_hist.pyplot(plot_power_dict(tests_dict=tests_dict))

    file = open(file_name_hist, 'r')
    value = np.array(file.readline().split()).astype(float)
    file.close()

    col_power_hist.write("Распределение данных в контрольных группах")
    col_power_hist.pyplot(plot_hist(value))

def navigation(col_cdf, col_power_hist, activ_names_test, std_coef, zones_corr, effect_size):
    if (len(activ_names_test)):
        tests_dict={}
        for name_test in activ_names_test:
            file_name_AB_test = get_file_name_test(name_test[1], std_coef, zones_corr, effect_size, name_test[2])
            power = 0
            AB_test = []
            AB_cdf_x = []
            AB_cdf_y = []
            if os.path.exists(file_name_AB_test):
                power, AB_test, AB_cdf_x, AB_cdf_y = read_file_test(file_name_AB_test)

            file_name_AA_test = get_file_name_test(name_test[1], std_coef, zones_corr, 0.0, name_test[2])
            alfa = 0
            AA_test = []
            AA_cdf_x = []
            AA_cdf_y = []
            if os.path.exists(file_name_AA_test):
                alfa, AA_test, AA_cdf_x, AA_cdf_y = read_file_test(file_name_AA_test)

            tests_dict[name_test[0]]={
                'power': power,
                'AB_test': AB_test,
                'AB_cdf_x': AB_cdf_x,
                'AB_cdf_y': AB_cdf_y,
                'alfa': alfa,
                'AA_test': AA_test,
                'AA_cdf_x': AA_cdf_x,
                'AA_cdf_y': AA_cdf_y,
            }

        col_cdf.write("Распределение p-value AB-тестов")
        col_cdf.pyplot(plot_ecdf_dict(tests_dict=tests_dict, test_v='AB', plot_legend=True))
        col_cdf.write("Распределение p-value AA-тестов")
        col_cdf.pyplot(plot_ecdf_dict(tests_dict=tests_dict, test_v='AA', plot_legend=True))


        file_name_hist = 'hist/std_coef_%f_zones_corr_%f_effect_size_%f'%(
            std_coef,
            zones_corr,
            effect_size,
        )
        plot_power_and_hist(col_power_hist, tests_dict, file_name_hist)