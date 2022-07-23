import torchvision
import torch.nn as nn


def shufflenet05():
    net = torchvision.models.shufflenet_v2_x0_5()
    net.fc = nn.Sequential(
        nn.Linear(1024, 10)
    )
    return net


def mobilenetv2():
    net = torchvision.models.mobilenet_v2()

    net.classifier = nn.Sequential(
        nn.Dropout(p=0.2, inplace=False),
        nn.Linear(1280, 10))
    return net


def resnet50():
    net = torchvision.models.resnet50()

    net.fc = nn.Sequential(
        nn.Linear(2048, 10)
    )
    return net


def resnet34():
    net = torchvision.models.resnet34()
    net.fc = nn.Sequential(
        nn.Linear(512, 10)
    )
    return net


def vgg19():
    net = torchvision.models.vgg19()
    net.classifier = nn.Sequential(
        nn.Linear(25088, 4096, bias=True),
        nn.ReLU(inplace=True),
        nn.Dropout(0.5, inplace=False),
        nn.Linear(in_features=4096, out_features=4096, bias=True),
        nn.ReLU(inplace=True),
        nn.Dropout(p=0.5, inplace=False),
        nn.Linear(in_features=4096, out_features=10, bias=True)
    )
    return net
