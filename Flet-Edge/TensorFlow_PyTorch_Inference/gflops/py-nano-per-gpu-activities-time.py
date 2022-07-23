import sys
import subprocess
import time

model_name = sys.argv[1]
device_name = sys.argv[2]
input_size = sys.argv[3]
input_size = int(input_size)

batchsize_throughput = sys.argv[4]

FET_section_name = sys.argv[5]
input_size = int(input_size)
batchsize_throughput = int(batchsize_throughput)

result_mark = model_name + "_" + device_name + "_" + str(input_size) + "_" + str(batchsize_throughput)
tmp_pre_name = result_mark + "gpu_activities"


def popen(cmd):
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         universal_newlines=True, executable="/bin/bash")
    out, err = p.communicate()
    return out + err


print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

print("popen > run py file --print-summary-per-gpu collect data >> tmp_pre_name_original.log")
collect_data = popen(
    "sudo /usr/local/cuda/bin/nvprof --print-summary-per-gpu --log-file ./%s/gflops/%s_original.log python3 "
    "./gflops/py_gflops_gpu_time_select_all_model_infer100.py %s %s %s %s" %
    (FET_section_name, tmp_pre_name, model_name, device_name, input_size, batchsize_throughput))
with open('./%s/gflops/out_pmu_popen_of_record_%s.txt' % (FET_section_name, result_mark), 'a') as f:
    f.write(collect_data)

print("popen > sum time >> tmp_pre_name_sum_time.log")
sum_time_ms = popen(
    "grep 'ms' ./%s/gflops/%s_original.log | awk '{sum+=$4}END{print sum*1000}' > ./%s/gflops/%s_sum_time.log" %
    (FET_section_name, tmp_pre_name, FET_section_name, tmp_pre_name))

print("popen > gpu title time >> tmp_pre_name_sum_time.log")
sum_time_us = popen(
    "grep 'us' ./%s/gflops/%s_original.log | awk '{sum+=$4}END{print sum}' >> ./%s/gflops/%s_sum_time.log" %
    (FET_section_name, tmp_pre_name, FET_section_name, tmp_pre_name))

print("popen > gpu title time >>  tmp_pre_name_gpu_time_done.log")
out_time_100 = popen(
    "awk '{sum+=$1}END{print sum/100000000}' ./%s/gflops/%s_sum_time.log > ./%s/gflops/%s_gpu_time_done.log" %
    (FET_section_name, tmp_pre_name, FET_section_name, tmp_pre_name))
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
print("The results have been saved in tmp_pre_name_gpu_time_done.log.")

print("Use ../FLOPs_l1_l2/%s_all_results.log and file 2 to calculate gflops.")
flops_file_name = result_mark + "flops_l1_l2_result"

FLOPS = popen("flops_pre=$(awk 'NR==4' ./%s/flops_l1_l2/%s_all_results.log);"
              "gpu_time=$(awk '$1' ./%s/gflops/%s_gpu_time_done.log);"
              "echo $flops_pre/$gpu_time |bc >> ./%s/gflops/%s_result_flops.txt"
              % (FET_section_name, flops_file_name, FET_section_name, tmp_pre_name, FET_section_name, tmp_pre_name))

GFLOPS = popen(
    "awk '{flops=$1}END{print flops/1000000000} ' ./%s/gflops/%s_result_flops.txt >> ./%s/gflops/%s_result_gflops.txt" %
    (FET_section_name, tmp_pre_name, FET_section_name, tmp_pre_name))
