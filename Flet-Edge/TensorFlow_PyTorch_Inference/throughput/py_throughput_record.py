import torch
import torchvision
import torchvision.transforms as transforms
from time import time
import os
import sys
import py_throughput_model as throughput_model

model_name = sys.argv[1]
device_name = sys.argv[2]
input_size = sys.argv[3]
batchsize = sys.argv[4]

FET_section_name = sys.argv[5]
input_size = int(input_size)
batchsize = int(batchsize)

result_mark = model_name + "_" + device_name + "_" + str(input_size) + "_" + str(batchsize)

time1 = time()

os.environ['CUDA_VISIBLE_DEVICES'] = "0"
device = device_name
print("device:", device)
transform = transforms.Compose(
    [transforms.Resize(input_size),
     transforms.ToTensor(),
     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

batch_size = batchsize

testset = torchvision.datasets.CIFAR10(root='./throughput/data', train=False,
                                       download=True, transform=transform)
testloader = torch.utils.data.DataLoader(testset, batch_size=batch_size,
                                         shuffle=False, num_workers=0)

net = throughput_model.mobilenetv2()

if model_name == "shufflenet05":
    net = throughput_model.shufflenet05()
elif model_name == "mobilenetv2":
    net = throughput_model.mobilenetv2()
elif model_name == "resnet50":
    net = throughput_model.resnet50()
elif model_name == "resnet34":
    net = throughput_model.resnet34()
elif model_name == "vgg19":
    net = throughput_model.vgg19()

net.to(device)
net.to(device).eval()

throughput_time = 0

for epoch in range(1):

    for i, data in enumerate(testloader, 0):
        inputs, labels = data
        inputs, labels = inputs.to(device), labels.to(device)

        outputs = net(inputs)

    time2 = time()
    throughput_time = time2 - time1

throughput = 10000 / throughput_time
os.system("echo 'throughput: %s' >> ./%s/throughput/py_pre_data_throughput_%s_%s.txt" % (
    throughput, FET_section_name, model_name, result_mark))
