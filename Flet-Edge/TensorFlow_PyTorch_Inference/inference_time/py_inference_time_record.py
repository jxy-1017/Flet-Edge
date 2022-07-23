import torch.nn.functional as F
from PIL import Image
from torch.autograd import Variable
from torchvision import transforms
import numpy as np
import os
import sys
from time import time

import py_inference_time_model as it_model

model_name = sys.argv[1]
device_name = sys.argv[2]
input_size = sys.argv[3]

batchsize_throughput = sys.argv[4]

FET_section_name = sys.argv[5]
input_size = int(input_size)
batchsize_throughput = int(batchsize_throughput)

result_mark = model_name + "_" + device_name + "_" + str(input_size) + "_" + str(batchsize_throughput)

os.environ['CUDA_VISIBLE_DEVICES'] = "0"
device = device_name
print("device:", device)
transform = transforms.Compose(
    [transforms.Resize(input_size),
     transforms.ToTensor(),
     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

net = it_model.mobilenetv2()

if model_name == "shufflenet05":
    net = it_model.shufflenet05()
elif model_name == "mobilenetv2":
    net = it_model.mobilenetv2()
elif model_name == "resnet50":
    net = it_model.resnet50()
elif model_name == "resnet34":
    net = it_model.resnet34()
elif model_name == "vgg19":
    net = it_model.vgg19()

net.to(device)
net.to(device).eval()

im = Image.open("8_190.jpg")
a = np.asarray(im)
img = Image.fromarray(a)
img = transform(img)
img = img.to(device)
img = img.unsqueeze(0)

output = net(img)

time1 = time()
for i in range(100):
    output = net(img)
time2 = time()
avg_time = ((time2 - time1) / 100)
print("avg time:", (time2 - time1) / 100)

prob = F.softmax(output, dim=1)
prob = Variable(prob)
prob = prob.cpu().numpy()
pred = np.argmax(prob)
classes = ('plane', 'car', 'bird', 'cat',
           'deer', 'dog', 'frog', 'horse', 'ship', 'truck')
pred_class = classes[pred]
print(pred_class)

os.system("echo 'avg_inference100_time: %s' >> ./%s/inference_time/py_pre_data_inference_time_%s_%s.txt" % (
    avg_time, FET_section_name, model_name, result_mark))
