import streamlit as st
import numpy as np
from plot import plot_ecdf_dict, plot_power_dict, plot_hist

def sbar():
    sidebar = st.sidebar

    sidebar.write('# Навигатор')
    cheak_name = sidebar.radio('', (
        'Введение',
        'Постановка задачи',
        'Baseline',
        'Фильтрация выбросов распределения',
        'Стратификация',
        'CUPED',
        'Линеаризация',
        'CUPAC',
    ))
    
    return sidebar, cheak_name

def introduction():  
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

def get_checkbox_slider(sidebar, names_test, std_coef, zones_corr, effect_size):
    sidebar.write("# Тесты")
    checkbox = []
    for name_test in names_test:
        checkbox.append(sidebar.checkbox(name_test, value = True))

    activ_names_test = []
    for i in range(len(checkbox)):
        if checkbox[i]:
            activ_names_test.append(names_test[i])
    
    sidebar.write("# Параметры")
    std_coef = sidebar.slider(
        "Стандортное отклонение",
        std_coef['start'],
        std_coef['stop'],
        step=std_coef['step'],
        format='%f',
    )
    zones_corr = sidebar.slider(
        "Корреляцмя м/у соседними зонами",
        zones_corr['start'],
        zones_corr['stop'],
        step=zones_corr['step'],
        format='%f',
    )
    effect_size = sidebar.slider(
        "Effect size",
        effect_size['start'],
        effect_size['stop'],
        step=effect_size['step'],
        format='%f',
    )

    _, col_cdf, _, col_power_hist, _ = st.columns((3, 10, 3, 13, 3))

    return activ_names_test, std_coef, zones_corr, effect_size, col_cdf, col_power_hist 

def plot_power_and_hist(col_power_hist, tests_dict, file_name_hist):
    col_power_hist.write("#### Power")
    col_power_hist.pyplot(plot_power_dict(tests_dict=tests_dict))

    file = open(file_name_hist, 'r')
    value = np.array(file.readline().split()).astype(float)
    file.close()

    col_power_hist.write("#### Hist")
    col_power_hist.pyplot(plot_hist(value))

def baseline(sidebar):
    (
        activ_names_test,
        std_coef,
        zones_corr,
        effect_size,
        col_cdf,
        col_power_hist
    ) = get_checkbox_slider(
            sidebar, 
            names_test=['ttest', 'mannwhitneyu', 'bootstrap'], 
            std_coef={'start': 0.001, 'stop': 0.01, 'step': 0.00225},
            zones_corr={'start': 0.1, 'stop': 0.8, 'step': 0.175},
            effect_size={'start': 0.002, 'stop': 0.006, 'step': 0.001},
            )

    if (len(activ_names_test)):
        tests_dict={}
        for name_test in activ_names_test:
            file_name_AB_test = get_file_name_test('baseline/', std_coef, zones_corr, effect_size, name_test)
            power, AB_test, AB_cdf_x, AB_cdf_y = read_file_test(file_name_AB_test)
        
            file_name_AA_test = get_file_name_test('baseline/', std_coef, zones_corr, 0.0, name_test)
            alfa, AA_test, AA_cdf_x, AA_cdf_y = read_file_test(file_name_AA_test)

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

        col_cdf.write("#### CDFs under H1")
        col_cdf.pyplot(plot_ecdf_dict(tests_dict=tests_dict, test_v='AB', plot_legend=True))
        col_cdf.write("#### CDFs under H0")
        col_cdf.pyplot(plot_ecdf_dict(tests_dict=tests_dict, test_v='AA'))


        file_name_hist = 'hist/std_coef_%f_zones_corr_%f_effect_size_%f'%(
            std_coef,
            zones_corr,
            effect_size,
        )
        plot_power_and_hist(col_power_hist, tests_dict, file_name_hist)

def outliers(sidebar):
    (
        activ_names_test,
        std_coef,
        zones_corr,
        effect_size,
        col_cdf,
        col_power_hist
    ) = get_checkbox_slider(
            sidebar, 
            names_test=['ttest', 'mannwhitneyu', 'bootstrap'], 
            std_coef={'start': 0.0055, 'stop': 0.0055, 'step': 0.00225},
            zones_corr={'start': 0.625, 'stop': 0.625, 'step': 0.175},
            effect_size={'start': 0.005, 'stop': 0.005, 'step': 0.001},
            )

    if (len(activ_names_test)):
        tests_dict={}
        for name_test in activ_names_test:
            file_name_AB_test = get_file_name_test('outliers/', std_coef, zones_corr, effect_size, name_test)
            power, AB_test, AB_cdf_x, AB_cdf_y = read_file_test(file_name_AB_test)
        
            file_name_AA_test = get_file_name_test('outliers/', std_coef, zones_corr, 0.0, name_test)
            alfa, AA_test, AA_cdf_x, AA_cdf_y = read_file_test(file_name_AA_test)

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

        col_cdf.write("#### CDFs under H1")
        col_cdf.pyplot(plot_ecdf_dict(tests_dict=tests_dict, test_v='AB', plot_legend=True))
        col_cdf.write("#### CDFs under H0")
        col_cdf.pyplot(plot_ecdf_dict(tests_dict=tests_dict, test_v='AA'))


        file_name_hist = 'hist/std_coef_%f_zones_corr_%f_effect_size_%f'%(
            std_coef,
            zones_corr,
            effect_size,
        )
        plot_power_and_hist(col_power_hist, tests_dict, file_name_hist)

def stratification(sidebar):
    (
        activ_names_test,
        std_coef,
        zones_corr,
        effect_size,
        col_cdf,
        col_power_hist
    ) = get_checkbox_slider(
            sidebar, 
            names_test=['ttest', 'mannwhitneyu', 'bootstrap'], 
            std_coef={'start': 0.0055, 'stop': 0.0055, 'step': 0.00225},
            zones_corr={'start': 0.625, 'stop': 0.625, 'step': 0.175},
            effect_size={'start': 0.005, 'stop': 0.005, 'step': 0.001},
            )

    if (len(activ_names_test)):
        tests_dict={}
        for name_test in activ_names_test:
            file_name_AB_test = get_file_name_test('stratification/', std_coef, zones_corr, effect_size, name_test)
            power, AB_test, AB_cdf_x, AB_cdf_y = read_file_test(file_name_AB_test)
        
            file_name_AA_test = get_file_name_test('stratification/', std_coef, zones_corr, 0.0, name_test)
            alfa, AA_test, AA_cdf_x, AA_cdf_y = read_file_test(file_name_AA_test)

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

        col_cdf.write("#### CDFs under H1")
        col_cdf.pyplot(plot_ecdf_dict(tests_dict=tests_dict, test_v='AB', plot_legend=True))
        col_cdf.write("#### CDFs under H0")
        col_cdf.pyplot(plot_ecdf_dict(tests_dict=tests_dict, test_v='AA'))


        file_name_hist = 'hist/std_coef_%f_zones_corr_%f_effect_size_%f'%(
            std_coef,
            zones_corr,
            effect_size,
        )
        plot_power_and_hist(col_power_hist, tests_dict, file_name_hist)

def cuped(sidebar):
    (
        activ_names_test,
        std_coef,
        zones_corr,
        effect_size,
        col_cdf,
        col_power_hist
    ) = get_checkbox_slider(
            sidebar, 
            names_test=['ttest', 'mannwhitneyu', 'bootstrap'], 
            std_coef={'start': 0.0055, 'stop': 0.0055, 'step': 0.00225},
            zones_corr={'start': 0.625, 'stop': 0.625, 'step': 0.175},
            effect_size={'start': 0.005, 'stop': 0.005, 'step': 0.001},
            )

    if (len(activ_names_test)):
        tests_dict={}
        for name_test in activ_names_test:
            file_name_AB_test = get_file_name_test('cuped/', std_coef, zones_corr, effect_size, name_test)
            power, AB_test, AB_cdf_x, AB_cdf_y = read_file_test(file_name_AB_test)
        
            file_name_AA_test = get_file_name_test('cuped/', std_coef, zones_corr, 0.0, name_test)
            alfa, AA_test, AA_cdf_x, AA_cdf_y = read_file_test(file_name_AA_test)

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

        col_cdf.write("#### CDFs under H1")
        col_cdf.pyplot(plot_ecdf_dict(tests_dict=tests_dict, test_v='AB', plot_legend=True))
        col_cdf.write("#### CDFs under H0")
        col_cdf.pyplot(plot_ecdf_dict(tests_dict=tests_dict, test_v='AA'))


        file_name_hist = 'hist/std_coef_%f_zones_corr_%f_effect_size_%f'%(
            std_coef,
            zones_corr,
            effect_size,
        )
        plot_power_and_hist(col_power_hist, tests_dict, file_name_hist)

def navigation(sidebar, cheak_name):
    if cheak_name == 'Введение':
        introduction()
    elif cheak_name == 'Baseline':
        baseline(sidebar)
    elif cheak_name == 'Фильтрация выбросов распределения':
        outliers(sidebar)
    elif cheak_name == 'Стратификация':
        stratification(sidebar)
    elif cheak_name == 'CUPED':
        cuped(sidebar)
        
