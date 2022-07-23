import sys
import subprocess
import time

model_name = sys.argv[1]
device_name = sys.argv[2]
input_size = sys.argv[3]

batchsize_throughput = sys.argv[4]

FET_section_name = sys.argv[5]
input_size = int(input_size)
batchsize_throughput = int(batchsize_throughput)

result_mark = model_name + "_" + device_name + "_" + str(input_size) + "_" + str(batchsize_throughput)

mid_log_pre_name = result_mark + "flops_l1_l2"
result_pre_name = result_mark + "flops_l1_l2_result"


def popen(cmd):
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         universal_newlines=True, executable="/bin/bash")
    out, err = p.communicate()
    return out + err


print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

print("popen > run py file, collect data of FLOPs/L1/L2 >> %s_original.log" % mid_log_pre_name)
collect_data = popen(
    "sudo /usr/local/cuda/bin/nvprof -m gld_transactions -m gst_transactions -m atomic_transactions"
    " -m local_load_transactions -m local_store_transactions -m shared_load_transactions "
    "-m shared_store_transactions -m l2_read_transactions -m l2_write_transactions -m flop_count_sp "
    "--log-file ./%s/flops_l1_l2/%s_original.log python3 ./FLOPs_l1_l2/py_flops_select_all_model_infer.py %s %s %s %s"
    % (FET_section_name, mid_log_pre_name, model_name, device_name, input_size, batchsize_throughput))
with open('./%s/flops_l1_l2/out_pmu_popen_of_record_%s.txt' % (FET_section_name, result_mark), 'a') as f:
    f.write(collect_data)

print("popen > cp log file >> ./%s/flops_l1_l2/%s_original_cp.log" % (FET_section_name, mid_log_pre_name))
cp_data = popen("cp ./%s/flops_l1_l2/%s_original.log ./%s/flops_l1_l2/%s_original_cp.log" %
                (FET_section_name, mid_log_pre_name, FET_section_name, mid_log_pre_name))

print("popen > clean data >> ./%s/flops_l1_l2/%s_original_cp.log" % (FET_section_name, mid_log_pre_name))
clean_collect_data_01 = popen(
    "sed -i '1,4d' ./%s/flops_l1_l2/%s_original_cp.log" % ((FET_section_name, mid_log_pre_name)))
clean_collect_data_02 = popen(
    "sed -i '/Kernel/d' ./%s/flops_l1_l2/%s_original_cp.log" % ((FET_section_name, mid_log_pre_name)))

print(
    "popen > touch ./%s/flops_l1_l2/%s_all_results.log and chmod 777 ./%s/flops_l1_l2/%s_all_results.log and echo L1-L2-FLOPs" % (
        FET_section_name, result_pre_name, FET_section_name, result_pre_name))
file_proc = popen(
    "touch ./%s/flops_l1_l2/%s_all_results.log;sudo chmod 777 ./%s/flops_l1_l2/%s_all_results.log;echo 'L1-L2-FLOPs' >> ./%s/flops_l1_l2/%s_all_results.log"
    % (FET_section_name, result_pre_name, FET_section_name, result_pre_name, FET_section_name, result_pre_name))

print("popen > redirect L1 data >> ./%s/flops_l1_l2/%s_all_results.log" % (FET_section_name, mid_log_pre_name))
L1_data_redirect = popen(
    "grep -E 'gld_transactions | gst_transactions | atomic_transactions | local_load_transactions |"
    " local_store_transactions | shared_load_transactions | shared_store_transactions' ./%s/flops_l1_l2/%s_original_cp.log | "
    "awk '{product+=$1*$NF}END{print product*4}' >> ./%s/flops_l1_l2/%s_all_results.log" % (
        FET_section_name, mid_log_pre_name, FET_section_name, result_pre_name))
print(L1_data_redirect)

print("popen > redirect L2 data >> ./%s/flops_l1_l2/%s_all_results.log" % (FET_section_name, mid_log_pre_name))
L2_data_redirect = popen(
    "grep -E 'l2_read_transactions | l2_write_transactions' ./%s/flops_l1_l2/%s_original_cp.log | "
    "awk '{product+=$1*$NF}END{print product*4}' >> ./%s/flops_l1_l2/%s_all_results.log"
    % (FET_section_name, mid_log_pre_name, FET_section_name, result_pre_name))

print("popen > redirect FLOPs data >> ./%s/flops_l1_l2/%s_all_results.log" % (FET_section_name, mid_log_pre_name))
FLOPs_data_redirect = popen(
    "grep -E 'flop_count_sp' ./%s/flops_l1_l2/%s_original_cp.log | "
    "awk '{product+=$1*$NF}END{print product}' >> ./%s/flops_l1_l2/%s_all_results.log"
    % (FET_section_name, mid_log_pre_name, FET_section_name, result_pre_name))

print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
print("results of FLOPs/L1/L2 have been saved in ./%s/flops_l1_l2/%s_all_results.log." % (
    FET_section_name, mid_log_pre_name))
