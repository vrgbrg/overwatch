import click
import nmap
from cve_search import cve_search, cve_search_by_id
from telnet_scan import telnet_connect, get_telnet_access
from ssh_scan import ssh_connect, get_ssh_access
from processes_scan import get_running_processes
from port_scan import port_scan
from mount import check_mount_infos
from users import get_user_list
from utils import get_system_info, check_useful_binaries, check_compiler, find_suid_binaries
from helper.questions import open_port_question, localhost_question
from PyInquirer.prompt import prompt

nmScan = nmap.PortScanner()

open_ports = []


def search(ip, ports, keyword):
    if not ports:
        ports = 'top'

    system_platform = get_system_info(ip, nmScan)
    print('\n----------------------------------------------------\n')
    tmp_open_ports = port_scan(ip, ports, nmScan)
    for open_port in tmp_open_ports:
        open_ports.append(open_port)
    print('\n----------------------------------------------------\n')

    answers = prompt(open_port_question(open_ports))
    choosen_port = answers.get("port")
    if choosen_port == 22:
        valid_ssh_credentials = get_ssh_access(ip, nmScan)
        if valid_ssh_credentials:
            credentials = valid_ssh_credentials.split(':')
            ssh_connect(ip, 22, credentials[0], credentials[1])
    if choosen_port == 23:
        valid_telnet_credentials = get_telnet_access(ip, nmScan)
        if valid_telnet_credentials:
            credentials = valid_telnet_credentials.split(':')
            telnet_connect(ip, 23, credentials[0], credentials[1])

    print('\n----------------------------------------------------\n')
    if(ip == 'localhost' or ip == '127.0.0.1'):
        nextQuestion = True
        while nextQuestion:
            answer = prompt(localhost_question()).get('scan')
            if answer == 'user list':
                get_user_list(ip)
            elif answer == 'running processes':
                get_running_processes(ip)
            elif answer == 'suid binaries':
                find_suid_binaries(ip)
            elif answer == 'mounted devices':
                check_mount_infos()
            elif answer == 'useful binaries':
                check_useful_binaries(ip)
            elif answer == 'available compilers':
                check_compiler(ip)
            elif answer == 'continue':
                nextQuestion = False
        print('\n----------------------------------------------------\n')
    cve_search(keyword, system_platform.system, open_ports)
    print('\n----------------------------------------------------\n')


def lookup(id):
    result = cve_search_by_id(id)
    click.echo(f'{result}')
