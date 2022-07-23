import configparser
import sys
import matplotlib.pyplot as plt
import numpy as np


def plot_nano_hierarchical_roofline(roofline_data_path, ax):
    config_read_roofline_data = configparser.RawConfigParser()
    config_read_roofline_data.optionxform = lambda option: option
    config_read_roofline_data.read(roofline_data_path)

    gflops_nano_peak = config_read_roofline_data.getfloat("gflops_bandwidth_nano", "gflops")
    l1_nano_peak = config_read_roofline_data.getfloat("gflops_bandwidth_nano", "l1")
    l2_nano_peak = config_read_roofline_data.getfloat("gflops_bandwidth_nano", "l2")
    dram_nano_peak = config_read_roofline_data.getfloat("gflops_bandwidth_nano", "dram")

    A1, B1 = l1_nano_peak, 0
    A2, B2 = l2_nano_peak, 0
    A3, B3 = dram_nano_peak, 0
    A4, B4 = 0, gflops_nano_peak

    t1 = np.arange(0.1, 1000, 0.1)
    y_list1 = []
    t2 = np.arange(0.1, B4 / A2, 0.1)
    y_list2 = []
    t3 = np.arange(0.1, B4 / A3, 0.1)
    y_list3 = []

    def y1(t):
        for i in t:
            if i <= B4 / A1:
                y_list1.append(A1 * i + B1)
            else:
                y_list1.append(0 * i + B4)

    def y2(t):
        for i in t:
            if i <= B4 / A2:
                y_list2.append(A2 * i + B2)
            else:
                y_list2.append(0 * i + B4)

    def y3(t):
        for i in t:
            if i <= B4 / A3:
                y_list3.append(A3 * i + B3)
            else:
                y_list3.append(0 * i + B4)

    y1(t1)
    y2(t2)
    y3(t3)

    ax.set_xscale('log')
    ax.set_yscale('log')

    plt.xlabel("FLOPs/Byte")
    plt.ylabel("GFLOPs/sec")

    ax.grid(which='both', alpha=0.3, linewidth=0.7)

    plt.plot(t3, y_list3, label='DRAM - %s GB/s' % dram_nano_peak, c='#0c84c6')
    plt.plot(t2, y_list2, label='L2 - %s GB/s' % l2_nano_peak, c='#ffa510')
    plt.plot(t1, y_list1, label='l1 - %s GB / s' % l1_nano_peak, c='#002c53')

    plt.legend()

    plt.xlim(0.1, 1000)
    plt.ylim(1, 1000)

    return None


def plot_single_model_xy(roofline_data_path, section_name, l1_c, l2_c, l1_marker, l2_marker):
    config_read_roofline_data = configparser.RawConfigParser()
    config_read_roofline_data.optionxform = lambda option: option
    config_read_roofline_data.read(roofline_data_path)

    plt.title("Hierarchical Roofline Graph of %s on Jetson Nano" % "tensorflow")

    model_name = config_read_roofline_data.get(section_name, "model_name")
    device_name = config_read_roofline_data.get(section_name, "device_name")
    input_size = config_read_roofline_data.getint(section_name, "input_size")

    gflops = config_read_roofline_data.getfloat(section_name, "gflops")
    l1 = config_read_roofline_data.getfloat(section_name, "l1")
    l2 = config_read_roofline_data.getfloat(section_name, "l2")
    flops = config_read_roofline_data.getfloat(section_name, "flops")

    l1_x = np.array([flops / l1])
    l1_y = np.array([gflops])
    l2_x = np.array([flops / l2])
    l2_y = np.array([gflops])
    plt.scatter(l1_x, l1_y, s=30, c='%s' % l1_c, alpha=1, marker='%s' % l1_marker, label='%s-l1' % section_name)
    plt.scatter(l2_x, l2_y, s=30, c='%s' % l2_c, alpha=1, marker='%s' % l2_marker, label='%s-l2' % section_name)
    plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0)

    return None


def plot_all_xy(roofline_data_path, plot_section_list):
    l1_c_list = ['#c82d31', '#c82d31', '#c82d31', '#c82d31', '#c82d31']
    l2_c_list = ['#3682be', '#3682be', '#3682be', '#3682be', '#3682be']
    l1_marker_list = ['o', '^', 's', 'p', 'h']
    l2_marker_list = ['o', '^', 's', 'p', 'h']

    len_plot_section_list = len(plot_section_list)
    for i in range(len_plot_section_list):
        l1_c = l1_c_list[i]
        l2_c = l2_c_list[i]
        l1_marker = l1_marker_list[i]
        l2_marker = l2_marker_list[i]

        section_name_i = plot_section_list[i]
        plot_single_model_xy(roofline_data_path, section_name_i, l1_c, l2_c, l1_marker, l2_marker)
    return None


def str_to_list(plot_combine_bar_list_str):
    plot_combine_bar_list = plot_combine_bar_list_str.split("+")
    return plot_combine_bar_list


if __name__ == '__main__':
    fig, ax = plt.subplots()

    roofline_data_path = sys.argv[1]
    plot_combine_section_list_str = sys.argv[2]

    plot_combine_section_list = str_to_list(plot_combine_section_list_str)
    combine_section_name = sys.argv[3]

    plot_nano_hierarchical_roofline(roofline_data_path, ax)

    section_name = "shufflenet05_cuda_16_16"

    plot_all_xy(roofline_data_path, plot_combine_section_list)

    plt.savefig(fname="roofline-pytorch-done.png", format="png", bbox_inches='tight')
    plt.show()
