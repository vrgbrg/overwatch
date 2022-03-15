def port_scan(ip, ports, nmScan):
    host = ip

    if ip == 'localhost':
        host = '127.0.0.1'

    if ports == 'top':
        nmScan.scan(host, arguments='--top-ports 20 -v')
    elif ports == 'all':
        nmScan.scan(host, arguments='-v -sU -sT -p- -T5')
    else:
        nmScan.scan(host, arguments='-v -p ' + ports)

    display_open_ports(nmScan)

    open_ports = []
    for p in nmScan[host]['tcp']:
        if nmScan[host]['tcp'][p]['state'] == 'open':
            open_ports.append(p)
    return open_ports


def display_open_ports(nmScan):
    for host in nmScan.all_hosts():
        print('Host : %s (%s)' % (host, nmScan[host].hostname()))
        print('State : %s' % nmScan[host].state())
        for proto in nmScan[host].all_protocols():
            print('----------------------------------------------------')
            print('Protocol : %s' % proto)
            lport = nmScan[host][proto].keys()
            for port in lport:
                print('port : %s\tstate : %s' %
                      (port, nmScan[host][proto][port]['state']))
