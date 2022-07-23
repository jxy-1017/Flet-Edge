import configparser
import os
import subprocess
import linecache
import sys


def cp_sub_config_and_process_for_pmu(FET_section_name):
    if os.path.exists("./%s/pmu_out" % FET_section_name):
        print("./%s/pmu_out exists." % FET_section_name)
    else:
        os.makedirs("./%s/pmu_out" % FET_section_name)

    cp_sub_config_and_process_for_pmu = popen("cp -r ../%s/%s_all_section.ini ./%s/%s_pmu.ini" %
                                              (FET_section_name, FET_section_name, FET_section_name, FET_section_name))

    with open('./%s/pmu_out/cp_sub_for_pmu_of_FET_section_name.txt' % FET_section_name, 'a') as f:
        f.write(cp_sub_config_and_process_for_pmu)
    print("cp_sub_config_and_process_for_pmu --> %s" % "FET_section_name")

    return None


def popen(cmd):
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         universal_newlines=True, executable="/bin/bash")
    out, err = p.communicate()
    return out + err


def scientific_to_float(x):
    if "e" in x:
        x = eval(x)
    return x


def store_pmu_value_sub_pmu_section_i(FET_section_name, section_name_i, pmu_value):
    config_store_pmu_data = configparser.RawConfigParser()
    config_store_pmu_data.optionxform = lambda option: option
    pmu_sub_ini_path = "./%s/%s_pmu.ini" % (FET_section_name, FET_section_name)
    config_store_pmu_data.read(pmu_sub_ini_path)
    config_store_pmu_data.set(section_name_i, "pmu", "%s" % pmu_value)

    config_store_pmu_data.write(open(pmu_sub_ini_path, 'w+'))

    return None


def find_and_store_pmu_to_sub(FET_section_name, single_sub_section_list):
    len_single_sub_section_list = len(single_sub_section_list)
    for i in range(len_single_sub_section_list):
        section_name_i = single_sub_section_list[i]
        print(section_name_i)

        find_path = '../%s/pmu/' % FET_section_name
        filename1 = "result"
        filename2 = section_name_i
        for root, dirs, files in os.walk(find_path):
            for file_name in files:
                if filename2 in file_name:
                    file_name_filename2 = file_name

                    if filename1 in file_name_filename2:
                        pmu_value_scientific = linecache.getline(
                            "../%s/pmu/%s" % (FET_section_name, file_name_filename2), 2)

                        pmu_value = scientific_to_float(pmu_value_scientific)

                        store_pmu_value_sub_pmu_section_i(FET_section_name, section_name_i, pmu_value)

    return


def read_combine_section_pmu_plot(combine_section_pmu_plot_path, combine_section_name):
    config_read_combine_section_pmu = configparser.RawConfigParser()
    config_read_combine_section_pmu.optionxform = lambda option: option
    config_read_combine_section_pmu.read(combine_section_pmu_plot_path)
    combine_section_value = config_read_combine_section_pmu.get(combine_section_name, "plot_combine_bar")

    combine_section_value_list = combine_section_value.split(" ")

    return combine_section_value_list


def start_pmu_plot(FET_section_name, combine_section_value_list, combine_section_name):
    pmu_data_path = "./%s/%s_pmu.ini" % (FET_section_name, FET_section_name)

    combine_section_value_list_str = "+".join(combine_section_value_list)
    out_popen_of_pmu_plot = popen(
        "python3 pmu_plot.py %s %s %s" % (pmu_data_path, combine_section_value_list_str, combine_section_name))
    with open("out_popen_of_pmu_plot_%s_%s.txt" % (FET_section_name, combine_section_name), 'a') as f:
        f.write(out_popen_of_pmu_plot)
    print("popen_of_pmu_plot_%s_%s" % (FET_section_name, combine_section_name))

    return None


def plot_all_combine_section_pmu(combine_section_pmu_plot_path):
    config_read_all_combine_section_pmu = configparser.RawConfigParser()
    config_read_all_combine_section_pmu.optionxform = lambda option: option
    config_read_all_combine_section_pmu.read(combine_section_pmu_plot_path)
    all_sections = config_read_all_combine_section_pmu.sections()

    len_all_sections = len(all_sections)
    for i in range(len_all_sections):
        combine_section_name_i = all_sections[i]

        combine_section_value_list = read_combine_section_pmu_plot(combine_section_pmu_plot_path,
                                                                   combine_section_name_i)

        start_pmu_plot(FET_section_name, combine_section_value_list, combine_section_name_i)

    return None


def get_all_section_list(FET_section_name):
    pmu_ini_path = "./%s/%s_pmu.ini" % (FET_section_name, FET_section_name)

    config_read_all_ini_section_pmu = configparser.RawConfigParser()
    config_read_all_ini_section_pmu.optionxform = lambda option: option
    config_read_all_ini_section_pmu.read(pmu_ini_path)
    single_sub_section_list = config_read_all_ini_section_pmu.sections()

    return single_sub_section_list


if __name__ == '__main__':
    FET_section_name = sys.argv[1]

    single_sub_section_list = get_all_section_list(FET_section_name)

    cp_sub_config_and_process_for_pmu(FET_section_name)

    find_and_store_pmu_to_sub(FET_section_name, single_sub_section_list)

    combine_section_pmu_plot_path = 'combine_section_pmu_plot.ini'

    plot_all_combine_section_pmu(combine_section_pmu_plot_path)
