"""
The function of this code is to control the execution of the throughput collection code for five times, add and average
the values collected each time, and then store them in the file.

Between the control code and the actual execution code, use py_pre_data_throughput_%s_%s.txt, and the average result is
output to result_throughput_%s_%s.

note: The function of each method can be known by referring to its method name.
"""
import sys
import subprocess
import time


def popen(cmd):
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         universal_newlines=True, executable="/bin/bash")
    out, err = p.communicate()
    return out + err


model_name = sys.argv[1]
device_name = sys.argv[2]
input_size = sys.argv[3]
batchsize = sys.argv[4]

FET_section_name = sys.argv[5]
input_size = int(input_size)
batchsize = int(batchsize)

result_mark = model_name + "_" + device_name + "_" + str(input_size) + "_" + str(batchsize)

print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
print("run py_throughput_record.py five times --> 1")
collect_data1 = popen("sudo python3 ./throughput/py_throughput_record.py %s %s %s %s %s" %
                      (model_name, device_name, input_size, batchsize, FET_section_name))
with open('./%s/throughput/out_pmu_popen_of_record_%s.txt' % (FET_section_name, result_mark), 'a') as f:
    f.write(collect_data1)

print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
print("run py_throughput_record.py five times --> 2")
collect_data2 = popen("sudo python3 ./throughput/py_throughput_record.py %s %s %s %s %s" %
                      (model_name, device_name, input_size, batchsize, FET_section_name))

with open('./%s/throughput/out_pmu_popen_of_record_%s.txt' % (FET_section_name, result_mark), 'a') as f:
    f.write(collect_data2)

print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
print("run py_throughput_record.py five times --> 3")
collect_data3 = popen("sudo python3 ./throughput/py_throughput_record.py %s %s %s %s %s" %
                      (model_name, device_name, input_size, batchsize, FET_section_name))
with open('./%s/throughput/out_pmu_popen_of_record_%s.txt' % (FET_section_name, result_mark), 'a') as f:
    f.write(collect_data3)

print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
print("run py_throughput_record.py five times --> 4")
collect_data4 = popen("sudo python3 ./throughput/py_throughput_record.py %s %s %s %s %s" %
                      (model_name, device_name, input_size, batchsize, FET_section_name))
with open('./%s/throughput/out_pmu_popen_of_record_%s.txt' % (FET_section_name, result_mark), 'a') as f:
    f.write(collect_data4)

print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
print("run py_throughput_record.py five times --> 5")
collect_data5 = popen("sudo python3 ./throughput/py_throughput_record.py %s %s %s %s %s" %
                      (model_name, device_name, input_size, batchsize, FET_section_name))
with open('./%s/throughput/out_pmu_popen_of_record_%s.txt' % (FET_section_name, result_mark), 'a') as f:
    f.write(collect_data5)

print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
print(
    "Five throughput collections have been completed. Now use ./%s/throughput/py_pre_data_throughput_%s_%s.txt to calculate the mean value of throughput."
    % (FET_section_name, model_name, result_mark))

throughput_result_file = popen(
    "touch ./%s/throughput/result_throughput_%s_%s.txt;sudo chmod 777 ./%s/throughput/result_throughput_%s_%s.txt;echo 'throughput_%s_%s: ' >> ./%s/throughput/result_throughput_%s_%s.txt"
    % (
        FET_section_name, model_name, result_mark, FET_section_name, model_name, result_mark, model_name,
        FET_section_name,
        result_mark, model_name, result_mark))

avg = popen(
    "awk '{sum+=$2}END{print sum/5}' ./%s/throughput/py_pre_data_throughput_%s_%s.txt >> ./%s/throughput/result_throughput_%s_%s.txt" %
    (FET_section_name, model_name, result_mark,
     FET_section_name, model_name, result_mark))

print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
print(
    "Five throughput collections of ./%s/throughput/py_pre_data_throughput_%s_%s.txt have been completed, view in ./%s/throughput/result_throughput_%s_%s.txt" %
    (FET_section_name, model_name, result_mark,
     FET_section_name, model_name, result_mark))
