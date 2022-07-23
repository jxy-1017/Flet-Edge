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
