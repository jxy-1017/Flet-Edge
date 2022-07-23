import subprocess


def popen(cmd):
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         universal_newlines=True, executable="/bin/bash")
    out, err = p.communicate()
    return out + err


out_of_popen_ansible_send_nanoX = popen("ansible %s -m copy -a 'src=./%s_all_hosts_files/%s dest=/home/%s/'"
                                        % ('nano1', 'FET_dt_experiment01', 'nano1', 'nano1'))
print(out_of_popen_ansible_send_nanoX)
