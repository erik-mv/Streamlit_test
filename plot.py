import matplotlib.pyplot as plt
import numpy as np

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

def plot_ecdf_dict(tests_dict, test_v='AB_test'):
    fig = plt.figure(figsize=(6, 6))
    for name_test in tests_dict:
        plot_ecdf(tests_dict[name_test][test_v])
    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.grid(True)
    return fig

def plot_power_dict(tests_dict):
    fig = plt.figure(figsize=(6, 3))
    index = 0
    for name_test in tests_dict:
        index += 1
        plt.barh([index], [tests_dict[name_test]['power']], alpha=0.4)
    index = np.arange(index)
    plt.yticks(index + 1, tests_dict.keys(), fontsize=18)
    plt.xlim([-0.05, 1.05])
    plt.ylim([0, index[-1] + 2])
    plt.grid(True)
    return fig

def plot_hist(control, test):
    fig = plt.figure(figsize=(6, 6))
    plt.hist(control, bins=70, alpha=0.4, facecolor='b', label='Control')
    plt.hist(test, bins=70, alpha=0.4, facecolor='r', label='Test')
    plt.legend(fontsize=18)
    plt.grid(True)
    
    return fig