"""
hierarchical_roofline main program, functions to be completed:

1. Generate the configuration file to be read;

2. To hierarchical_roofline_plot.py program passes in the list of combinations to be plotted plot_section_list。

Preparation process:
1. Refer to hierarchical_roofline file generation method of roofline is hierarchical_roofline value containing sub
configuration file of rootline is written:
(1) Hardware value section, for example:
[gflops_bandwidth_nano]
gflops = 387.93
l1 = 57.1
l2 = 38.95
dram = 25.6
(2) Values of gflops, L1, L2, and flops, for example:
gflops = 13.0827
l1 = 961836
l2 = 385724
flops = 31442347

note: The function of each method can be known by referring to its method name.
"""
import configparser
import os
import subprocess
import linecache
import sys


def cp_sub_config_and_process_for_hierarchical_roofline(FET_section_name):
    if os.path.exists("./%s/hierarchical_roofline_out" % FET_section_name):
        print("./%s/hierarchical_roofline_out exists." % FET_section_name)
    else:
        os.makedirs("./%s/hierarchical_roofline_out" % FET_section_name)

    cp_sub_config_and_process_for_hierarchical_roofline = popen(
        "cp -r ../%s/%s_all_section.ini ./%s/%s_hierarchical_roofline.ini" %
        (FET_section_name, FET_section_name, FET_section_name, FET_section_name))

    with open(
            './%s/hierarchical_roofline_out/cp_sub_for_hierarchical_roofline_of_FET_section_name.txt' % FET_section_name,
            'a') as f:
        f.write(cp_sub_config_and_process_for_hierarchical_roofline)
    print("cp_sub_config_and_process_for_hierarchical_roofline --> %s" % "FET_section_name")

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


def store_hierarchical_roofline_value_sub_hierarchical_roofline_section_i(FET_section_name, section_name_i, l1_value,
                                                                          l2_value, flops_value):
    config_store_hierarchical_roofline_data = configparser.RawConfigParser()
    config_store_hierarchical_roofline_data.optionxform = lambda option: option
    hierarchical_roofline_sub_ini_path = "./%s/%s_hierarchical_roofline.ini" % (FET_section_name, FET_section_name)
    config_store_hierarchical_roofline_data.read(hierarchical_roofline_sub_ini_path)
    config_store_hierarchical_roofline_data.set(section_name_i, "l1", "%s" % l1_value)
    config_store_hierarchical_roofline_data.set(section_name_i, "l2", "%s" % l2_value)
    config_store_hierarchical_roofline_data.set(section_name_i, "flops", "%s" % flops_value)

    config_store_hierarchical_roofline_data.write(open(hierarchical_roofline_sub_ini_path, 'w+'))

    return None


def store_hierarchical_roofline_value_sub_hierarchical_roofline_section_i_gflops(FET_section_name, section_name_i,
                                                                                 gflops_value):
    config_store_pmu_data = configparser.RawConfigParser()
    config_store_pmu_data.optionxform = lambda option: option
    pmu_sub_ini_path = "./%s/%s_hierarchical_roofline.ini" % (FET_section_name, FET_section_name)
    config_store_pmu_data.read(pmu_sub_ini_path)
    config_store_pmu_data.set(section_name_i, "gflops", "%s" % gflops_value)

    config_store_pmu_data.write(open(pmu_sub_ini_path, 'w+'))

    return None


def find_and_store_hierarchical_roofline_to_sub(FET_section_name, single_sub_section_list):
    len_single_sub_section_list = len(single_sub_section_list)
    for i in range(len_single_sub_section_list):
        section_name_i = single_sub_section_list[i]
        print(section_name_i)

        find_path = '../%s/flops_l1_l2/' % FET_section_name
        filename1 = "result_all_results"
        filename2 = section_name_i
        for root, dirs, files in os.walk(find_path):
            for file_name in files:
                if filename2 in file_name:
                    file_name_filename2 = file_name

                    if filename1 in file_name_filename2:
                        l1_value_scientific = linecache.getline("../%s/flops_l1_l2/%s" %
                                                                (FET_section_name, file_name_filename2), 2)

                        l2_value_scientific = linecache.getline("../%s/flops_l1_l2/%s" %
                                                                (FET_section_name, file_name_filename2), 3)

                        flops_value_scientific = linecache.getline("../%s/flops_l1_l2/%s" %
                                                                   (FET_section_name, file_name_filename2), 4)

                        l1_value = scientific_to_float(l1_value_scientific)
                        l2_value = scientific_to_float(l2_value_scientific)
                        flops_value = scientific_to_float(flops_value_scientific)

                        store_hierarchical_roofline_value_sub_hierarchical_roofline_section_i(FET_section_name,
                                                                                              section_name_i, l1_value,
                                                                                              l2_value, flops_value)

        find_path = '../%s/gflops/' % FET_section_name
        filename1 = "result_gflops"
        filename2 = section_name_i
        for root, dirs, files in os.walk(find_path):
            for file_name in files:
                if filename2 in file_name:
                    file_name_filename2 = file_name

                    if filename1 in file_name_filename2:
                        gflops_value_scientific = linecache.getline("../%s/gflops/%s" %
                                                                    (FET_section_name, file_name_filename2), 1)

                        gflops_value = scientific_to_float(gflops_value_scientific)

                        store_hierarchical_roofline_value_sub_hierarchical_roofline_section_i_gflops(FET_section_name,
                                                                                                     section_name_i,
                                                                                                     gflops_value)
    return


def read_combine_section_hierarchical_roofline_plot(combine_section_hierarchical_roofline_plot_path,
                                                    combine_section_name):
    config_read_combine_section_hierarchical_roofline = configparser.RawConfigParser()
    config_read_combine_section_hierarchical_roofline.optionxform = lambda option: option
    config_read_combine_section_hierarchical_roofline.read(combine_section_hierarchical_roofline_plot_path)
    combine_section_value = config_read_combine_section_hierarchical_roofline.get(combine_section_name,
                                                                                  "plot_combine_bar")

    combine_section_value_list = combine_section_value.split(" ")

    return combine_section_value_list


def start_hierarchical_roofline_plot(FET_section_name, combine_section_value_list, combine_section_name):
    hierarchical_roofline_data_path = "./%s/%s_hierarchical_roofline.ini" % (FET_section_name, FET_section_name)

    combine_section_value_list_str = "+".join(combine_section_value_list)
    out_popen_of_hierarchical_roofline_plot = popen("python3 hierarchical_roofline_plot.py %s %s %s" % (
    hierarchical_roofline_data_path, combine_section_value_list_str, combine_section_name))
    with open("out_popen_of_hierarchical_roofline_plot_%s_%s.txt" % (FET_section_name, combine_section_name), 'a') as f:
        f.write(out_popen_of_hierarchical_roofline_plot)
    print("popen_of_hierarchical_roofline_plot_%s_%s" % (FET_section_name, combine_section_name))

    return None


def plot_all_combine_section_hierarchical_roofline(FET_section_name, combine_section_hierarchical_roofline_plot_path):
    config_read_all_combine_section_hierarchical_roofline = configparser.RawConfigParser()
    config_read_all_combine_section_hierarchical_roofline.optionxform = lambda option: option
    config_read_all_combine_section_hierarchical_roofline.read(combine_section_hierarchical_roofline_plot_path)
    all_sections = config_read_all_combine_section_hierarchical_roofline.sections()

    len_all_sections = len(all_sections)
    for i in range(len_all_sections):
        combine_section_name_i = all_sections[i]

        combine_section_value_list = read_combine_section_hierarchical_roofline_plot(
            combine_section_hierarchical_roofline_plot_path, combine_section_name_i)

        start_hierarchical_roofline_plot(FET_section_name, combine_section_value_list, combine_section_name_i)

    return None


def store_nano_peak_value_to_sub_ini(FET_section_name):
    config_store_pmu_data = configparser.RawConfigParser()
    config_store_pmu_data.optionxform = lambda option: option
    pmu_sub_ini_path = "./%s/%s_hierarchical_roofline.ini" % (FET_section_name, FET_section_name)
    config_store_pmu_data.read(pmu_sub_ini_path)
    config_store_pmu_data.add_section("gflops_bandwidth_nano")
    config_store_pmu_data.set("gflops_bandwidth_nano", "gflops", "387.93")
    config_store_pmu_data.set("gflops_bandwidth_nano", "l1", "57.1")
    config_store_pmu_data.set("gflops_bandwidth_nano", "l2", "38.95")
    config_store_pmu_data.set("gflops_bandwidth_nano", "dram", "25.6")

    config_store_pmu_data.write(open(pmu_sub_ini_path, 'w+'))

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

    cp_sub_config_and_process_for_hierarchical_roofline(FET_section_name)

    find_and_store_hierarchical_roofline_to_sub(FET_section_name, single_sub_section_list)

    store_nano_peak_value_to_sub_ini(FET_section_name)

    combine_section_hierarchical_roofline_plot_path = 'combine_section_hierarchical_roofline_plot.ini'


    def plot_all_combine_section_hierarchical_roofline(FET_section_name,
                                                       combine_section_hierarchical_roofline_plot_path):

        config_read_all_combine_section_hierarchical_roofline = configparser.RawConfigParser()
        config_read_all_combine_section_hierarchical_roofline.optionxform = lambda option: option
        config_read_all_combine_section_hierarchical_roofline.read(combine_section_hierarchical_roofline_plot_path)
        all_sections = config_read_all_combine_section_hierarchical_roofline.sections()

        len_all_sections = len(all_sections)
        for i in range(len_all_sections):
            combine_section_name_i = all_sections[i]

            combine_section_value_list = read_combine_section_hierarchical_roofline_plot(
                combine_section_hierarchical_roofline_plot_path, combine_section_name_i)

            start_hierarchical_roofline_plot(FET_section_name, combine_section_value_list, combine_section_name_i)

        return None


    plot_all_combine_section_hierarchical_roofline(FET_section_name, combine_section_hierarchical_roofline_plot_path)
