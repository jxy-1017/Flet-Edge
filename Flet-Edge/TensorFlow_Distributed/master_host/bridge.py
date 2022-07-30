"""
Add a program to the root directory of different hosts as a springboard. The function of this program is to obtain the
current host name and start change under the host folder change_dt_indir.py program.

Initially, it is sent to the target host along with the host name folder, mainly using host_name.ini file. Then store
it in the /root/ folder of the target host and wait for it to be dt_control_of_indir.py program starts.

After the program starts, get the host in the current folder host_name.ini's host_name, and then start the
corresponding host folder with medium change_dt_indir.py program.

note: The function of each method can be known by referring to its method name.
"""
import linecache
import subprocess


def get_host_name():
    host_name = linecache.getline("./host_name.ini", 4)
    print("host_name_change_dt_indir:", host_name)
    host_name = host_name.strip().replace(' ', '').replace('\n', '').replace('\r', '')
    return host_name


def popen(cmd):
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         universal_newlines=True, executable="/bin/bash")
    out, err = p.communicate()
    return out + err


if __name__ == '__main__':
    host_name = get_host_name()
    print(host_name)
    out_of_popen_start_change_dt_indir = popen("python3 /home/%s/%s/change_dt_indir.py" % (host_name, host_name))

    with open('out_of_popen_start_change_dt_indir_%s' % (host_name), 'a') as f:
        f.write(out_of_popen_start_change_dt_indir)
