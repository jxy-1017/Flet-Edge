import torch.nn.functional as F
from PIL import Image
from torch.autograd import Variable
from torchvision import transforms
import numpy as np
import os
import subprocess
import threading
import py_CPU_GPU_model as cg_model
import sys

model_name = sys.argv[1]
device_name = sys.argv[2]
input_size = sys.argv[3]

batchsize_throughput = sys.argv[4]

FET_section_name = sys.argv[5]
input_size = int(input_size)
batchsize_throughput = int(batchsize_throughput)

result_mark = model_name + "_" + device_name + "_" + str(input_size) + "_" + str(batchsize_throughput)


def popen(cmd):
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         universal_newlines=True, executable="/bin/bash")
    out, err = p.communicate()
    return out + err


cmd = "sudo python3 ./cpu_gpu_utilization/py_jtop_logger_gpu_cpu.py %s %s" % (result_mark, FET_section_name)


class myThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        print("开始线程：" + self.name)
        popen(cmd)
        print("退出线程：" + self.name)


thread_popen = myThread(1, "Thread-popen")
thread_popen.setDaemon(True)
thread_popen.start()

os.environ['CUDA_VISIBLE_DEVICES'] = "0"
device = device_name
print("device:", device)
transform = transforms.Compose(
    [transforms.Resize(input_size),
     transforms.ToTensor(),
     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

net = cg_model.mobilenetv2()

if model_name == "shufflenet05":
    net = cg_model.shufflenet05()
elif model_name == "mobilenetv2":
    net = cg_model.mobilenetv2()
elif model_name == "resnet50":
    net = cg_model.resnet50()
elif model_name == "resnet34":
    net = cg_model.resnet34()
elif model_name == "vgg19":
    net = cg_model.vgg19()

net.to(device)
net.to(device).eval()

im = Image.open("8_190.jpg")
a = np.asarray(im)
img = Image.fromarray(a)
img = transform(img)
img = img.to(device)
img = img.unsqueeze(0)
output = net(img)
prob = F.softmax(output, dim=1)
prob = Variable(prob)
prob = prob.cpu().numpy()
pred = np.argmax(prob)
classes = ('plane', 'car', 'bird', 'cat',
           'deer', 'dog', 'frog', 'horse', 'ship', 'truck')
pred_class = classes[pred]
print(pred_class)
