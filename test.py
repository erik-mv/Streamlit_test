import streamlit as st
import numpy as np

from plot import plot_ecdf_dict, plot_power_dict, plot_hist


container_cdf = st.container()
container_param_power_hist = st.container()

col_power_hist, _, col_param = container_param_power_hist.columns([6, 1, 4])
col_cdf_AB, col_cdf_AA = container_cdf.columns(2)

col_param.write("#### Параметры")
#std_coef = st.slider("std_coef", 0.001, 0.01, step=0.00225, format='%f')
std_coef = col_param.slider("Стандортное отклонение", 0.001, 0.0055, step=0.00225, format='%f')
zones_corr = col_param.slider("Корреляцмя м/у соседними зонами", 0.1, 0.8, step=0.175, format='%f')
effect_size = col_param.slider("Effect size", 0.002, 0.006, step=0.001, format='%f')
col_param.write("#### Тесты")
checkbox_ttest = col_param.checkbox('ttest', value = True)
checkbox_mannwhitneyu = col_param.checkbox('mannwhitneyu', value = False)

baseline_test = []
if checkbox_ttest:
    baseline_test.append('ttest')
if checkbox_mannwhitneyu:
    baseline_test.append('mannwhitneyu')

if checkbox_ttest + checkbox_mannwhitneyu:
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
        file.close()

        tests_dict[name_test]={
            'power': power,
            'AB_test': AB_test,
            'alfa': alfa,
            'AA_test': AA_test
        }

    col_cdf_AB.write("#### Simulated p-value CDFs under H1")
    col_cdf_AB.pyplot(plot_ecdf_dict(tests_dict=tests_dict, test_v='AB_test'))
    col_cdf_AA.write("#### Simulated p-value CDFs under H0")
    col_cdf_AA.pyplot(plot_ecdf_dict(tests_dict=tests_dict, test_v='AA_test'))
    col_power_hist.write("#### Power")
    col_power_hist.pyplot(plot_power_dict(tests_dict=tests_dict))
    col_power_hist.write("#### Hist")
    col_power_hist.pyplot(plot_hist(AB_test, AA_test))

    

