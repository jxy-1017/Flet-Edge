"""
Control cpu/gpu、inference100_time、throughput program execution logic script.

Logic: control with if else statement.

Optimization 2: read the parameters by reading the INI file to transfer the parameters that need to be executed by this
control to the actual running program.

As for the upper program of the control program during reasoning, it is necessary to arrange and combine the different
conditions selected by the user to generate different configuration files. Each time, a flag is passed to the reasoning
file to control which sub configuration file the current control file reads to complete data collection.

“FTE_generate_sub_config_run_inference_control_popen_06_04.py”, this code is called in the Popen of control when it
starts inference.

note: The function of each method can be known by referring to its method name.
"""
import os
import sys
import subprocess
import time
from distutils.util import strtobool


def popen(cmd):
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         universal_newlines=True, executable="/bin/bash")
    out, err = p.communicate()
    return out + err


if __name__ == "__main__":

    single_sub_section_list_string = sys.argv[1]

    FET_section_name = sys.argv[2]

    single_sub_section_list = single_sub_section_list_string.split("-")

    print("single_sub_section_list_control: ", single_sub_section_list)

    single_sub_section_list_name = single_sub_section_list[0]
    model_name = single_sub_section_list[1]
    device_name = single_sub_section_list[2]
    input_size_str = single_sub_section_list[3]
    batchsize_throughput_str = single_sub_section_list[4]
    is_all_str = single_sub_section_list[5]
    is_cpu_utilization_str = single_sub_section_list[6]
    is_gpu_utilization_str = single_sub_section_list[7]
    is_pum_str = single_sub_section_list[8]
    is_inference_time_str = single_sub_section_list[9]
    is_throughput_str = single_sub_section_list[10]
    is_flops_l1_l2_str = single_sub_section_list[11]
    is_gflops_str = single_sub_section_list[12]

    input_size = int(input_size_str)
    batchsize_throughput = int(batchsize_throughput_str)

    is_all = strtobool(is_all_str)
    is_cpu_utilization = strtobool(is_cpu_utilization_str)
    is_gpu_utilization = strtobool(is_gpu_utilization_str)
    is_pum = strtobool(is_pum_str)
    is_inference_time = strtobool(is_inference_time_str)
    is_throughput = strtobool(is_throughput_str)
    is_flops_l1_l2 = strtobool(is_flops_l1_l2_str)
    is_gflops = strtobool(is_gflops_str)

    "配置文件的获取可使用：file = sys.argv[1]"

    if is_cpu_utilization and is_gpu_utilization:
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        print("cpu/gpu utilization collection program --> %s" % "py_CPU_GPU_record.py")

        out_cpu_gpu_popen = popen("sudo python3 ./cpu_gpu_utilization/py_CPU_GPU_record.py %s %s %s %s %s" %
                                  (model_name, device_name, input_size, batchsize_throughput, FET_section_name))

        result_mark = model_name + "_" + device_name + "_" + str(input_size) + "_" + str(batchsize_throughput)
        with open('./%s/cpu_gpu_utilization/out_cpu_gpu_popen_of_%s.txt' % (FET_section_name, result_mark), 'a') as f:
            f.write(out_cpu_gpu_popen)
        print("cpu/gpu utilization collection done --> %s" % "py_CPU_GPU_record.py")

    if is_pum:
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        print("pmu collection program py_pmu_five_times.py --> configure details: %s" % "py_pmu_record.py")

        out_pmu_popen = popen(
            "sudo python3 ./pmu/py_pmu_five_times.py %s %s %s %s %s" %
            (model_name, device_name, input_size, batchsize_throughput, FET_section_name))

        result_mark = model_name + "_" + device_name + "_" + str(input_size) + "_" + str(batchsize_throughput)
        with open('./%s/pmu/out_pmu_popen_of_%s.txt' % (FET_section_name, result_mark), 'a') as f:
            f.write(out_pmu_popen)
        print("pmu collection done py_pmu_five_times.py --> configure details: %s %s %s" % (
            model_name, device_name, input_size))

    if is_inference_time:
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        print("inference time collection program--> %s" % "py_inference_time_five_times.py")

        out_inference_time_popen = popen(
            "sudo python3 ./inference_time/py_inference_time_five_times.py %s %s %s %s %s" %
            (model_name, device_name, input_size, batchsize_throughput, FET_section_name))

        result_mark = model_name + "_" + device_name + "_" + str(input_size) + "_" + str(batchsize_throughput)
        with open('./%s/inference_time/out_inference_time_popen_of_%s.txt' % (FET_section_name, result_mark), 'a') as f:
            f.write(out_inference_time_popen)
        print("inference time collection done --> %s" % "py_inference_time_five_times.py")

    if is_throughput:
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        print("throughput collection program--> %s" % "py_throughput_five_times.py")
        out_throughput_popen = popen("sudo python3 ./throughput/py_throughput_five_times.py %s %s %s %s %s" %
                                     (model_name, device_name, input_size, batchsize_throughput, FET_section_name))

        result_mark = model_name + "_" + device_name + "_" + str(input_size) + "_" + str(batchsize_throughput)
        with open('./%s/throughput/out_throughput_popen_of_%s.txt' % (FET_section_name, result_mark), 'a') as f:
            f.write(out_throughput_popen)
        print("throughput collection done --> %s" % "py_throughput_five_times.py")

    if is_flops_l1_l2:
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        print("flops_l1_l2 collection program--> %s" % "py-nano-flops-l1-l2-get.py")

        out_flops_l1_l2_popen = popen("sudo python3 ./FLOPs_l1_l2/py-nano-flops-l1-l2-get.py %s %s %s %s %s" %
                                      (model_name, device_name, input_size, batchsize_throughput, FET_section_name))

        result_mark = model_name + "_" + device_name + "_" + str(input_size) + "_" + str(batchsize_throughput)
        with open('./%s/flops_l1_l2/out_flops_l1_l2_popen_of_%s.txt' % (FET_section_name, result_mark), 'a') as f:
            f.write(out_flops_l1_l2_popen)
        print("flops_l1_l2 collection done --> %s" % "py-nano-flops-l1-l2-get.py")

    if is_gflops:
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        print("flops_l1_l2 collection program--> %s" % "py-nano-per-gpu-activities-time.py")

        out_gflops_popen = popen(
            "sudo python3 ./gflops/py-nano-per-gpu-activities-time.py %s %s %s %s %s" %
            (model_name, device_name, input_size, batchsize_throughput, FET_section_name))

        result_mark = model_name + "_" + device_name + "_" + str(input_size) + "_" + str(batchsize_throughput)
        with open('./%s/gflops/out_gflops_popen_of_%s.txt' % (FET_section_name, result_mark), 'a') as f:
            f.write(out_gflops_popen)
        print("flops_l1_l2 collection done --> %s" % "py-nano-per-gpu-activities-time.py")

    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    print("Inference collection of %s has done." % single_sub_section_list_name)

    if os.path.exists("./plot_%s" % FET_section_name):
        print("./plot_%s" % FET_section_name)
    else:
        os.makedirs("./plot_%s" % FET_section_name)

    out_of_popen_cg_plot = popen(
        "python3 ./cpu_gpu_utilization_plot/cpu_gpu_utilization_plot_main.py %s " % (FET_section_name))
    with open("./plot_%s/out_of_popen_cg_plot.txt" % FET_section_name, 'a') as f:
        f.write(out_of_popen_cg_plot)

    out_of_popen_pmu_plot = popen("python3 ./pmu_plot/pmu_plot_mian.py %s" % (FET_section_name))
    with open("./plot_%s/out_of_popen_pmu_plot.txt" % FET_section_name, 'a') as f:
        f.write(out_of_popen_pmu_plot)

    out_of_popen_throughput_plot = popen("python3 ./throughput_plot/throughput_plot_mian.py %s" % (FET_section_name))
    with open("./plot_%s/out_of_popen_throughput_plot.txt" % FET_section_name, 'a') as f:
        f.write(out_of_popen_throughput_plot)

    out_of_popen_inference_time_plot = popen(
        "python3 ./inference_time_plot/inference_time_plot_mian.py %s" % (FET_section_name))
    with open("./plot_%s/out_of_popen_inference_time_plot.txt" % FET_section_name, 'a') as f:
        f.write(out_of_popen_inference_time_plot)

    out_of_popen_roofline_plot = popen("python3 ./roofline_plot/roofline_plot_mian.py %s" % (FET_section_name))
    with open("./plot_%s/out_of_popen_roofline_plot.txt" % FET_section_name, 'a') as f:
        f.write(out_of_popen_roofline_plot)
