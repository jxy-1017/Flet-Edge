import configparser
import xlrd
from matplotlib import pyplot as plt


def dt_single_plot(dt_scalability_ini_path, section_name):
    dt_color_list = [['#ff6600', '#433e7c'], ['#fcd300', '#765005'], ['#c82d31', '#3682be'],
                     ['#ffa510', '#0780cf'], ['#0c84c6', '#002c53']]
    config_read_cpu_gpu_ini = configparser.RawConfigParser()
    config_read_cpu_gpu_ini.optionxform = lambda option: option
    config_read_cpu_gpu_ini.read(dt_scalability_ini_path)
    training_model_name_all = config_read_cpu_gpu_ini.get(section_name, "training_model_name")

    is_nano = config_read_cpu_gpu_ini.getboolean(section_name, "is_nano")
    is_nano_speed_up = config_read_cpu_gpu_ini.getboolean(section_name, "is_nano_speed_up")
    is_nano_acc_up = config_read_cpu_gpu_ini.getboolean(section_name, "is_nano_acc_up")
    is_nano_val_up = config_read_cpu_gpu_ini.getboolean(section_name, "is_nano_val_up")

    training_model_name_all_list = training_model_name_all.split(" ")

    len_training_model_name_all_list = len(training_model_name_all_list)

    fig, ax = plt.subplots()

    plt.xlabel("Host Number")
    plt.ylabel("Speedup/Acc-up/Val-Acc-imp")
    ax.grid(which='both', alpha=0.3, linewidth=0.7)
    sheet_model = None
    for i in range(len_training_model_name_all_list):
        model_name_i = training_model_name_all_list[i]
        if is_nano:
            color_i = dt_color_list[i][1]
            xls_path_nano = config_read_cpu_gpu_ini.get(section_name, "xls_path_nano")

            book_wind = xlrd.open_workbook(filename=xls_path_nano)
            if model_name_i == 'shufflenet05':
                sheet_model = book_wind.sheets()[0]  # [0]代表sheet1，依次类推。
            if model_name_i == 'mobilenetv2':
                sheet_model = book_wind.sheets()[1]
            if model_name_i == 'resnet50':
                sheet_model = book_wind.sheets()[2]
            if model_name_i == 'resnet34':
                sheet_model = book_wind.sheets()[3]
            if model_name_i == 'vgg19':
                sheet_model = book_wind.sheets()[4]

            sheet_model_host_number = sheet_model.col_values(0, 1)
            sheet_model_host_number = [i for i in sheet_model_host_number if i != '']
            if is_nano_speed_up:
                sheet_model_host_speed_up = sheet_model.col_values(1, 1)
                sheet_model_host_speed_up = [i for i in sheet_model_host_speed_up if i != '']
                plt.plot(sheet_model_host_number, sheet_model_host_speed_up,
                         label='%s_speed_up_nano-%s' % (model_name_i, section_name), c='%s' % color_i, linestyle='-')
            if is_nano_acc_up:
                sheet_model_host_acc_up = sheet_model.col_values(2, 1)
                sheet_model_host_acc_up = [i for i in sheet_model_host_acc_up if i != '']
                plt.plot(sheet_model_host_number, sheet_model_host_acc_up,
                         label='%s_acc_up_nano-%s' % (model_name_i, section_name), c='%s' % color_i, linestyle='--')
            if is_nano_val_up:
                sheet_model_host_val_up = sheet_model.col_values(3, 1)
                sheet_model_host_val_up = [i for i in sheet_model_host_val_up if i != '']
                plt.plot(sheet_model_host_number, sheet_model_host_val_up,
                         label='%s_val_acc_up_nano-%s' % (model_name_i, section_name), c='%s' % color_i, linestyle='-.')

    fig.legend(bbox_to_anchor=(0.145, 0.1), loc=2, borderaxespad=4)
    fig.savefig(fname="dt_scalability_%s.png" % section_name, format="png", bbox_inches='tight')
    fig.show()

    return None


def plot_multiple_section(dt_scalability_ini_path, multiple_sections_list):
    len_multiple_sections_list = len(multiple_sections_list)
    for i in range(len_multiple_sections_list):
        section_name = multiple_sections_list[i]
        dt_single_plot(dt_scalability_ini_path, section_name)

    return None


def str_to_list(multiple_sections_list_str):
    multiple_sections_list = multiple_sections_list_str.split("+")
    return multiple_sections_list


if __name__ == '__main__':
    dt_scalability_ini_path = 'dt_plot_config.ini'
    multiple_sections_list = ["plot_dt_01"]
    plot_multiple_section(dt_scalability_ini_path, multiple_sections_list)
