import configparser
import os
import subprocess
import linecache
import sys


def cp_sub_config_and_process_for_inference_time(FET_section_name):
    if os.path.exists("./%s/inference_time_out" % FET_section_name):
        print("./%s/inference_time_out exists." % FET_section_name)
    else:
        os.makedirs("./%s/inference_time_out" % FET_section_name)

    cp_sub_config_and_process_for_inference_time = popen("cp -r ../%s/%s_all_section.ini ./%s/%s_inference_time.ini" %
                                                         (FET_section_name, FET_section_name, FET_section_name,
                                                          FET_section_name))

    with open('./%s/inference_time_out/cp_sub_for_inference_time_of_FET_section_name.txt' % FET_section_name, 'a') as f:
        f.write(cp_sub_config_and_process_for_inference_time)
    print("cp_sub_config_and_process_for_inference_time --> %s" % "FET_section_name")

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


def store_inference_time_value_sub_inference_time_section_i(FET_section_name, section_name_i, inference_time_value):
    config_store_inference_time_data = configparser.RawConfigParser()
    config_store_inference_time_data.optionxform = lambda option: option
    inference_time_sub_ini_path = "./%s/%s_inference_time.ini" % (FET_section_name, FET_section_name)
    config_store_inference_time_data.read(inference_time_sub_ini_path)
    config_store_inference_time_data.set(section_name_i, "inference_time", "%s" % inference_time_value)

    config_store_inference_time_data.write(open(inference_time_sub_ini_path, 'w+'))

    return None


def find_and_store_inference_time_to_sub(FET_section_name, single_sub_section_list):
    len_single_sub_section_list = len(single_sub_section_list)
    for i in range(len_single_sub_section_list):
        section_name_i = single_sub_section_list[i]
        print(section_name_i)

        find_path = '../%s/inference_time/' % FET_section_name
        filename1 = "result"
        filename2 = section_name_i
        for root, dirs, files in os.walk(find_path):
            for file_name in files:
                if filename2 in file_name:
                    file_name_filename2 = file_name

                    if filename1 in file_name_filename2:
                        inference_time_value_scientific = linecache.getline(
                            "../%s/inference_time/%s" % (FET_section_name, file_name_filename2), 2)

                        inference_time_value = scientific_to_float(inference_time_value_scientific)

                        store_inference_time_value_sub_inference_time_section_i(FET_section_name, section_name_i,
                                                                                inference_time_value)

    return


def read_combine_section_inference_time_plot(combine_section_inference_time_plot_path, combine_section_name):
    config_read_combine_section_inference_time = configparser.RawConfigParser()
    config_read_combine_section_inference_time.optionxform = lambda option: option
    config_read_combine_section_inference_time.read(combine_section_inference_time_plot_path)
    combine_section_value = config_read_combine_section_inference_time.get(combine_section_name, "plot_combine_bar")

    combine_section_value_list = combine_section_value.split(" ")

    return combine_section_value_list


def start_inference_time_plot(FET_section_name, combine_section_value_list, combine_section_name):
    inference_time_data_path = "./%s/%s_inference_time.ini" % (FET_section_name, FET_section_name)

    combine_section_value_list_str = "+".join(combine_section_value_list)
    out_popen_of_inference_time_plot = popen("python3 inference_time_plot.py %s %s %s" % (
        inference_time_data_path, combine_section_value_list_str, combine_section_name))
    with open("out_popen_of_inference_time_plot_%s_%s.txt" % (FET_section_name, combine_section_name), 'a') as f:
        f.write(out_popen_of_inference_time_plot)
    print("popen_of_inference_time_plot_%s_%s" % (FET_section_name, combine_section_name))

    return None


def plot_all_combine_section_inference_time(combine_section_inference_time_plot_path):
    config_read_all_combine_section_inference_time = configparser.RawConfigParser()
    config_read_all_combine_section_inference_time.optionxform = lambda option: option
    config_read_all_combine_section_inference_time.read(combine_section_inference_time_plot_path)
    all_sections = config_read_all_combine_section_inference_time.sections()

    len_all_sections = len(all_sections)
    for i in range(len_all_sections):
        combine_section_name_i = all_sections[i]

        combine_section_value_list = read_combine_section_inference_time_plot(combine_section_inference_time_plot_path,
                                                                              combine_section_name_i)

        start_inference_time_plot(FET_section_name, combine_section_value_list, combine_section_name_i)

    return None


def get_all_section_list(FET_section_name):
    inference_time_ini_path = "./%s/%s_inference_time.ini" % (FET_section_name, FET_section_name)

    config_read_all_ini_section_inference_time = configparser.RawConfigParser()
    config_read_all_ini_section_inference_time.optionxform = lambda option: option
    config_read_all_ini_section_inference_time.read(inference_time_ini_path)
    single_sub_section_list = config_read_all_ini_section_inference_time.sections()

    return single_sub_section_list


if __name__ == '__main__':
    FET_section_name = sys.argv[1]

    single_sub_section_list = get_all_section_list(FET_section_name)

    cp_sub_config_and_process_for_inference_time(FET_section_name)

    find_and_store_inference_time_to_sub(FET_section_name, single_sub_section_list)

    combine_section_inference_time_plot_path = 'combine_section_inference_time_plot.ini'

    plot_all_combine_section_inference_time(combine_section_inference_time_plot_path)
