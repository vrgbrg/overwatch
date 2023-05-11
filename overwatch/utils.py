import os
import platform
import reports.report as report
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
        print("Processing...")
        binaries = os.popen(FIND_USEFUL_BINARIES).read().split("\n")
        if len(binaries) > 0:
            report.storeMessage("title", "Useful Binaries")
            report.storeMessage("useful_binaries", binaries)
            for b in binaries:
                print(b)
    else:
        return FIND_USEFUL_BINARIES


def check_compiler(ip):
    if ip == 'localhost' or ip == '127.0.0.1':
        print("Processing...")
        compilers = os.popen(FIND_AVAILABLE_COMPILERS).read().split("\n")
        if len(compilers) > 0:
            report.storeMessage("title", "Available Compilers")
            report.storeMessage("available_compilers", compilers)
            for c in compilers:
                print(c)
    else:
        return FIND_AVAILABLE_COMPILERS


def find_suid_binaries(ip):
    cmd = FIND_SUID_BINARIES
    if ip == 'localhost' or ip == '127.0.0.1':
        print("Processing...")
        binaries = os.popen(cmd).read().split("\n")
        if len(binaries) > 0:
            report.storeMessage("title", "SUID Binaries")
            report.storeMessage("binaries", binaries)
            for b in binaries:
                print(b)
    else:
        return cmd
