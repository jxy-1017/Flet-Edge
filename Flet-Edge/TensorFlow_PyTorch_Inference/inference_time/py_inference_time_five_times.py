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

batchsize_throughput = sys.argv[4]

FET_section_name = sys.argv[5]
input_size = int(input_size)
batchsize_throughput = int(batchsize_throughput)

result_mark = model_name + "_" + device_name + "_" + str(input_size) + "_" + str(batchsize_throughput)

print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
print("run py_inference_time_record.py five times --> 1")
collect_data1 = popen("sudo python3 ./inference_time/py_inference_time_record.py %s %s %s %s %s" %
                      (model_name, device_name, input_size, batchsize_throughput, FET_section_name))
with open('./%s/inference_time/out_pmu_popen_of_record_%s.txt' % (FET_section_name, result_mark), 'a') as f:
    f.write(collect_data1)

print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
print("run py_inference_time_record.py five times --> 2")
collect_data2 = popen("sudo python3 ./inference_time/py_inference_time_record.py %s %s %s %s %s" %
                      (model_name, device_name, input_size, batchsize_throughput, FET_section_name))
with open('./%s/inference_time/out_pmu_popen_of_record_%s.txt' % (FET_section_name, result_mark), 'a') as f:
    f.write(collect_data2)

print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
print("run py_inference_time_record.py five times --> 3")
collect_data3 = popen("sudo python3 ./inference_time/py_inference_time_record.py %s %s %s %s %s" %
                      (model_name, device_name, input_size, batchsize_throughput, FET_section_name))
with open('./%s/inference_time/out_pmu_popen_of_record_%s.txt' % (FET_section_name, result_mark), 'a') as f:
    f.write(collect_data3)

print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
print("run py_inference_time_record.py five times --> 4")
collect_data4 = popen("sudo python3 ./inference_time/py_inference_time_record.py %s %s %s %s %s" %
                      (model_name, device_name, input_size, batchsize_throughput, FET_section_name))
with open('./%s/inference_time/out_pmu_popen_of_record_%s.txt' % (FET_section_name, result_mark), 'a') as f:
    f.write(collect_data4)

print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
print("run py_inference_time_record.py five times --> 5")
collect_data5 = popen("sudo python3 ./inference_time/py_inference_time_record.py %s %s %s %s %s" %
                      (model_name, device_name, input_size, batchsize_throughput, FET_section_name))
with open('./%s/inference_time/out_pmu_popen_of_record_%s.txt' % (FET_section_name, result_mark), 'a') as f:
    f.write(collect_data5)

print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
print(
    "Five inference time collections have been completed. Now use ./%s/inference_time/py_pre_date_inference_time_%s_%s.txt to calculate the mean value of inference time."
    % (FET_section_name, model_name, result_mark))

inference_time_result_file = popen(
    "touch ./%s/inference_time/result_inference_time_%s_%s.txt;./%s/inference_time/sudo chmod 777 result_inference_time_%s_%s.txt;echo 'inference time:%s_%s' >> ./%s/inference_time/result_inference_time_%s_%s.txt"
    % (FET_section_name, model_name, result_mark, FET_section_name, model_name, result_mark, model_name, result_mark,
       FET_section_name, model_name, result_mark))

avg = popen(
    "awk '{sum+=$2}END{print sum/5}' ./%s/inference_time/py_pre_data_inference_time_%s_%s.txt >> ./%s/inference_time/result_inference_time_%s_%s.txt" % (
        FET_section_name, model_name, result_mark,
        FET_section_name, model_name, result_mark))

print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
print(
    "Five inference time collections of ./%s/inference_time/py_pre_data_inference_time_%s_%s.txt have been completed, view in ./%s/inference_time/result_inference_time_%s_%s.txt" % (
        FET_section_name, model_name, result_mark,
        FET_section_name, model_name, result_mark))
