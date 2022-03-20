import os
import platform
from model.system_info import SystemInfo


def get_system_info(ip, nmScan):
    if ip == "localhost" or ip == "127.0.0.1":
        name = os.name
        system = platform.system()
        release = platform.release()
        print('System info: ' + system + ' - ' + release)
        if system == "Linux":
            system = 'linux'
        elif system == "Darwin":
            system = 'osx'
        elif system == "Win32":
            system = 'windows_x86'
        elif system == "Win64":
            system = 'windows_x86-64'
        return SystemInfo(name, system, release)
    else:
        nmScan.scan(ip, arguments='-O -v')
        name = nmScan[ip]['osmatch'][0]['osclass'][0]['vendor'].lower()
        system = nmScan[ip]['osmatch'][0]['osclass'][0]['osfamily'].lower()
        release = nmScan[ip]['osmatch'][0]['osclass'][0]['osgen'].lower()
        print('System info: ' + nmScan[ip]['osmatch'][0]['name'])
        return SystemInfo(name, system, release)


def check_useful_binaries(ip):
    cmd = 'which nmap aws nc ncat netcat nc.traditional wget curl ping gcc g++ make gdb base64 socat python python2 python3 python2.7 python2.6 python3.6 python3.7 perl php ruby xterm doas sudo fetch docker lxc ctr runc rkt kubectl 2>/dev/null'
    if ip == 'localhost' or ip == '127.0.0.1':
        print('Useful binaries: \n')
        os.system(cmd)
    else:
        return cmd


def check_compiler(ip):
    cmd = '(dpkg --list 2>/dev/null | grep "compiler" | grep -v "decompiler\|lib" 2>/dev/null || yum list installed \'gcc*\' 2>/dev/null | grep gcc 2>/dev/null; which gcc g++ 2>/dev/null || locate -r "/gcc[0-9\.-]\+$" 2>/dev/null | grep -v "/doc/")'
    if ip == 'localhost' or ip == '127.0.0.1':
        print('Available compilers: \n')
        os.system(cmd)
    else:
        return cmd


def find_suid_binaries(ip):
    cmd = 'find / -type f -perm -u=s 2>/dev/null'
    if ip == 'localhost' or ip == '127.0.0.1':
        print('SUID Binaries: \n')
        os.system(cmd)
    else:
        return cmd
