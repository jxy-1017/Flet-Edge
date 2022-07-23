import configparser
import itertools
import os
import subprocess
from distutils.util import strtobool
import time


def make_result_dir_3(FET_section_name, is_all_in, is_cpu_utilization_in, is_gpu_utilization_in, is_pum_in,
                      is_inference_time_in, is_flops_l1_l2_in, is_gflops_in):
    FET_section_name = FET_section_name

    is_all = is_all_in
    is_cpu_utilization = is_cpu_utilization_in
    is_gpu_utilization = is_gpu_utilization_in
    is_pum = is_pum_in
    is_inference_time = is_inference_time_in

    is_throughput = "False"
    is_throughput = strtobool(is_throughput)
    is_flops_l1_l2 = is_flops_l1_l2_in
    is_gflops = is_gflops_in

    if is_cpu_utilization or is_gpu_utilization:
        if os.path.exists("./%s/cpu_gpu_utilization" % FET_section_name):
            print("./%s/cpu_gpu_utilization exists." % FET_section_name)
        else:
            os.makedirs("./%s/cpu_gpu_utilization" % FET_section_name)

    if is_pum:
        if os.path.exists("./%s/pmu" % FET_section_name):
            print("./%s/pmu exists." % FET_section_name)
        else:
            os.makedirs("./%s/pmu" % FET_section_name)

    if is_inference_time:
        if os.path.exists("./%s/inference_time" % FET_section_name):
            print("./%s/inference_time exists." % FET_section_name)
        else:
            os.makedirs("./%s/inference_time" % FET_section_name)

    if is_throughput:
        if os.path.exists("./%s/throughput" % FET_section_name):
            print("./%s/throughput exists." % FET_section_name)
        else:
            os.makedirs("./%s/throughput" % FET_section_name)

    if is_flops_l1_l2:
        if os.path.exists("./%s/flops_l1_l2" % FET_section_name):
            print("./%s/flops_l1_l2 exists." % FET_section_name)
        else:
            os.makedirs("./%s/flops_l1_l2" % FET_section_name)

    if is_gflops:
        if os.path.exists("./%s/gflops" % FET_section_name):
            print("./%s/gflops exists." % FET_section_name)
        else:
            os.makedirs("./%s/gflops" % FET_section_name)


def make_result_dir_4(FET_section_name, is_all_in, is_cpu_utilization_in, is_gpu_utilization_in, is_pum_in,
                      is_inference_time_in, is_flops_l1_l2_in, is_gflops_in):
    FET_section_name = FET_section_name

    is_all = is_all_in
    is_cpu_utilization = is_cpu_utilization_in
    is_gpu_utilization = is_gpu_utilization_in
    is_pum = is_pum_in
    is_inference_time = is_inference_time_in

    is_throughput = "True"
    is_throughput = strtobool(is_throughput)
    is_flops_l1_l2 = is_flops_l1_l2_in
    is_gflops = is_gflops_in

    if is_cpu_utilization or is_gpu_utilization:
        if os.path.exists("./%s/cpu_gpu_utilization" % FET_section_name):
            print("./%s/cpu_gpu_utilization exists." % FET_section_name)
        else:
            os.makedirs("./%s/cpu_gpu_utilization" % FET_section_name)

    if is_pum:
        if os.path.exists("./%s/pmu" % FET_section_name):
            print("./%s/pmu exists." % FET_section_name)
        else:
            os.makedirs("./%s/pmu" % FET_section_name)

    if is_inference_time:
        if os.path.exists("./%s/inference_time" % FET_section_name):
            print("./%s/inference_time exists." % FET_section_name)
        else:
            os.makedirs("./%s/inference_time" % FET_section_name)

    if is_throughput:
        if os.path.exists("./%s/throughput" % FET_section_name):
            print("./%s/throughput exists." % FET_section_name)
        else:
            os.makedirs("./%s/throughput" % FET_section_name)

    if is_flops_l1_l2:
        if os.path.exists("./%s/flops_l1_l2" % FET_section_name):
            print("./%s/flops_l1_l2 exists." % FET_section_name)
        else:
            os.makedirs("./%s/flops_l1_l2" % FET_section_name)

    if is_gflops:
        if os.path.exists("./%s/gflops" % FET_section_name):
            print("./%s/gflops exists." % FET_section_name)
        else:
            os.makedirs("./%s/gflops" % FET_section_name)


def generate_sub_config_3_conditions(FET_section_name, without_throughput_combine_list, is_metrics,
                                     batchsize_throughput_list):
    if os.path.exists("./%s" % FET_section_name):
        print("./%s exists." % FET_section_name)
    else:
        os.makedirs("./%s" % FET_section_name)

    len_without_throughput_combine_list = len(without_throughput_combine_list)

    sub_ini_file_path = "./%s/%s_all_section.ini" % (FET_section_name, FET_section_name)

    is_metrics = is_metrics
    is_all_in = is_metrics[0]
    is_cpu_utilization_in = is_metrics[1]
    is_gpu_utilization_in = is_metrics[2]
    is_pum_in = is_metrics[3]
    is_inference_time_in = is_metrics[4]
    is_flops_l1_l2_in = is_metrics[5]
    is_gflops_in = is_metrics[6]

    FTE_sub_section_list = []

    make_result_dir_3(FET_section_name, is_all_in, is_cpu_utilization_in, is_gpu_utilization_in, is_pum_in,
                      is_inference_time_in, is_flops_l1_l2_in, is_gflops_in)

    for i in range(len_without_throughput_combine_list):
        model_name_in = without_throughput_combine_list[i][0]
        device_name_in = without_throughput_combine_list[i][1]
        input_size_in = without_throughput_combine_list[i][2]
        batchsize_throughput_in = batchsize_throughput_list[0]

        sub_config_mark = model_name_in + "_" + device_name_in + "_" + input_size_in

        config_generate_sub_config = configparser.ConfigParser()

        FTE_sub_section_list.append(sub_config_mark)

        config_generate_sub_config.add_section('%s' % sub_config_mark)
        config_generate_sub_config.set("%s" % sub_config_mark, "framework", "%s" % "pytorch")
        config_generate_sub_config.set("%s" % sub_config_mark, "model_name", "%s" % model_name_in)
        config_generate_sub_config.set("%s" % sub_config_mark, "device_name", "%s" % device_name_in)
        config_generate_sub_config.set("%s" % sub_config_mark, "input_size", "%s" % input_size_in)

        config_generate_sub_config.set("%s" % sub_config_mark, "batchsize_throughput", "%s" % batchsize_throughput_in)
        config_generate_sub_config.set("%s" % sub_config_mark, "is_all", "%s" % is_all_in)
        config_generate_sub_config.set("%s" % sub_config_mark, "is_cpu_utilization", "%s" % is_cpu_utilization_in)
        config_generate_sub_config.set("%s" % sub_config_mark, "is_gpu_utilization", "%s" % is_gpu_utilization_in)
        config_generate_sub_config.set("%s" % sub_config_mark, "is_pum", "%s" % is_pum_in)
        config_generate_sub_config.set("%s" % sub_config_mark, "is_inference_time", "%s" % is_inference_time_in)
        config_generate_sub_config.set("%s" % sub_config_mark, "is_throughput", "False")
        config_generate_sub_config.set("%s" % sub_config_mark, "is_flops_l1_l2", "%s" % is_flops_l1_l2_in)
        config_generate_sub_config.set("%s" % sub_config_mark, "is_gflops", "%s" % is_gflops_in)

        config_generate_sub_config.write(open(sub_ini_file_path, 'a'))

    return FTE_sub_section_list


def generate_sub_config_4_conditions(FET_section_name, with_throughput_combine_list, is_metrics):
    if os.path.exists("./%s" % FET_section_name):
        print("./%s exists." % FET_section_name)
    else:
        os.makedirs("./%s" % FET_section_name)

    len_with_throughput_combine_list = len(with_throughput_combine_list)

    sub_ini_file_path = "./%s/%s_all_section.ini" % (FET_section_name, FET_section_name)

    is_metrics = is_metrics
    is_all_in = is_metrics[0]
    is_cpu_utilization_in = is_metrics[1]
    is_gpu_utilization_in = is_metrics[2]
    is_pum_in = is_metrics[3]
    is_inference_time_in = is_metrics[4]
    is_flops_l1_l2_in = is_metrics[5]
    is_gflops_in = is_metrics[6]

    FTE_sub_section_list = []

    make_result_dir_4(FET_section_name, is_all_in, is_cpu_utilization_in, is_gpu_utilization_in, is_pum_in,
                      is_inference_time_in, is_flops_l1_l2_in, is_gflops_in)

    for i in range(len_with_throughput_combine_list):
        model_name_in = with_throughput_combine_list[i][0]
        device_name_in = with_throughput_combine_list[i][1]
        input_size_in = with_throughput_combine_list[i][2]
        batchsize_throughput_in = with_throughput_combine_list[i][3]

        sub_config_mark = model_name_in + "_" + device_name_in + "_" + input_size_in + "_" + batchsize_throughput_in

        config_generate_sub_config = configparser.ConfigParser()

        FTE_sub_section_list.append(sub_config_mark)

        config_generate_sub_config.add_section('%s' % sub_config_mark)
        config_generate_sub_config.set("%s" % sub_config_mark, "model_name", "%s" % model_name_in)
        config_generate_sub_config.set("%s" % sub_config_mark, "device_name", "%s" % device_name_in)
        config_generate_sub_config.set("%s" % sub_config_mark, "input_size", "%s" % input_size_in)
        config_generate_sub_config.set("%s" % sub_config_mark, "batchsize_throughput", "%s" % batchsize_throughput_in)
        config_generate_sub_config.set("%s" % sub_config_mark, "is_all", "%s" % is_all_in)
        config_generate_sub_config.set("%s" % sub_config_mark, "is_cpu_utilization", "%s" % is_cpu_utilization_in)
        config_generate_sub_config.set("%s" % sub_config_mark, "is_gpu_utilization", "%s" % is_gpu_utilization_in)
        config_generate_sub_config.set("%s" % sub_config_mark, "is_pum", "%s" % is_pum_in)
        config_generate_sub_config.set("%s" % sub_config_mark, "is_inference_time", "%s" % is_inference_time_in)
        config_generate_sub_config.set("%s" % sub_config_mark, "is_throughput", "True")
        config_generate_sub_config.set("%s" % sub_config_mark, "is_flops_l1_l2", "%s" % is_flops_l1_l2_in)
        config_generate_sub_config.set("%s" % sub_config_mark, "is_gflops", "%s" % is_gflops_in)

        config_generate_sub_config.write(open(sub_ini_file_path, 'a'))

    return FTE_sub_section_list


def combine_list_without_throughput(model_name_list, device_name_list, input_size_list):
    without_throughput_combine = itertools.product(model_name_list, device_name_list, input_size_list)
    without_throughput_combine_list = list(without_throughput_combine)
    print("without_throughput_combine_list:", len(without_throughput_combine_list))
    return without_throughput_combine_list


def combine_list_with_throughput(model_name_list, device_name_list, input_size_list, batchsize_throughput_list):
    with_throughput_combine = itertools.product(model_name_list, device_name_list, input_size_list,
                                                batchsize_throughput_list)
    with_throughput_combine_list = list(with_throughput_combine)
    print("with_throughput_combine_list:", len(with_throughput_combine_list))
    return with_throughput_combine_list


def judge_and_generate_sub_config(FET_section_name, is_throughput, model_name_list, device_name_list, input_size_list,
                                  batchsize_throughput_list, is_metrics):
    is_metrics = is_metrics

    if is_throughput:

        with_throughput_combine_list = combine_list_with_throughput(model_name_list, device_name_list, input_size_list,
                                                                    batchsize_throughput_list)

        FTE_sub_section_list = generate_sub_config_4_conditions(FET_section_name, with_throughput_combine_list,
                                                                is_metrics)


    else:

        without_throughput_combine_list = combine_list_without_throughput(model_name_list, device_name_list,
                                                                          input_size_list)

        FTE_sub_section_list = generate_sub_config_3_conditions(FET_section_name, without_throughput_combine_list,
                                                                is_metrics, batchsize_throughput_list)

    return FTE_sub_section_list


def FTE_read(FTE_path, FET_section_name):
    config_in = configparser.ConfigParser()
    FTE_file_path = "%s" % FTE_path
    config_in.read(FTE_file_path)

    model_name = config_in.get('%s' % FET_section_name, 'model_name')
    device_name = config_in.get('%s' % FET_section_name, 'device_name')
    input_size = config_in.get('%s' % FET_section_name, 'input_size')
    batchsize_throughput = config_in.get('%s' % FET_section_name, 'batchsize_throughput')

    is_throughput = config_in.getboolean('%s' % FET_section_name, 'is_throughput')

    is_metrics = []
    is_all = config_in.getboolean('%s' % FET_section_name, 'is_all')
    is_cpu_utilization = config_in.getboolean('%s' % FET_section_name, 'is_cpu_utilization')
    is_gpu_utilization = config_in.getboolean('%s' % FET_section_name, 'is_gpu_utilization')
    is_pum = config_in.getboolean('%s' % FET_section_name, 'is_pum')
    is_inference_time = config_in.getboolean('%s' % FET_section_name, 'is_inference_time')
    is_flops_l1_l2 = config_in.getboolean('%s' % FET_section_name, 'is_flops_l1_l2')
    is_gflops = config_in.getboolean('%s' % FET_section_name, 'is_gflops')

    is_metrics.append(is_all)
    is_metrics.append(is_cpu_utilization)
    is_metrics.append(is_gpu_utilization)
    is_metrics.append(is_pum)
    is_metrics.append(is_inference_time)
    is_metrics.append(is_flops_l1_l2)
    is_metrics.append(is_gflops)

    model_name_list = model_name.split(" ")
    device_name_list = device_name.split(" ")
    input_size_list = input_size.split(" ")
    batchsize_throughput_list = batchsize_throughput.split(" ")

    return is_throughput, model_name_list, device_name_list, input_size_list, batchsize_throughput_list, is_metrics


def read_single_sub_section_return_list(FTE_sub_section_list, i, config_sub_read):
    single_sub_section_list = []

    model_name = config_sub_read.get('%s' % FTE_sub_section_list[i], 'model_name')
    device_name = config_sub_read.get('%s' % FTE_sub_section_list[i], 'device_name')
    input_size = config_sub_read.get('%s' % FTE_sub_section_list[i], 'input_size')
    batchsize_throughput = config_sub_read.get('%s' % FTE_sub_section_list[i], 'batchsize_throughput')
    is_all = config_sub_read.get('%s' % FTE_sub_section_list[i], 'is_all')
    is_cpu_utilization = config_sub_read.get('%s' % FTE_sub_section_list[i], 'is_cpu_utilization')
    is_gpu_utilization = config_sub_read.get('%s' % FTE_sub_section_list[i], 'is_gpu_utilization')
    is_pum = config_sub_read.get('%s' % FTE_sub_section_list[i], 'is_pum')
    is_inference_time = config_sub_read.get('%s' % FTE_sub_section_list[i], 'is_inference_time')
    is_throughput = config_sub_read.get('%s' % FTE_sub_section_list[i], 'is_throughput')
    is_flops_l1_l2 = config_sub_read.get('%s' % FTE_sub_section_list[i], 'is_flops_l1_l2')
    is_gflops = config_sub_read.get('%s' % FTE_sub_section_list[i], 'is_gflops')

    single_sub_section_list.append(FTE_sub_section_list[i])
    single_sub_section_list.append(model_name)
    single_sub_section_list.append(device_name)
    single_sub_section_list.append(input_size)
    single_sub_section_list.append(batchsize_throughput)
    single_sub_section_list.append(is_all)
    single_sub_section_list.append(is_cpu_utilization)
    single_sub_section_list.append(is_gpu_utilization)
    single_sub_section_list.append(is_pum)
    single_sub_section_list.append(is_inference_time)
    single_sub_section_list.append(is_throughput)
    single_sub_section_list.append(is_flops_l1_l2)
    single_sub_section_list.append(is_gflops)

    return single_sub_section_list


def popen(cmd):
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         universal_newlines=True, executable="/bin/bash")
    out, err = p.communicate()
    return out + err


if __name__ == '__main__':

    FTE_path = "test_create_FTE.ini"

    FET_section_name = "FET_inference_experiment07"

    is_throughput, model_name_list, device_name_list, input_size_list, batchsize_throughput_list, is_metrics = FTE_read(
        FTE_path, FET_section_name)

    FTE_sub_section_list = judge_and_generate_sub_config(FET_section_name, is_throughput, model_name_list,
                                                         device_name_list, input_size_list, batchsize_throughput_list,
                                                         is_metrics)

    print("Reading the %s section of %s, judging and fully combining the conditions, and generating the sub "
          "configuration file ./%s/%s_all_section.ini have been completed." % (FET_section_name, FTE_path,
                                                                               FET_section_name, FET_section_name))

    config_sub_read = configparser.ConfigParser()
    config_sub_read_path = "./%s/%s_all_section.ini" % (FET_section_name, FET_section_name)
    config_sub_read.read(config_sub_read_path)

    for i in range(len(FTE_sub_section_list)):
        single_sub_section_list = read_single_sub_section_return_list(FTE_sub_section_list, i, config_sub_read)
        single_sub_section_list_string = "-".join(single_sub_section_list)
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        print("执行popen: %s" % single_sub_section_list[0])

        inference_control_stdout = popen("sudo python3 popen_inference_sequential_control_base.py %s %s"
                                         % (single_sub_section_list_string, FET_section_name))

        print(inference_control_stdout)
