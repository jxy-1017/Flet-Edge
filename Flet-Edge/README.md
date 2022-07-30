# Flet-Edge
## Introduction
### Flet-Edge
A Full Life-cycle Evaluation Tool for deep learning framework on the Edge

1. To describe the full life-cycle performance of deep learning frameworks on the edge, we proposed a metric set, PDR, includes three comprehensive sub-metrics: Programming complexity, Deployment complexity, and Runtime performance.

2. Based on the PDR, we designed and implemented a full life-cycle evaluation tool, Flet-Edge, which can automatically collect and present the PDR's metrics, visually.

3. With only one configuration file as input, the Flet-Edge will collect the twelve metrics of training or inference tasks and output them in text or chart. 

4. By observing the hierarchical roofline diagram provided by the Flet-Edge, you can see that the Flet-edge has the ability to optimize software and hardware of deep learning.

### PDR

<table>
   <tr>
      <td>Programming complexity</td>
      <td>Deployment complexity</td>
      <td>Runtime performance</td>
   </tr>
   <tr>
      <td>Github Populity</td>
      <td>Hardware Support</td>
      <td>CPU Utilization(Ⅰ,Ⅱ)</td>
   </tr>
   <tr>
      <td>API Intrgrity</td>
      <td>System and software support</td>
      <td>GPU Utilization(Ⅰ,Ⅱ)</td>
   </tr>
   <tr>
      <td>Pre-Training Models Support</td>
      <td>Task support</td>
      <td>Peak Memory Usage(Ⅰ,Ⅱ)</td>
   </tr>
   <tr>
      <td>Tool Support</td>
      <td>Deployment Flexibility</td>
      <td>Throughput(Ⅰ,Ⅱ)</td>
   </tr>
   <tr>
      <td></td>
      <td></td>
      <td>Speedup(Ⅰ)</td>
   </tr>
   <tr>
      <td></td>
      <td></td>
      <td>Acc-imp(Ⅰ)</td>
   </tr>
   <tr>
      <td></td>
      <td></td>
      <td>Inference Time(Ⅱ)</td>
   </tr>
   <tr>
      <td></td>
      <td></td>
      <td>Runtime Hierarchical Roofline(Ⅱ)</td>
   </tr>
   <tr>
      <td colspan="3">*Ⅰ:Metric concerned in training. *Ⅱ:Metric concerned inInference.</td>
   </tr>
</table>

## Programming complexity Components
### Frameworks
* TensorFlow
* PyTorch
* MXNet
* Paddle Paddle
* TensorFlow ite
* Paddle Lite
### Metrics
* Github Populity
  * Star
  * Watcher
  * Fork
  * Issue(closed)
  * Created
    
* API Intrgrity
  * NN
  * Activation
  * Loss
  * Optimizer
  * Regularizer
  * Callback
  * Device
  * Train
  * model save and use
* The Number of Pre-Trained Models
  * Images
  * Text
  * Audio
  * Video
  * other
* The Number of Tools
  * Visualization
  * Benchmarks
  * Optimize
  * Others

## Deployment complexity Components
### Frameworks
* TensorFlow
* PyTorch
* MXNet
* Paddle Paddle
* TensorFlow ite
* Paddle Lite
### Metrics
* Supported Categories of Hardware
  * Android
  * iOS
  * Arm
  * FPGA
  * GPU
* Supported Categories of System and Software
  * Linux
  * Windows
  * macOS
  * Docker
  * Python3
* Supported Categories of Task
  * Training
  * Inference
* Deployment Flexibility
  * Set
    * Installation
    * Distributed
  * Convert
    * CPU/GPU
    * Single/Distributed
    * Frame
    * Edge Model

## Runtime performance Components
### Benchmark 
* ShuffleNet v2 0.5×
* MobileNet v2
* ResNet-50
* ResNet-34
* VGG-19
### Support Hardware 
* Jetson NANO
* Raspberry Pi 4 Model B (Partially Supported)
### Inference
* CPU Utilization
* GPU Utilization
* Peak Memory Usage
* Throughput
* Inference Time
* Runtime Hierarchical Roofline
### Training
* CPU Utilization
* GPU Utilization
* Peak Memory Usage
* Throughput
* Speedup
* Acc-imp 

## Plotting Support
Support the Combination of multiple programs
* CPU Utilization
* GPU Utilization
* Peak Memory Usage
* Throughput
* Speedup (Number of variable hosts)
* Acc-imp (Number of variable hosts)
* Val-Acc-imp (Number of variable hosts)
* Inference Time
* Runtime Hierarchical Roofline

## Environment
* pipenv
* TensorFLow
* PyTorch
* ssh
* ansible
* jetson stat
* perf
* nvprof
* Matplotlib

## Method
### Install
1. Download the Flet-Edge project to the home directory of the host where Linux is installed.
2. Install and configure the environment.
### Training
#### Control node
1. Set the parameters of different test programs in the FTE_dt.ini file, such as framework, model, super parameters, etc.
2. Set the configuration information of different work points in the FTE_device_config.ini file, such as IP, virtual environment activation statement, etc.

#### Worker node
1. Install and configure the required environment.
### Inference
1. Set parameters of different test programs in test_create_FTE.ini file, such as framework, model, super parameters, etc.

## Note
1. The current version is an internal beta version, and there may be some points to be optimized. We are also debugging and updating.
2. In the future work, we will optimize the stability and reliability of the tool during operation.
3. More benchmark support will be added in the future.
4. The final version of our plan will support the testing of highly customized programs.

<p align="right">2022.07.30</p>






