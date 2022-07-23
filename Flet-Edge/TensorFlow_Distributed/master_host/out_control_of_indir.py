import configparser
import os
import sys
import linecache
import xlrd
import xlwt
from xlutils.copy import copy
import subprocess


def all_sections_list_str_convert_to_all_sections_list(all_sections_from_main_str):
    all_sections_from_main_str = all_sections_from_main_str
    all_sections_from_main_list = all_sections_from_main_str.split("+")

    return all_sections_from_main_list


def write_section_to_per_ini(FTE_training_section_name, per_section_name):
    if os.path.exists("./per_section_name_dir"):
        print("./per_section_name_dir")
    else:
        os.makedirs("./per_section_name_dir")
    FTE_training_section_name = FTE_training_section_name
    per_section_name = per_section_name

    config_write_section_to_per_ini = configparser.RawConfigParser()
    config_write_section_to_per_ini.optionxform = lambda option: option
    config_write_section_to_per_ini.add_section("from_out_control")
    config_write_section_to_per_ini.set("from_out_control", "FTE_training_section_name",
                                        "%s" % FTE_training_section_name)
    config_write_section_to_per_ini.set("from_out_control", "sub_config_section_name", "%s" % per_section_name)

    config_write_section_to_per_ini.write(open("./per_section_name_dir/per_section_name.ini", 'w+'))


def get_current_dt_device_by_ansible(FTE_training_section_name, per_section_name):
    current_section_path = "./%s/%s_all_section.ini" % (FTE_training_section_name, FTE_training_section_name)
    config_get_current_dt_device_list_str = configparser.RawConfigParser()
    config_get_current_dt_device_list_str.optionxform = lambda option: option
    config_get_current_dt_device_list_str.read(current_section_path)
    current_dt_device_list_str = config_get_current_dt_device_list_str.get("%s" % per_section_name,
                                                                           "dt_device_name")

    current_dt_device_list = current_dt_device_list_str.split(" ")

    return current_dt_device_list


def out_control_generate_ansible_hosts_file_for_send_nanoX(current_dt_device_list):
    section_device_config_ip_read = configparser.ConfigParser()
    device_config_ini_path = "./FTE_device_config.ini"
    section_device_config_ip_read.read(device_config_ini_path)

    hosts_list = []

    len_current_dt_device_list = len(current_dt_device_list)
    for i in range(len_current_dt_device_list):
        per_dt_device_name = current_dt_device_list[i]
        hosts_list.append(per_dt_device_name)

        hosts_section = "[" + per_dt_device_name + "]"

        with open('hosts', 'a') as f:
            f.write(hosts_section + "\n")

        name_of_device_ip = per_dt_device_name + "_ip"

        dt_per_device_ip = section_device_config_ip_read.get("FTE_device_config", name_of_device_ip)

        with open('hosts', 'a') as f:
            f.write(dt_per_device_ip + "\n")

    return hosts_list


def popen(cmd):
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         universal_newlines=True, executable="/bin/bash")
    out, err = p.communicate()
    return out + err


def cp_hosts_to_etc_ansible(FTE_training_section_name, per_section_name):
    popen_cp_hosts_to_etc_ansible = popen("sudo cp -f ./hosts /etc/ansible/")
    with open('./%s/out_control_cp_hosts_to_etc_ansible/out_of_popen_cp_%s_%s.txt' % (
            FTE_training_section_name, FTE_training_section_name, per_section_name), 'a') as f:
        f.write(popen_cp_hosts_to_etc_ansible)
    return None


def popen_ansible_start_change_dt_indir(per_host_name, FTE_training_section_name, per_section_name):
    out_of_popen_ansible_start_change_dt_indir = \
        popen("ansible %s -m command -a 'sudo python3 /home/%s/%s/change_dt_indir.py'" % (
            per_host_name, per_host_name, per_host_name))
    with open(
            './%s/out_control_popen_ansible_start_change_dt_indir/out_of_popen_ansible_start_change_dt_indir_%s_%s_%s.txt' %
            (FTE_training_section_name, FTE_training_section_name, per_section_name, per_host_name), 'a') as f:
        f.write(out_of_popen_ansible_start_change_dt_indir)


def send_per_section_name_to_dt_device(hosts_list, FTE_training_section_name, per_section_name):
    len_hosts_list = len(hosts_list)
    for i in range(len_hosts_list):
        per_host_name = hosts_list[i]

        out_of_popen_ansible_send_per = popen("ansible %s -m copy -a 'src=./per_section_name_dir dest=/home/%s/%s'" %
                                              (per_host_name, per_host_name, per_host_name))
        with open('./%s/out_control_popen_ansible_send_per/out_of_popen_ansible_send_per_dir_%s_%s_%s.txt' %
                  (FTE_training_section_name, FTE_training_section_name, per_section_name, per_host_name), 'a') as f:
            f.write(out_of_popen_ansible_send_per)

    return None


def mkdir_for_record_stdout_of_popen(FTE_training_section_name):
    if os.path.exists("./%s/out_control_cp_hosts_to_etc_ansible" % FTE_training_section_name):
        print("./%s/out_control_cp_hosts_to_etc_ansible." % FTE_training_section_name)
    else:
        os.makedirs("./%s/out_control_cp_hosts_to_etc_ansible" % FTE_training_section_name)

    if os.path.exists("./%s/out_control_popen_ansible_send_per" % FTE_training_section_name):
        print("./%s/out_control_popen_ansible_send_per." % FTE_training_section_name)
    else:
        os.makedirs("./%s/out_control_popen_ansible_send_per" % FTE_training_section_name)

    if os.path.exists("./%s/out_control_popen_ansible_start_change_dt_indir" % FTE_training_section_name):
        print("./%s/out_control_popen_ansible_start_change_dt_indir." % FTE_training_section_name)
    else:
        os.makedirs("./%s/out_control_popen_ansible_start_change_dt_indir" % FTE_training_section_name)

    return None


def out_control_generate_ansible_hosts_file_for_start_bridge(current_dt_device_list):
    current_dt_device_list_str = "_".join(current_dt_device_list)

    hosts_group = "[" + current_dt_device_list_str + "]"
    hosts_group_str = current_dt_device_list_str

    with open('hosts', 'a') as f:
        f.write(hosts_group + "\n")

    current_dt_device_list_len = len(current_dt_device_list)

    device_config_ip_read = configparser.ConfigParser()
    device_config_ini_path = "FTE_device_config.ini"
    device_config_ip_read.read(device_config_ini_path)
    for i in range(current_dt_device_list_len):
        dt_per_device_name = current_dt_device_list[i]

        name_of_device_ip = dt_per_device_name + "_ip"

        dt_per_device_ip = device_config_ip_read.get("FTE_device_config", name_of_device_ip)

        with open('hosts', 'a') as f:
            f.write(dt_per_device_ip + "\n")

    return hosts_group_str


def popen_ansible_start_all_nanoX_change_dt_indir(hosts_group_str, FTE_training_section_name, per_section_name):
    out_of_popen_ansible_start_all_nanoX_change_dt_indir = \
        popen("ansible %s -m command -a 'python3 /root/bridge/bridge.py'" % (hosts_group_str))

    with open(
            './%s/out_control_popen_ansible_start_change_dt_indir/out_of_popen_ansible_start_all_nanoX_change_dt_indir_%s_%s.txt' %
            (FTE_training_section_name, FTE_training_section_name, per_section_name), 'a') as f:
        f.write(out_of_popen_ansible_start_all_nanoX_change_dt_indir)

    return None


def generate_dt_single_experiment_xls(dt_xls_name, host_manager_results_dir_path):
    workbook = xlwt.Workbook(encoding='utf-8')

    shufflenet05 = workbook.add_sheet('shufflenet05', cell_overwrite_ok=True)
    mobilenetv2 = workbook.add_sheet('mobilenetv2', cell_overwrite_ok=True)
    resnet50 = workbook.add_sheet('resnet50', cell_overwrite_ok=True)
    resnet34 = workbook.add_sheet('resnet34', cell_overwrite_ok=True)
    vgg19 = workbook.add_sheet('vgg19', cell_overwrite_ok=True)

    shufflenet05.write(0, 0, 'host_number')
    shufflenet05.write(0, 1, 'speedup')
    shufflenet05.write(0, 2, 'acc_imp')
    shufflenet05.write(0, 3, 'val_acc_imp')
    shufflenet05.write(0, 4, 'time_spend')
    shufflenet05.write(0, 5, 'acc')
    shufflenet05.write(0, 6, 'val_acc')

    mobilenetv2.write(0, 0, 'host_number')
    mobilenetv2.write(0, 1, 'speedup')
    mobilenetv2.write(0, 2, 'acc_imp')
    mobilenetv2.write(0, 3, 'val_acc_imp')
    mobilenetv2.write(0, 4, 'time_spend')
    mobilenetv2.write(0, 5, 'acc')
    mobilenetv2.write(0, 6, 'val_acc')

    resnet50.write(0, 0, 'host_number')
    resnet50.write(0, 1, 'speedup')
    resnet50.write(0, 2, 'acc_imp')
    resnet50.write(0, 3, 'val_acc_imp')
    resnet50.write(0, 4, 'time_spend')
    resnet50.write(0, 5, 'acc')
    resnet50.write(0, 6, 'val_acc')

    resnet34.write(0, 0, 'host_number')
    resnet34.write(0, 1, 'speedup')
    resnet34.write(0, 2, 'acc_imp')
    resnet34.write(0, 3, 'val_acc_imp')
    resnet34.write(0, 4, 'time_spend')
    resnet34.write(0, 5, 'acc')
    resnet34.write(0, 6, 'val_acc')

    vgg19.write(0, 0, 'host_number')
    vgg19.write(0, 1, 'speedup')
    vgg19.write(0, 2, 'acc_imp')
    vgg19.write(0, 3, 'val_acc_imp')
    vgg19.write(0, 4, 'time_spend')
    vgg19.write(0, 5, 'acc')
    vgg19.write(0, 6, 'val_acc')
    workbook.save('%s%s.xls' % (host_manager_results_dir_path, dt_xls_name))

    return None


def single_experiment_all_model_to_excel(host_name, FTE_training_section_name, dt_xls_name,
                                         FTE_training_sub_section_list):
    host_manager_results_dir_path = "~/" + host_name + "/" + FTE_training_section_name + "/"

    generate_dt_single_experiment_xls(dt_xls_name, host_manager_results_dir_path)

    len_FTE_training_sub_section_list = len(FTE_training_sub_section_list)
    for i in range(len_FTE_training_sub_section_list):

        FTE_training_sub_section_i = FTE_training_sub_section_list[i]

        host_manager_result_txt_i_path = host_manager_results_dir_path + FTE_training_sub_section_i

        popen_of_store_result = popen("cat %s | grep 'step - loss' | tail -1 >> %s%s_acc_val_acc_result.txt" %
                                      (host_manager_result_txt_i_path, host_manager_results_dir_path,
                                       FTE_training_sub_section_i))
        with open('%sout_popen_of_store_acc_val_acc_result_%s.txt' % (
                host_manager_results_dir_path, FTE_training_sub_section_i), 'a') as f:
            f.write(popen_of_store_result)

        popen_of_store_result = popen(
            "cat %s | grep 'The distributed training time of' | tail -1 >> %s%s_time_spend_result.txt" %
            (host_manager_result_txt_i_path, host_manager_results_dir_path, FTE_training_sub_section_i))
        with open('%sout_popen_of_store_time_spend_result_%s.txt' % (
                host_manager_results_dir_path, FTE_training_sub_section_i), 'a') as f:
            f.write(popen_of_store_result)
        table = xlrd.open_workbook('%s%s.xls' % (host_manager_results_dir_path, dt_xls_name))
        table_copy = copy(table)
        popen("awk '{acc = $11}END{print acc}' %s%s_acc_val_acc_result.txt >> %s%s_result_acc.txt; "
              "awk '{val_acc = $17}END{print val_acc}' %s%s_acc_val_acc_result.txt >> %s%s_result_val_acc.txt; " %
              (host_manager_results_dir_path, FTE_training_sub_section_i,
               host_manager_results_dir_path, FTE_training_sub_section_i,
               host_manager_results_dir_path, FTE_training_sub_section_i,
               host_manager_results_dir_path, FTE_training_sub_section_i))
        popen("awk '{spend_time = $10}END{print spend_time}' %s%s_time_spend_result.txt >> "
              "%s%s_result_time_spend.txt; " %
              (host_manager_results_dir_path, FTE_training_sub_section_i,
               host_manager_results_dir_path, FTE_training_sub_section_i))

        time_spend = linecache.getline(
            "%s%s_result_time_spend.txt" % (host_manager_results_dir_path, FTE_training_sub_section_i), 1)
        acc = linecache.getline("%s%s_result_acc.txt" % (host_manager_results_dir_path, FTE_training_sub_section_i), 1)
        val_acc = linecache.getline(
            "%s%s_result_val_acc.txt" % (host_manager_results_dir_path, FTE_training_sub_section_i), 1)
        if "shufflenet05" in FTE_training_sub_section_i:
            sheet_shufflenet05 = table_copy.get_sheet(0)
            sheet_shufflenet05.write(1, 4,
                                     label=time_spend.strip().replace(' ', '').replace('\n', '').replace('\r', ''))
            sheet_shufflenet05.write(1, 5, acc.strip().replace(' ', '').replace('\n', '').replace('\r', ''))
            sheet_shufflenet05.write(1, 6, val_acc.strip().replace(' ', '').replace('\n', '').replace('\r', ''))
            table_copy.save('%s%s.xls' % (host_manager_results_dir_path, dt_xls_name))

        if "mobilenetv2" in FTE_training_sub_section_i:
            sheet_mobilenetv2 = table_copy.get_sheet(1)
            sheet_mobilenetv2.write(1, 4, label=time_spend.strip().replace(' ', '').replace('\n', '').replace('\r', ''))
            sheet_mobilenetv2.write(1, 5, acc.strip().replace(' ', '').replace('\n', '').replace('\r', ''))
            sheet_mobilenetv2.write(1, 6, val_acc.strip().replace(' ', '').replace('\n', '').replace('\r', ''))
            table_copy.save('%s%s.xls' % (host_manager_results_dir_path, dt_xls_name))

        if "resnet50" in FTE_training_sub_section_i:
            sheet_resnet50 = table_copy.get_sheet(2)
            sheet_resnet50.write(1, 4, label=time_spend.strip().replace(' ', '').replace('\n', '').replace('\r', ''))
            sheet_resnet50.write(1, 5, acc.strip().replace(' ', '').replace('\n', '').replace('\r', ''))
            sheet_resnet50.write(1, 6, val_acc.strip().replace(' ', '').replace('\n', '').replace('\r', ''))
            table_copy.save('%s%s.xls' % (host_manager_results_dir_path, dt_xls_name))

        if "resnet34" in FTE_training_sub_section_i:
            sheet_resnet34 = table_copy.get_sheet(3)
            sheet_resnet34.write(1, 4, label=time_spend.strip().replace(' ', '').replace('\n', '').replace('\r', ''))
            sheet_resnet34.write(1, 5, acc.strip().replace(' ', '').replace('\n', '').replace('\r', ''))
            sheet_resnet34.write(1, 6, val_acc.strip().replace(' ', '').replace('\n', '').replace('\r', ''))
            table_copy.save('%s%s.xls' % (host_manager_results_dir_path, dt_xls_name))

        if "vgg19" in FTE_training_sub_section_i:
            sheet_vgg19 = table_copy.get_sheet(4)
            sheet_vgg19.write(1, 4, label=time_spend.strip().replace(' ', '').replace('\n', '').replace('\r', ''))
            sheet_vgg19.write(1, 5, acc.strip().replace(' ', '').replace('\n', '').replace('\r', ''))
            sheet_vgg19.write(1, 6, val_acc.strip().replace(' ', '').replace('\n', '').replace('\r', ''))
            table_copy.save('%s%s.xls' % (host_manager_results_dir_path, dt_xls_name))

    return None


def start_plot_mian(dt_plot_config_path, multiple_sections_list, host_name):
    multiple_sections_list_str = "+".join(multiple_sections_list)
    popen_out_of_start_plot_main = popen("python3 ./distrabuted_training_plot/dt_plot_mian.py %s %s %s" %
                                         (dt_plot_config_path, multiple_sections_list_str, host_name))
    with open('out_popen_of_start_plot_mian_%s.txt' % multiple_sections_list_str, 'a') as f:
        f.write(popen_out_of_start_plot_main)

    return None


if __name__ == '__main__':

    FTE_training_section_name = sys.argv[1]

    all_sections_from_main_str = sys.argv[2]
    dt_xls_name = sys.argv[3]

    all_sections_from_main_list = all_sections_list_str_convert_to_all_sections_list(all_sections_from_main_str)

    mkdir_for_record_stdout_of_popen(FTE_training_section_name)

    all_sections_from_main_list_len = len(all_sections_from_main_list)
    for i in range(all_sections_from_main_list_len):
        per_section_name = all_sections_from_main_list[i]

        write_section_to_per_ini(FTE_training_section_name, per_section_name)

        current_dt_device_list = get_current_dt_device_by_ansible(FTE_training_section_name,
                                                                  per_section_name)

        hosts_list = out_control_generate_ansible_hosts_file_for_send_nanoX(current_dt_device_list)

        cp_hosts_to_etc_ansible(FTE_training_section_name, per_section_name)

        send_per_section_name_to_dt_device(hosts_list, FTE_training_section_name, per_section_name)

        hosts_group_str = out_control_generate_ansible_hosts_file_for_start_bridge(current_dt_device_list)

        cp_hosts_to_etc_ansible(FTE_training_section_name, per_section_name)

        popen_ansible_start_all_nanoX_change_dt_indir(hosts_group_str, FTE_training_section_name, per_section_name)

    single_experiment_all_model_to_excel("nano3", FTE_training_section_name, dt_xls_name, all_sections_from_main_list)

    dt_plot_config_path = "~/nano3/" + FTE_training_section_name + "/distrabuted_training_plot/dt_plot_config.ini"
    multiple_sections_list = ["plot_dt_01"]
    host_name = "nano3"
    start_plot_mian(dt_plot_config_path, multiple_sections_list, host_name)
