import configparser
import os
import subprocess
import sys
import xlrd
import xlwt
from xlutils.copy import copy


def generate_dt_single_experiment_xls(dt_xls_name):
    workbook = xlwt.Workbook(encoding='utf-8')

    shufflenet05 = workbook.add_sheet('shufflenet05', cell_overwrite_ok=True)
    mobilenetv2 = workbook.add_sheet('mobilenetv2', cell_overwrite_ok=True)
    resnet50 = workbook.add_sheet('resnet50', cell_overwrite_ok=True)
    resnet34 = workbook.add_sheet('resnet34', cell_overwrite_ok=True)
    vgg19 = workbook.add_sheet('vgg19', cell_overwrite_ok=True)

    shufflenet05.write(0, 0, 'host_number')
    shufflenet05.write(0, 1, 'speedup')
    shufflenet05.write(0, 2, 'acc_imp')
    shufflenet05.write(0, 3, 'val_acc_imp')
    shufflenet05.write(0, 4, 'time_spend')
    shufflenet05.write(0, 5, 'acc')
    shufflenet05.write(0, 6, 'val_acc')

    mobilenetv2.write(0, 0, 'host_number')
    mobilenetv2.write(0, 1, 'speedup')
    mobilenetv2.write(0, 2, 'acc_imp')
    mobilenetv2.write(0, 3, 'val_acc_imp')
    mobilenetv2.write(0, 4, 'time_spend')
    mobilenetv2.write(0, 5, 'acc')
    mobilenetv2.write(0, 6, 'val_acc')

    resnet50.write(0, 0, 'host_number')
    resnet50.write(0, 1, 'speedup')
    resnet50.write(0, 2, 'acc_imp')
    resnet50.write(0, 3, 'val_acc_imp')
    resnet50.write(0, 4, 'time_spend')
    resnet50.write(0, 5, 'acc')
    resnet50.write(0, 6, 'val_acc')

    resnet34.write(0, 0, 'host_number')
    resnet34.write(0, 1, 'speedup')
    resnet34.write(0, 2, 'acc_imp')
    resnet34.write(0, 3, 'val_acc_imp')
    resnet34.write(0, 4, 'time_spend')
    resnet34.write(0, 5, 'acc')
    resnet34.write(0, 6, 'val_acc')

    vgg19.write(0, 0, 'host_number')
    vgg19.write(0, 1, 'speedup')
    vgg19.write(0, 2, 'acc_imp')
    vgg19.write(0, 3, 'val_acc_imp')
    vgg19.write(0, 4, 'time_spend')
    vgg19.write(0, 5, 'acc')
    vgg19.write(0, 6, 'val_acc')
    workbook.save('./%s.xls' % dt_xls_name)


def read_experiments_xls_path(experiments_i_path):
    global experiments_xls_path
    file_exist = ['.xls']
    print(experiments_i_path)
    experiments_i_path = "/home/jiang/nano3/FET_dt_experiment01/"
    for path in os.listdir(experiments_i_path):
        experiments_xls_path = os.path.join(experiments_i_path, path)
        if os.path.isfile(experiments_xls_path):
            if (os.path.splitext(experiments_xls_path)[1]) in file_exist:
                print(experiments_xls_path)

    return experiments_xls_path


def write_all_to_excel(experiment_i_path, excel_name, experiments_dt_number_list_i):
    book_wind = xlrd.open_workbook(filename=experiment_i_path)
    shufflenet05_sheet = book_wind.sheets()[0]
    mobilenetv2_sheet = book_wind.sheets()[1]
    resnet50_sheet = book_wind.sheets()[2]
    resnet34_sheet = book_wind.sheets()[3]
    vgg19_sheet = book_wind.sheets()[4]

    shufflenet05_sheet_time_spend = shufflenet05_sheet.cell_value(1, 4)
    shufflenet05_sheet_acc = shufflenet05_sheet.cell_value(1, 5)
    shufflenet05_sheet_val_acc = shufflenet05_sheet.cell_value(1, 6)
    shufflenet05_sheet_time_spend = float(shufflenet05_sheet_time_spend)
    shufflenet05_sheet_acc = float(shufflenet05_sheet_acc)
    shufflenet05_sheet_val_acc = float(shufflenet05_sheet_val_acc)

    mobilenetv2_sheet_time_spend = mobilenetv2_sheet.cell_value(1, 4)
    mobilenetv2_sheet_acc = mobilenetv2_sheet.cell_value(1, 5)
    mobilenetv2_sheet_val_acc = mobilenetv2_sheet.cell_value(1, 6)
    mobilenetv2_sheet_time_spend = float(mobilenetv2_sheet_time_spend)
    mobilenetv2_sheet_acc = float(mobilenetv2_sheet_acc)
    mobilenetv2_sheet_val_acc = float(mobilenetv2_sheet_val_acc)

    resnet50_sheet_time_spend = resnet50_sheet.cell_value(1, 4)
    resnet50_sheet_acc = resnet50_sheet.cell_value(1, 5)
    resnet50_sheet_val_acc = resnet50_sheet.cell_value(1, 6)
    resnet50_sheet_time_spend = float(resnet50_sheet_time_spend)
    resnet50_sheet_acc = float(resnet50_sheet_acc)
    resnet50_sheet_val_acc = float(resnet50_sheet_val_acc)

    resnet34_sheet_time_spend = resnet34_sheet.cell_value(1, 4)
    resnet34_sheet_acc = resnet34_sheet.cell_value(1, 5)
    resnet34_sheet_val_acc = resnet34_sheet.cell_value(1, 6)
    resnet34_sheet_time_spend = float(resnet34_sheet_time_spend)
    resnet34_sheet_acc = float(resnet34_sheet_acc)
    resnet34_sheet_val_acc = float(resnet34_sheet_val_acc)

    vgg19_sheet_time_spend = vgg19_sheet.cell_value(1, 4)
    vgg19_sheet_acc = vgg19_sheet.cell_value(1, 5)
    vgg19_sheet_val_acc = vgg19_sheet.cell_value(1, 6)
    vgg19_sheet_time_spend = float(vgg19_sheet_time_spend)
    vgg19_sheet_acc = float(vgg19_sheet_acc)
    vgg19_sheet_val_acc = float(vgg19_sheet_val_acc)

    global shufflenet05_time_spend_benchmark
    global shufflenet05_acc_benchmark
    global shufflenet05_val_acc_benchmark

    global mobilenetv2_time_spend_benchmark
    global mobilenetv2_acc_benchmark
    global mobilenetv2_val_acc_benchmark

    global resnet50_time_spend_benchmark
    global resnet50_acc_benchmark
    global resnet50_val_acc_benchmark

    global resnet34_time_spend_benchmark
    global resnet34_acc_benchmark
    global resnet34_val_acc_benchmark

    global vgg19_time_spend_benchmark
    global vgg19_acc_benchmark
    global vgg19_val_acc_benchmark

    if int(experiments_dt_number_list_i) == 1:
        shufflenet05_time_spend_benchmark = shufflenet05_sheet_time_spend
        shufflenet05_acc_benchmark = shufflenet05_sheet_acc
        shufflenet05_val_acc_benchmark = shufflenet05_sheet_val_acc
        mobilenetv2_time_spend_benchmark = mobilenetv2_sheet_time_spend
        mobilenetv2_acc_benchmark = mobilenetv2_sheet_acc
        mobilenetv2_val_acc_benchmark = mobilenetv2_sheet_val_acc
        resnet50_time_spend_benchmark = resnet50_sheet_time_spend
        resnet50_acc_benchmark = resnet50_sheet_acc
        resnet50_val_acc_benchmark = resnet50_sheet_val_acc
        resnet34_time_spend_benchmark = resnet34_sheet_time_spend
        resnet34_acc_benchmark = resnet34_sheet_acc
        resnet34_val_acc_benchmark = resnet34_sheet_val_acc
        vgg19_time_spend_benchmark = vgg19_sheet_time_spend
        vgg19_acc_benchmark = vgg19_sheet_acc
        vgg19_val_acc_benchmark = vgg19_sheet_val_acc

    table = xlrd.open_workbook("./%s.xls" % excel_name)
    table_copy = copy(table)
    sheet_shufflenet05 = table_copy.get_sheet(0)
    sheet_mobilenetv2 = table_copy.get_sheet(1)
    sheet_resnet50 = table_copy.get_sheet(2)
    sheet_resnet34 = table_copy.get_sheet(3)
    sheet_vgg19 = table_copy.get_sheet(4)
    sheet_shufflenet05.write(int(experiments_dt_number_list_i), 0, label=experiments_dt_number_list_i)
    sheet_shufflenet05.write(int(experiments_dt_number_list_i), 4, label=shufflenet05_sheet_time_spend)
    sheet_shufflenet05.write(int(experiments_dt_number_list_i), 5, label=shufflenet05_sheet_acc)
    sheet_shufflenet05.write(int(experiments_dt_number_list_i), 6, label=shufflenet05_sheet_val_acc)
    sheet_shufflenet05.write(int(experiments_dt_number_list_i), 1,
                             label=(shufflenet05_sheet_time_spend / shufflenet05_time_spend_benchmark))
    sheet_shufflenet05.write(int(experiments_dt_number_list_i), 2,
                             label=(shufflenet05_sheet_acc / shufflenet05_acc_benchmark))
    sheet_shufflenet05.write(int(experiments_dt_number_list_i), 3,
                             label=(shufflenet05_sheet_val_acc / shufflenet05_val_acc_benchmark))

    sheet_mobilenetv2.write(int(experiments_dt_number_list_i), 0, label=int(experiments_dt_number_list_i))
    sheet_mobilenetv2.write(int(experiments_dt_number_list_i), 4, label=mobilenetv2_sheet_time_spend)
    sheet_mobilenetv2.write(int(experiments_dt_number_list_i), 5, label=mobilenetv2_sheet_acc)
    sheet_mobilenetv2.write(int(experiments_dt_number_list_i), 6, label=mobilenetv2_sheet_val_acc)
    sheet_mobilenetv2.write(int(experiments_dt_number_list_i), 1,
                            label=(mobilenetv2_sheet_time_spend / mobilenetv2_time_spend_benchmark))
    sheet_mobilenetv2.write(int(experiments_dt_number_list_i), 2,
                            label=(mobilenetv2_sheet_acc / mobilenetv2_acc_benchmark))
    sheet_mobilenetv2.write(int(experiments_dt_number_list_i), 3,
                            label=(mobilenetv2_sheet_val_acc / mobilenetv2_val_acc_benchmark))

    sheet_resnet50.write(int(experiments_dt_number_list_i), 0, label=int(experiments_dt_number_list_i))
    sheet_resnet50.write(int(experiments_dt_number_list_i), 4, label=resnet50_sheet_time_spend)
    sheet_resnet50.write(int(experiments_dt_number_list_i), 5, label=resnet50_sheet_acc)
    sheet_resnet50.write(int(experiments_dt_number_list_i), 6, label=resnet50_sheet_val_acc)
    sheet_resnet50.write(int(experiments_dt_number_list_i), 1,
                         label=(resnet50_sheet_time_spend / resnet50_time_spend_benchmark))
    sheet_resnet50.write(int(experiments_dt_number_list_i), 2, label=(resnet50_sheet_acc / resnet50_acc_benchmark))
    sheet_resnet50.write(int(experiments_dt_number_list_i), 3,
                         label=(resnet50_sheet_val_acc / resnet50_val_acc_benchmark))

    sheet_resnet34.write(int(experiments_dt_number_list_i), 0, label=int(experiments_dt_number_list_i))
    sheet_resnet34.write(int(experiments_dt_number_list_i), 4, label=resnet34_sheet_time_spend)
    sheet_resnet34.write(int(experiments_dt_number_list_i), 5, label=resnet34_sheet_acc)
    sheet_resnet34.write(int(experiments_dt_number_list_i), 6, label=resnet34_sheet_val_acc)
    sheet_resnet34.write(int(experiments_dt_number_list_i), 1,
                         label=(resnet34_sheet_time_spend / resnet34_time_spend_benchmark))
    sheet_resnet34.write(int(experiments_dt_number_list_i), 2, label=(resnet34_sheet_acc / resnet34_acc_benchmark))
    sheet_resnet34.write(int(experiments_dt_number_list_i), 3,
                         label=(resnet34_sheet_val_acc / resnet34_val_acc_benchmark))

    sheet_vgg19.write(int(experiments_dt_number_list_i), 0, label=int(experiments_dt_number_list_i))
    sheet_vgg19.write(int(experiments_dt_number_list_i), 4, label=vgg19_sheet_time_spend)
    sheet_vgg19.write(int(experiments_dt_number_list_i), 5, label=vgg19_sheet_acc)
    sheet_vgg19.write(int(experiments_dt_number_list_i), 6, label=vgg19_sheet_val_acc)
    sheet_vgg19.write(int(experiments_dt_number_list_i), 1, label=(vgg19_sheet_time_spend / vgg19_time_spend_benchmark))
    sheet_vgg19.write(int(experiments_dt_number_list_i), 2, label=(vgg19_sheet_acc / vgg19_acc_benchmark))
    sheet_vgg19.write(int(experiments_dt_number_list_i), 3, label=(vgg19_sheet_val_acc / vgg19_val_acc_benchmark))

    table_copy.save("./%s.xls" % excel_name)

    return None


def generate_summary_table_and_write(dt_plot_config_path, plot_section, host_name):
    config_plot_dt = configparser.ConfigParser()
    per_section_name_ini_path = dt_plot_config_path
    config_plot_dt.read(per_section_name_ini_path)
    experiments_name = config_plot_dt.get(plot_section, 'experiments_name')
    experiments_dt_number = config_plot_dt.get(plot_section, 'dt_device_number')
    experiments_name_list = experiments_name.split(" ")
    experiments_dt_number_list = experiments_dt_number.split(" ")
    len_experiments_name_list = len(experiments_name_list)
    excel_name = ""
    for i in range(len_experiments_name_list):
        experiments_name_list_i = experiments_name_list[i]
        excel_name = excel_name + experiments_name_list_i + "_"

    generate_dt_single_experiment_xls(excel_name)

    for i in range(len_experiments_name_list):
        experiments_name_list_i = experiments_name_list[i]
        experiments_dt_number_list_i = experiments_dt_number_list[i]

        experiments_i_path = "~/" + host_name + "/" + experiments_name_list_i + "/"

        print("experiment_i_path: ", experiments_i_path)
        experiment_i_path = read_experiments_xls_path(experiments_i_path)

        write_all_to_excel(experiment_i_path, excel_name, experiments_dt_number_list_i)

    return None


def popen_dt_scalability_plot(dt_plot_config_path, multiple_sections_list):
    multiple_sections_list_str = "+".join(multiple_sections_list)
    popen_out_of_dt_scalability_plot = popen("python3 dt_scalability_plot.py %s %s" %
                                             (dt_plot_config_path, multiple_sections_list_str))
    with open('out_of_popen_%s.txt' % (multiple_sections_list_str), 'a') as f:
        f.write(popen_out_of_dt_scalability_plot)

    return None


def popen(cmd):
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         universal_newlines=True, executable="/bin/bash")
    out, err = p.communicate()
    return out + err


def str_to_list(multiple_sections_list_str):
    multiple_sections_list = multiple_sections_list_str.split("+")
    return multiple_sections_list


if __name__ == '__main__':

    dt_plot_config_path = sys.argv[1]
    multiple_sections_list_str = sys.argv[2]
    host_name = sys.argv[3]
    multiple_sections_list = str_to_list(multiple_sections_list_str)

    len_multiple_sections_list = len(multiple_sections_list)
    for i in range(len_multiple_sections_list):
        plot_section_i = multiple_sections_list[i]
        generate_summary_table_and_write(dt_plot_config_path, plot_section_i, host_name)

    popen_dt_scalability_plot(dt_plot_config_path, multiple_sections_list)
