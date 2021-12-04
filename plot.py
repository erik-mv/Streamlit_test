import matplotlib.pyplot as plt
import numpy as np


def plot_ecdf_dict(tests_dict, test_v='AB', plot_legend=False):
    fig = plt.figure(figsize=(6, 6))
    for name_test in tests_dict:
        x =  tests_dict[name_test][test_v + '_cdf_x']
        y =  tests_dict[name_test][test_v + '_cdf_y']
        plt.plot(x, y, drawstyle='steps-post', linewidth = 2, label=name_test)
    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.grid(True)
    if plot_legend:
        plt.legend(loc='lower right', fontsize=18)
    return fig

def plot_power_dict(tests_dict):
    fig = plt.figure(figsize=(6, 3))
    index = 0
    for name_test in tests_dict:
        index += 1
        plt.barh([-index], [tests_dict[name_test]['power']], alpha=0.4)
    index = np.arange(index)
    #plt.yticks(index + 1, tests_dict.keys(), fontsize=18)
    plt.xlim([-0.05, 1.05])
    plt.ylim([-index[-1] - 1.8, -0.2])
    plt.yticks([])
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