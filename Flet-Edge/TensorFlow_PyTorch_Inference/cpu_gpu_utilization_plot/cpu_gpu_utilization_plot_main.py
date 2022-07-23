import configparser
import subprocess
import sys
import xlrd
import xlwt
from xlutils.copy import copy


def popen(cmd):
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         universal_newlines=True, executable="/bin/bash")
    out, err = p.communicate()
    return out + err


def cp_sub_config_and_process_for_cpu_gpu_utilization(FET_section_name):
    if os.path.exists("./%s/cpu_gpu_utilization_out" % FET_section_name):
        print("./%s/cpu_gpu_utilization_out exists." % FET_section_name)
    else:
        os.makedirs("./%s/cpu_gpu_utilization_out" % FET_section_name)

    cp_sub_config_and_process_for_cpu_gpu_utilization = popen(
        "cp -r ../%s/%s_all_section.ini ./%s/%s_cpu_gpu_utilization.ini" %
        (FET_section_name, FET_section_name, FET_section_name, FET_section_name))
    with open('./%s/cpu_gpu_utilization_out/cp_sub_for_cpu_gpu_utilization_of_FET_section_name.txt' % FET_section_name,
              'a') as f:
        f.write(cp_sub_config_and_process_for_cpu_gpu_utilization)
    print("cp_sub_config_and_process_for_cpu_gpu_utilization --> %s" % "FET_section_name")

    return None


def get_all_sections(FET_section_name):
    config_read_all_combine_section_cpu_gpu_utilization = configparser.RawConfigParser()
    config_read_all_combine_section_cpu_gpu_utilization.optionxform = lambda option: option
    config_read_all_combine_section_cpu_gpu_utilization.read("./%s/%s_cpu_gpu_utilization.ini" %
                                                             (FET_section_name, FET_section_name))
    cpu_gpu_utilization_ini_all_sections_list = config_read_all_combine_section_cpu_gpu_utilization.sections()

    return cpu_gpu_utilization_ini_all_sections_list


def generate_section_i_xls(section_i):
    workbook = xlwt.Workbook(encoding='utf-8')

    section_i_model = workbook.add_sheet('section_i_model', cell_overwrite_ok=True)

    section_i_model.write(0, 0, 'time')
    section_i_model.write(0, 1, 'gpu')
    section_i_model.write(0, 2, 'c0')
    section_i_model.write(0, 3, 'c1')
    section_i_model.write(0, 4, 'c2')
    section_i_model.write(0, 5, 'c3')
    section_i_model.write(0, 6, 'c_avg')
    workbook.save('%s.xls' % section_i)

    return None


def write_xls_name_to_sub_cg(FET_section_name, section_i):
    config_read_all_combine_section_cpu_gpu_utilization = configparser.RawConfigParser()
    config_read_all_combine_section_cpu_gpu_utilization.optionxform = lambda option: option
    config_read_all_combine_section_cpu_gpu_utilization.read("./%s/%s_cpu_gpu_utilization.ini" %
                                                             (FET_section_name, FET_section_name))
    config_read_all_combine_section_cpu_gpu_utilization.set(section_i, "xls_path", "%s.xls" % section_i)
    config_read_all_combine_section_cpu_gpu_utilization.write(open("./%s/%s_cpu_gpu_utilization.ini" %
                                                                   (FET_section_name, FET_section_name), 'w+'))

    return None


def find_and_write_data_to_excel_cg(FET_section_name, section_i):
    find_path = '../%s/cpu_gpu_utilization' % FET_section_name

    filename1 = "py_pre_data_jtop_gpu_cpu_"
    filename2 = section_i
    for root, dirs, files in os.walk(find_path):
        for file_name in files:
            if filename2 in file_name:
                file_name_filename2 = file_name

                if filename1 in file_name_filename2:

                    gpu_data = []
                    cpu_data = []
                    with open("../%s/cpu_gpu_utilization/%s" % (FET_section_name, file_name_filename2), 'r') as f:
                        lines = f.readlines()
                        for line in lines:
                            gpu_data.append(line.split(" ")[2])
                            c1 = int(line.split(" ")[3])
                            c2 = int(line.split(" ")[4])
                            c3 = int(line.split(" ")[5])
                            c4 = int(line.split(" ")[6])
                            c_avg = float((c1 + c2 + c3 + c4) / 4)
                            cpu_data.append(c_avg)

                    section_i_xls = "./%s.xls" % section_i
                    table = xlrd.open_workbook(section_i_xls)
                    table_copy = copy(table)
                    section_i_sheet = table_copy.get_sheet(0)

                    len_gpu_cpu = len(gpu_data)
                    for i in range(len_gpu_cpu):
                        section_i_sheet.write(i + 1, 0, label=i + 1)
                        section_i_sheet.write(i + 1, 1, label=gpu_data[i])
                        section_i_sheet.write(i + 1, 6, label=cpu_data[i])
                    table_copy.save(section_i_xls)

    return None


def start_cpu_gpu_utilization_plot(FET_section_name, cpu_gpu_utilization_plot_list_line_str):
    popen_start_cpu_gpu_utilization_plot = popen(
        "python3 ./cpu_gpu_utilization_plot.py %s %s" % (FET_section_name, cpu_gpu_utilization_plot_list_line_str))
    with open('./out_of_popen_start_cpu_gpu_utilization_plot.txt_%s_%s' %
              (FET_section_name, cpu_gpu_utilization_plot_list_line_str), 'a') as f:
        f.write(popen_start_cpu_gpu_utilization_plot)

    return None


import os

if __name__ == '__main__':

    FET_section_name = sys.argv[1]

    cp_sub_config_and_process_for_cpu_gpu_utilization(FET_section_name)

    cpu_gpu_utilization_ini_all_sections_list = get_all_sections(FET_section_name)
    len_cpu_gpu_utilization_ini_all_sections_list = len(cpu_gpu_utilization_ini_all_sections_list)

    for i in range(len_cpu_gpu_utilization_ini_all_sections_list):
        section_i = cpu_gpu_utilization_ini_all_sections_list[i]

        generate_section_i_xls(section_i)

        write_xls_name_to_sub_cg(FET_section_name, section_i)

        find_and_write_data_to_excel_cg(FET_section_name, section_i)

    cpu_gpu_utilization_plot_list_line_str = "1"
    start_cpu_gpu_utilization_plot(FET_section_name, cpu_gpu_utilization_plot_list_line_str)
