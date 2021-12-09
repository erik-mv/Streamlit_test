import matplotlib.pyplot as plt
import numpy as np


def plot_ecdf_dict(tests_dict, test_v='AB', plot_legend=False):
    fig = plt.figure(figsize=(6, 6))

    if test_v == 'AA':
        plt.plot([0.0, 1.0], [0.0, 1.0], color='black', linestyle='dashed', linewidth=2, alpha=0.5)
    else:
        plt.plot([0.05, 0.05], [0.0, 1.0], color='black', linestyle='dashed', linewidth=2, alpha=0.5)

    for name_test in tests_dict:
        x =  tests_dict[name_test][test_v + '_cdf_x']
        y =  tests_dict[name_test][test_v + '_cdf_y']
        plt.plot(x, y, drawstyle='steps-post', linewidth = 2, label=name_test)
    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    #plt.ylabel('Истинно положительные чистоты (TPR)', fontsize=14)
    #plt.xlabel('Ложноположительные чистоты (FPR)', fontsize=14)
    plt.grid(True)
    if plot_legend:
        plt.legend(loc='lower right', fontsize=16)
    return fig

def plot_power_dict(tests_dict):
    fig = plt.figure(figsize=(6, 3))
    index = 0
    for name_test in tests_dict:
        index += 1
        power = tests_dict[name_test]['power']
        plt.barh([-index], [power], alpha=0.4)
        plt.text(0.02, -index, '%s: %.3f' % (name_test, power), ha='left', va = 'center', fontsize=14)
    index = np.arange(index)
    #plt.yticks(-index - 1, tests_dict.keys(), fontsize=14)
    plt.yticks([])
    plt.xlim([-0.05, 1.05])
    plt.ylim([-index[-1] - 1.8, -0.2])
    plt.grid(True)
    return fig

def plot_hist(value):
    """
    Строит гистограмму по value
    """
    fig = plt.figure(figsize=(6, 6))
    plt.hist(value, bins=70, alpha=0.4, facecolor='r')
    plt.xlim([-0.05, 1.05])
    plt.ylim([0, 6500])
    plt.grid(True)
    return fig