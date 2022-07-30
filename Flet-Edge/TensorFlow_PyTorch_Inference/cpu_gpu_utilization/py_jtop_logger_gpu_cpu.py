"""
Operation mode, for example:
python3 jtop_logger_gpu_cpu.py shufflenet05

note: The function of each method can be known by referring to its method name.
"""
from jtop import jtop, JtopException
import argparse
import sys

result_mark = sys.argv[1]

FET_section_name = sys.argv[2]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Simple jtop logger')

    try:
        with jtop() as jetson:

            with open('./%s/cpu_gpu_utilization/py_pre_data_jtop_gpu_cpu_%s.txt' %
                      (FET_section_name, result_mark), 'a') as f:
                stats = jetson.stats

                while jetson.ok():
                    stats = jetson.stats

                    f.write(str(stats['time']) + " " + str(stats['GPU']) + " " + str(stats['CPU1']) + " " + str(
                        stats['CPU2']) + " " + str(stats['CPU3']) + " " + str(stats['CPU4']) + "\n")
                    print("Log at {time}".format(time=stats['time']))
                    print("GPU:", str(stats['GPU']), str(stats['CPU1']), str(stats['CPU2']), str(stats['CPU3']),
                          str(stats['CPU4']), )
    except JtopException as e:
        print(e)
    except KeyboardInterrupt:
        print("Closed with CTRL-C")
    except IOError:
        print("I/O error")
