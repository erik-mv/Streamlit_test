import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

def ecdf(sample):
    """
    Считает x, y для cdf
    :param sample: данные p
    """
    x, counts = np.unique(sample, return_counts=True)
    cusum = np.cumsum(counts)
    return x, cusum / cusum[-1]

def plot_ecdf(sample):
    """
    Строит cdf
    :param sample: данные p
    """
    x, y = ecdf(sample)
    x = np.insert(x, 0, x[0])
    y = np.insert(y, 0, 0.)
    plt.plot(x, y, drawstyle='steps-post', linewidth = 2)

def plot_all(tests_dict):
    """
    Строит гистаграму и кумулятивную функцию плотности (cdf)
    :param tests_dict = {
        'name_tests': {
            'power': 'float'
            'AB_test': np.array('float')
            'alfa': 'float'
            'AA_test': np.array('float')
        }
    }
    """
    gridsize = (2, 2)
    fig = plt.figure(figsize=(16, 16))

    plt.subplot2grid(gridsize, (0, 0))
    for name_test in tests_dict:
        plot_ecdf(tests_dict[name_test]['AB_test'])
    plt.title('Simulated p-value CDFs under H1')
    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.grid(True)

    plt.subplot2grid(gridsize, (0, 1))
    for name_test in tests_dict:
        plot_ecdf(tests_dict[name_test]['AA_test'])
    plt.title('Simulated p-value CDFs under H0')
    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.grid(True)
    
    #plt.subplot2grid(gridsize, (6, 7), colspan=4, rowspan=4)
    #for name_test in tests_dict:
    #    plt.hist(tests_dict[name_test]['AB_test'], bins=70, alpha=0.4)
    #plt.title('histogram')
    #plt.grid(True)

    plt.subplot2grid(gridsize, (1, 0), colspan=2)
    index = 0
    power = []
    for name_test in tests_dict:
        index += 1
        plt.barh([index], [tests_dict[name_test]['power']], alpha=0.4)
    index = np.arange(index)
    plt.yticks(index + 1, tests_dict.keys())
    plt.title('Test power')
    plt.xlim([-0.05, 1.05])
    plt.ylim([0, index[-1] + 2])
    plt.grid(True)

    st.pyplot(fig)




st.title("Этот титул")
st.write(
    """
    # Это заголовок
    Это текст
    """
)
st.write("""# Выберите параметры""")

#std_coef = st.slider("std_coef", 0.001, 0.01, step=0.00225, format='%f')
std_coef = st.slider("std_coef", 0.001, 0.0055, step=0.00225, format='%f')
zones_corr = st.slider("zones_corr", 0.1, 0.8, step=0.175, format='%f')
effect_size = st.slider("effect_size", 0.002, 0.006, step=0.001, format='%f')


checkbox_ttest = st.checkbox('ttest', value = True)
checkbox_mannwhitneyu = st.checkbox('mannwhitneyu', value = False)
st.write("""# Выберите тесты для отображения""")

stat_test = []
if checkbox_ttest:
    stat_test.append('ttest')
if checkbox_mannwhitneyu:
    stat_test.append('mannwhitneyu')

if checkbox_ttest + checkbox_mannwhitneyu:
    tests_dict={}
    for name_test in stat_test:
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
    
    plot_all(tests_dict=tests_dict)




