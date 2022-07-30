"""
Progressive host number distributed training master program:

<1> Read the main configuration file, generate a list of full combination sub configuration files and record sub
configuration file sections;

<2> Generate folders of all hosts in the main configuration file and store them in sub configuration file, device
configuration file and control_dt_indir and change_dt_config two template programs and host identification files.

<3> Use ansible to transfer the folder to the corresponding host;

<4> Popen starts the outer control program, and at the same time, it passes in the list of recording sub configuration
file sections.

The program runs on a host running Flet-Edge, and the main configuration file FTE should be contained in the same
directory FTE_dt.ini, device configuration file FTE_device_config.ini.

The FTE of the main configuration file needs to be set at the beginning of the FTE_device_config.ini path, which
section in the main configuration file is the current experiment to take, that is, FTE_training_section_name。

note: The function of each method can be known by referring to its method name.
"""
import configparser
import itertools
import os
import subprocess


def mkdir_all_hosts_files(FTE_training_section_name):
    os.makedirs("./%s_all_hosts_files" % FTE_training_section_name)
    return None


def read_dt_FTE(FTE_dt_path, FTE_training_section_name):
    config_read_dt_FTE = configparser.RawConfigParser()
    config_read_dt_FTE.optionxform = lambda option: option
    config_read_dt_FTE.read(FTE_dt_path)

    training_batchsize = config_read_dt_FTE.get('%s' % FTE_training_section_name, 'training_batchsize')
    training_model_name = config_read_dt_FTE.get('%s' % FTE_training_section_name, 'training_model_name')
    weights = config_read_dt_FTE.get('%s' % FTE_training_section_name, 'weights')
    training_input_size = config_read_dt_FTE.get('%s' % FTE_training_section_name, 'training_input_size')
    optimizer_name = config_read_dt_FTE.get('%s' % FTE_training_section_name, 'optimizer_name')
    learning_rate_value = config_read_dt_FTE.get('%s' % FTE_training_section_name, 'learning_rate_value')
    epochs = config_read_dt_FTE.get('%s' % FTE_training_section_name, 'epochs')
    steps_per_epoch = config_read_dt_FTE.get('%s' % FTE_training_section_name, 'steps_per_epoch')
    validation_steps = config_read_dt_FTE.get('%s' % FTE_training_section_name, 'validation_steps')
    dataset_name = config_read_dt_FTE.get('%s' % FTE_training_section_name, 'dataset_name')
    frameworks = config_read_dt_FTE.get('%s' % FTE_training_section_name, 'frameworks')
    dt_device_number = config_read_dt_FTE.get('%s' % FTE_training_section_name, 'dt_device_number')
    dt_device_name = config_read_dt_FTE.get('%s' % FTE_training_section_name, 'dt_device_name')

    training_batchsize_list = training_batchsize.split(" ")
    training_model_name_list = training_model_name.split(" ")
    weights_list = weights.split(" ")
    training_input_size_list = training_input_size.split(" ")
    optimizer_name_list = optimizer_name.split(" ")
    learning_rate_value_list = learning_rate_value.split(" ")
    epochs_list = epochs.split(" ")
    steps_per_epoch_list = steps_per_epoch.split(" ")
    validation_steps_list = validation_steps.split(" ")
    dataset_name_list = dataset_name.split(" ")
    frameworks_list = frameworks.split(" ")
    dt_device_number_list = dt_device_number.split(" ")
    dt_device_name_list = dt_device_name.split(" ")

    return training_batchsize_list, training_model_name_list, weights_list, training_input_size_list, \
           optimizer_name_list, learning_rate_value_list, epochs_list, steps_per_epoch_list, \
           validation_steps_list, dataset_name_list, frameworks_list, dt_device_number_list, dt_device_name_list


def generate_sub_return_all_sub_section_list(training_batchsize_list, training_model_name_list, weights_list,
                                             training_input_size_list, optimizer_name_list, learning_rate_value_list,
                                             epochs_list, steps_per_epoch_list, validation_steps_list,
                                             dataset_name_list,
                                             frameworks_list, dt_device_number_list, dt_device_name_list,
                                             FTE_training_section_name):
    combine_of_13_FTE_dt = itertools.product(training_batchsize_list, training_model_name_list, weights_list,
                                             training_input_size_list, optimizer_name_list, learning_rate_value_list,
                                             epochs_list, steps_per_epoch_list, validation_steps_list,
                                             dataset_name_list,
                                             frameworks_list, dt_device_number_list)

    combine_of_13_FTE_dt_list = list(combine_of_13_FTE_dt)
    if os.path.exists("./%s" % FTE_training_section_name):
        print("./%s exists." % FTE_training_section_name)
    else:
        os.makedirs("./%s" % FTE_training_section_name)

    len_combine_of_13_FTE_dt_list = len(combine_of_13_FTE_dt_list)

    sub_ini_file_path = "./%s/%s_all_section.ini" % (FTE_training_section_name, FTE_training_section_name)

    FTE_training_sub_section_list = []
    dt_xls_name = None
    for i in range(len_combine_of_13_FTE_dt_list):
        training_batchsize_in = combine_of_13_FTE_dt_list[i][0]
        training_model_name_in = combine_of_13_FTE_dt_list[i][1]
        weights_in = combine_of_13_FTE_dt_list[i][2]
        training_input_size_in = combine_of_13_FTE_dt_list[i][3]
        optimizer_name_in = combine_of_13_FTE_dt_list[i][4]
        learning_rate_value_in = combine_of_13_FTE_dt_list[i][5]
        epochs_in = combine_of_13_FTE_dt_list[i][6]
        steps_per_epoch_in = combine_of_13_FTE_dt_list[i][7]
        validation_steps_in = combine_of_13_FTE_dt_list[i][8]
        dataset_name_in = combine_of_13_FTE_dt_list[i][9]
        frameworks_in = combine_of_13_FTE_dt_list[i][10]
        dt_device_number_in = combine_of_13_FTE_dt_list[i][11]

        sub_training_section_name = training_batchsize_in + "_" + training_model_name_in + "_" + weights_in + "_" \
                                                                                                              "" + training_input_size_in + "_" + optimizer_name_in + "_" + learning_rate_value_in + "_" + epochs_in + "_" \
                                                                                                                                                                                                                       "" + steps_per_epoch_in + "_" + validation_steps_in + "_" + dataset_name_in + "_" + frameworks_in + "_" \
                                                                                                                                                                                                                                                                                                                           "" + dt_device_number_in + "_" + '_'.join(
            dt_device_name_list)

        dt_xls_name = training_batchsize_in + "_" + "model" + "_" + weights_in + "_" \
                                                                                 "" + training_input_size_in + "_" + optimizer_name_in + "_" + learning_rate_value_in + "_" + epochs_in + "_" \
                                                                                                                                                                                          "" + steps_per_epoch_in + "_" + validation_steps_in + "_" + dataset_name_in + "_" + frameworks_in + "_" \
                                                                                                                                                                                                                                                                                              "" + dt_device_number_in + "_" + '_'.join(
            dt_device_name_list)

        config_generate_sub_training_config = configparser.RawConfigParser()
        config_generate_sub_training_config.optionxform = lambda option: option

        FTE_training_sub_section_list.append(sub_training_section_name)

        config_generate_sub_training_config.add_section('%s' % sub_training_section_name)

        config_generate_sub_training_config.set("%s" % sub_training_section_name, "training_batchsize",
                                                "%s" % training_batchsize_in)
        config_generate_sub_training_config.set("%s" % sub_training_section_name, "training_model_name",
                                                "%s" % training_model_name_in)
        config_generate_sub_training_config.set("%s" % sub_training_section_name, "weights", "%s" % weights_in)
        config_generate_sub_training_config.set("%s" % sub_training_section_name, "training_input_size",
                                                "%s" % training_input_size_in)
        config_generate_sub_training_config.set("%s" % sub_training_section_name, "optimizer_name",
                                                "%s" % optimizer_name_in)
        config_generate_sub_training_config.set("%s" % sub_training_section_name, "learning_rate_value",
                                                "%s" % learning_rate_value_in)
        config_generate_sub_training_config.set("%s" % sub_training_section_name, "epochs", "%s" % epochs_in)
        config_generate_sub_training_config.set("%s" % sub_training_section_name, "steps_per_epoch",
                                                "%s" % steps_per_epoch_in)
        config_generate_sub_training_config.set("%s" % sub_training_section_name, "validation_steps",
                                                "%s" % validation_steps_in)
        config_generate_sub_training_config.set("%s" % sub_training_section_name, "dataset_name",
                                                "%s" % dataset_name_in)
        config_generate_sub_training_config.set("%s" % sub_training_section_name, "frameworks", "%s" % frameworks_in)
        config_generate_sub_training_config.set("%s" % sub_training_section_name, "dt_device_number",
                                                "%s" % dt_device_number_in)
        config_generate_sub_training_config.set("%s" % sub_training_section_name, "dt_device_name",
                                                "%s" % ' '.join(dt_device_name_list))

        config_generate_sub_training_config.write(open(sub_ini_file_path, 'a'))
    print(
        "Experiment %s generated %s sub experiments." % (FTE_training_section_name, len(FTE_training_sub_section_list)))

    return FTE_training_sub_section_list, dt_xls_name


def popen(cmd):
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         universal_newlines=True, executable="/bin/bash")
    out, err = p.communicate()
    return out + err


def read_FTE_dt_device_name_generate_dir_and_host_name_ini(dt_device_name_list, FTE_training_section_name):
    len_dt_device_name_list = len(dt_device_name_list)
    for i in range(len_dt_device_name_list):
        host_name_i = dt_device_name_list[i]

        os.makedirs("./%s_all_hosts_files/%s" % (FTE_training_section_name, host_name_i))

        open('./%s_all_hosts_files/%s/host_name.ini' % (FTE_training_section_name, host_name_i), 'a')

        config_write_hosts_name_ini = configparser.RawConfigParser()
        config_write_hosts_name_ini.optionxform = lambda option: option

        config_write_hosts_name_ini.add_section("host_name")

        config_write_hosts_name_ini.set("host_name", "host_name", "%s" % host_name_i)

        config_write_hosts_name_ini.write(
            open('./%s_all_hosts_files/%s/host_name.ini' % (FTE_training_section_name, host_name_i), 'a'))

        with open('./%s_all_hosts_files/%s/host_name.ini' % (FTE_training_section_name, host_name_i), 'a') as f:
            f.write(host_name_i)

        os.makedirs("./%s_all_hosts_files/%s/bridge" % (FTE_training_section_name, host_name_i))

        popen("sudo cp -r ./bridge.py ./%s_all_hosts_files/%s/bridge" %
              (FTE_training_section_name, host_name_i))

        popen("sudo cp -r ./%s_all_hosts_files/%s/host_name.ini ./%s_all_hosts_files/%s/bridge" %
              (FTE_training_section_name, host_name_i, FTE_training_section_name, host_name_i))

        cp_experiment_dir_to_all_hosts_files = popen("sudo cp -r ./%s ./%s_all_hosts_files/%s/" %
                                                     (
                                                         FTE_training_section_name, FTE_training_section_name,
                                                         host_name_i))

        cp_device_config_to_all_hosts_files = popen("sudo cp -r ./FTE_device_config.ini ./%s_all_hosts_files/%s/" %
                                                    (FTE_training_section_name, host_name_i))

        cp_out_control_indir_to_all_hosts_files = popen("sudo cp -r ./change_dt_indir.py ./%s_all_hosts_files/%s/" %
                                                        (FTE_training_section_name, host_name_i))

        cp_change_config_to_all_hosts_files = popen("sudo cp -r ./change_dt_config.py ./%s_all_hosts_files/%s/" %
                                                    (FTE_training_section_name, host_name_i))

        cp_experiment_dir_to_all_hosts_files = popen("sudo cp -r ./tf_dt_change_models.py ./%s_all_hosts_files/%s/" %
                                                     (FTE_training_section_name, host_name_i))


def FTE_main_generate_ansible_hosts_file(dt_device_name_list):
    FTE_main_device_config_ip_read = configparser.ConfigParser()
    device_config_ini_path = "./FTE_device_config.ini"
    FTE_main_device_config_ip_read.read(device_config_ini_path)

    len_dt_device_name_list = len(dt_device_name_list)
    for i in range(len_dt_device_name_list):
        per_dt_device_name = dt_device_name_list[i]

        hosts_group = "[" + per_dt_device_name + "]"

        with open('hosts', 'a') as f:
            f.write(hosts_group + "\n")

        name_of_device_ip = per_dt_device_name + "_ip"

        dt_per_device_ip = FTE_main_device_config_ip_read.get("FTE_device_config", name_of_device_ip)

        with open('hosts', 'a') as f:
            f.write(dt_per_device_ip + "\n")

    return None


def cp_hosts_to_etc_ansible():
    popen("sudo cp -f ./hosts /etc/ansible/")

    return None


def send_nanoX_to_dt_device(dt_device_name_list, FTE_training_section_name):
    if os.path.exists("./%s/send_nanoX_to_dt_device" % FTE_training_section_name):
        print("./%s/send_nanoX_to_dt_device exists." % FTE_training_section_name)
    else:
        os.makedirs("./%s/send_nanoX_to_dt_device" % FTE_training_section_name)

    len_dt_device_name_list = len(dt_device_name_list)
    for i in range(len_dt_device_name_list):
        per_dt_device_name = dt_device_name_list[i]

        out_of_popen_ansible_send_nanoX = popen("ansible %s -m copy -a 'src=./%s_all_hosts_files/%s dest=/home/%s'"
                                                % (per_dt_device_name, FTE_training_section_name, per_dt_device_name,
                                                   per_dt_device_name))
        with open('./%s/send_nanoX_to_dt_device/out_of_%s_send_%s_by_ansible.txt' %
                  (FTE_training_section_name, FTE_training_section_name, per_dt_device_name), 'a') as f:
            f.write(out_of_popen_ansible_send_nanoX)

        out_of_popen_ansible_send_bridgeX = popen(
            "ansible %s -m copy -a 'src=./%s_all_hosts_files/%s/bridge dest=/root/'"
            % (per_dt_device_name, FTE_training_section_name, per_dt_device_name))
        with open('./%s/send_nanoX_to_dt_device/out_of_%s_send_%s_by_ansible_bridge.txt' %
                  (FTE_training_section_name, FTE_training_section_name, per_dt_device_name), 'a') as f:
            f.write(out_of_popen_ansible_send_bridgeX)
    return None


def popen_start_out_control(FTE_training_section_name, FTE_training_sub_section_list, dt_xls_name):
    if os.path.exists("./%s/popen_start_out_control" % FTE_training_section_name):
        print("./%s/popen_start_out_control." % FTE_training_section_name)
    else:
        os.makedirs("./%s/popen_start_out_control" % FTE_training_section_name)

    FTE_training_sub_section_list_str = "+".join(FTE_training_sub_section_list)
    out_of_popen_start_out_control = popen("sudo python3 out_control_of_indir.py %s %s %s " %
                                           (FTE_training_section_name, FTE_training_sub_section_list_str, dt_xls_name))
    with open('./%s/popen_start_out_control/out_of_popen_%s_start_out_control.txt' %
              (FTE_training_section_name, FTE_training_section_name), 'a') as f:
        f.write(out_of_popen_start_out_control)

    return None


if __name__ == '__main__':
    FTE_dt_path = "./FTE_dt.ini"
    FTE_training_section_name = "FET_dt_experiment03"

    mkdir_all_hosts_files(FTE_training_section_name)

    training_batchsize_list, training_model_name_list, weights_list, training_input_size_list, optimizer_name_list, \
    learning_rate_value_list, epochs_list, steps_per_epoch_list, validation_steps_list, dataset_name_list, \
    frameworks_list, dt_device_number_list, dt_device_name_list = read_dt_FTE(FTE_dt_path, FTE_training_section_name)

    FTE_training_sub_section_list, dt_xls_name = generate_sub_return_all_sub_section_list(training_batchsize_list,
                                                                                          training_model_name_list,
                                                                                          weights_list,
                                                                                          training_input_size_list,
                                                                                          optimizer_name_list,
                                                                                          learning_rate_value_list,
                                                                                          epochs_list,
                                                                                          steps_per_epoch_list,
                                                                                          validation_steps_list,
                                                                                          dataset_name_list,
                                                                                          frameworks_list,
                                                                                          dt_device_number_list,
                                                                                          dt_device_name_list,
                                                                                          FTE_training_section_name)

    read_FTE_dt_device_name_generate_dir_and_host_name_ini(dt_device_name_list, FTE_training_section_name)

    FTE_main_generate_ansible_hosts_file(dt_device_name_list)

    cp_hosts_to_etc_ansible()

    send_nanoX_to_dt_device(dt_device_name_list, FTE_training_section_name)

    popen_start_out_control(FTE_training_section_name, FTE_training_sub_section_list, dt_xls_name)
