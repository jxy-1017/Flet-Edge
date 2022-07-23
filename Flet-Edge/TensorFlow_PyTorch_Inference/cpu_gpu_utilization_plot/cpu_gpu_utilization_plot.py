import linecache
import sys
from matplotlib import pyplot as plt
import xlrd
import configparser
from matplotlib.ticker import MultipleLocator, AutoLocator, FixedLocator, FormatStrFormatter


def plot_single_cpu_gpu(cpu_gpu_ini_path, section_name, is_plot_cpu, is_plot_gpu, color_list_i):
    color_i_cpu = color_list_i[0]
    color_i_gpu = color_list_i[1]

    config_read_cpu_gpu_ini = configparser.RawConfigParser()
    config_read_cpu_gpu_ini.optionxform = lambda option: option
    config_read_cpu_gpu_ini.read(cpu_gpu_ini_path)

    framework = config_read_cpu_gpu_ini.get(section_name, "framework")
    model_name = config_read_cpu_gpu_ini.get(section_name, "model_name")
    device_name = config_read_cpu_gpu_ini.get(section_name, "device_name")
    input_size = config_read_cpu_gpu_ini.getint(section_name, "input_size")
    batchsize_throughput = config_read_cpu_gpu_ini.get(section_name, "batchsize_throughput")
    cpu_gpu_xls_path = config_read_cpu_gpu_ini.get(section_name, "xls_path")

    book_wind = xlrd.open_workbook(filename=cpu_gpu_xls_path)
    sheet1_model = book_wind.sheets()[0]

    if is_plot_gpu and is_plot_gpu:
        plt.title('TF-Py-CPU/GPU Utilization-%s' % model_name, fontsize=16)
    elif is_plot_cpu:
        plt.title('TF-Py-CPU Utilization-%s' % model_name, fontsize=16)
    elif is_plot_gpu:
        plt.title('TF-Py-GPU Utilization-%s' % model_name, fontsize=16)
    else:
        print("The flag whether to draw cpu/gpu diagram is not set correctly.")

    plt.xlabel("Time(500ms per unit)")
    plt.ylabel("Utilization(%)")

    sheet1_model_time = sheet1_model.col_values(0, 1)
    sheet1_model_gpu = sheet1_model.col_values(1, 1)
    sheet1_model_cpu = sheet1_model.col_values(6, 1)

    sheet1_model_time = [i for i in sheet1_model_time if i != '']
    sheet1_model_gpu = [i for i in sheet1_model_gpu if i != '']
    sheet1_model_cpu = [i for i in sheet1_model_cpu if i != '']

    if is_plot_cpu and is_plot_gpu:
        plt.plot(sheet1_model_time, sheet1_model_cpu, label='%s-CPU Utilization-%s' % (framework, section_name),
                 c='%s' % color_i_cpu)
        plt.plot(sheet1_model_time, sheet1_model_gpu, label='%s-GPU Utilization-%s' % (framework, section_name),
                 c='%s' % color_i_gpu)
    elif is_plot_cpu:
        plt.plot(sheet1_model_time, sheet1_model_cpu, label='%s-CPU Utilization-%s' % (framework, section_name),
                 c='%s' % color_i_cpu)
    elif is_plot_gpu:
        plt.plot(sheet1_model_time, sheet1_model_gpu, label='%s-GPU Utilization-%s' % (framework, section_name),
                 c='%s' % color_i_gpu)
    else:
        print("The flag whether to draw cpu/gpu diagram is not set correctly.")

    plt.legend(bbox_to_anchor=(-0.112, 0), loc=2, borderaxespad=4)

    return None


def plot_combine_section_of_CPU_GPU(cpu_gpu_ini_path, three_level_nested_list):
    cpu_gpu_color_list = [['#ff6600', '#433e7c'], ['#fcd300', '#765005'], ['#c82d31', '#3682be'],
                          ['#ffa510', '#0780cf'], ['#0c84c6', '#002c53']]

    len_three_level_nested_list_out = len(three_level_nested_list)

    for i in range(len_three_level_nested_list_out):

        len_three_level_nested_list_mid = len(three_level_nested_list[i])

        plt_i_name = three_level_nested_list[i][0]

        width = 25
        height = 6
        fig_i, ax = plt.subplots(figsize=(width, height))
        ax.grid(which='both', alpha=0.3, linewidth=0.7)
        y_major = MultipleLocator(10)
        y_minor = MultipleLocator(2)
        ax.yaxis.set_major_locator(y_major)
        ax.yaxis.set_minor_locator(y_minor)
        ax.tick_params(axis="y", direction="out", which="major", labelsize=15, length=5)
        ax.tick_params(axis="y", direction="out", which="minor", length=4)

        ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f%%'))
        section_name_in = None
        section_name_is_cpu = None
        section_name_is_gpu = None
        for j in range(len_three_level_nested_list_mid):

            if j == 0:
                pass
            else:
                section_name_in = three_level_nested_list[i][j][0]
                section_name_is_cpu = three_level_nested_list[i][j][1]
                section_name_is_gpu = three_level_nested_list[i][j][2]

                color_list_i = cpu_gpu_color_list[j]

                plot_single_cpu_gpu(cpu_gpu_ini_path, section_name_in, section_name_is_cpu, section_name_is_gpu,
                                    color_list_i)
        fig_i.show()

        fig_i_name = three_level_nested_list[i][0][0]
        fig_i.savefig(fname="TF_Py_%s_cpu_gpu_utilization.png" % fig_i_name, format="png", bbox_inches='tight')

    return None


def read_cpu_gpu_utilization_plot_list_name_line_to_list(cpu_gpu_utilization_plot_list_line_str):
    cpu_gpu_utilization_plot_list_line = int(cpu_gpu_utilization_plot_list_line_str)
    cpu_gpu_utilization_plot_list_str = linecache.getline("./cpu_gpu_utilization_to_plot_list.txt",
                                                          cpu_gpu_utilization_plot_list_line)
    cpu_gpu_utilization_plot_list = eval(cpu_gpu_utilization_plot_list_str)

    return cpu_gpu_utilization_plot_list


if __name__ == '__main__':
    FET_section_name = sys.argv[1]
    cpu_gpu_ini_path = "./%s/%s_cpu_gpu_utilization.ini" % (FET_section_name, FET_section_name)

    cpu_gpu_utilization_plot_list_line_str = sys.argv[2]

    cpu_gpu_utilization_plot_list = read_cpu_gpu_utilization_plot_list_name_line_to_list(
        cpu_gpu_utilization_plot_list_line_str)

    plot_combine_section_of_CPU_GPU(cpu_gpu_ini_path, cpu_gpu_utilization_plot_list)
