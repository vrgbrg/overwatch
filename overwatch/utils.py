import os
import platform
from model.system_info import SystemInfo
from helper.commands import FIND_SUID_BINARIES, FIND_USEFUL_BINARIES, FIND_AVAILABLE_COMPILERS


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
    if ip == 'localhost' or ip == '127.0.0.1':
        os.system(FIND_USEFUL_BINARIES)
    else:
        return FIND_USEFUL_BINARIES


def check_compiler(ip):
    if ip == 'localhost' or ip == '127.0.0.1':
        os.system(FIND_AVAILABLE_COMPILERS)
    else:
        return FIND_AVAILABLE_COMPILERS


def find_suid_binaries(ip):
    cmd = FIND_SUID_BINARIES
    if ip == 'localhost' or ip == '127.0.0.1':
        os.system(cmd)
    else:
        return cmd
