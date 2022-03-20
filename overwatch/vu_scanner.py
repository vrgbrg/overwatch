import click
import nmap
from cve_search import cve_search, cve_search_by_id
from ssh_scan import ssh_connect, get_ssh_access
from processes_scan import get_running_processes
from port_scan import port_scan
from mount import check_mount_infos
from users import get_user_list
from utils import get_system_info, check_useful_binaries, check_compiler, find_suid_binaries
from helper.questions import open_port_question
from PyInquirer import prompt
from examples import custom_style_2

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

    answers = prompt(open_port_question(open_ports), style=custom_style_2)
    choosen_port = answers.get("port")
    if choosen_port == 22:
        valid_ssh_credentials = get_ssh_access(ip, nmScan)
        if valid_ssh_credentials:
            credentials = valid_ssh_credentials.split(':')
            ssh_connect(ip, 22, credentials[0], credentials[1])

    print('\n----------------------------------------------------\n')
    if(ip == 'localhost' or ip == '127.0.0.1'):
        get_running_processes(ip)
        print('\n----------------------------------------------------\n')
        get_user_list(ip)
        print('\n----------------------------------------------------\n')
        find_suid_binaries(ip)
        print('\n----------------------------------------------------\n')
        check_mount_infos()
        print('\n----------------------------------------------------\n')
        check_useful_binaries(ip)
        print('\n----------------------------------------------------\n')
        check_compiler(ip)
        print('\n----------------------------------------------------\n')

    cve_search(keyword, system_platform, open_ports)
    print('\n----------------------------------------------------\n')


def lookup(id):
    result = cve_search_by_id(id)
    click.echo(f'{result}')
