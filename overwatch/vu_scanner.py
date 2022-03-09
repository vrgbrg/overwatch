import platform
import os
import nmap
from api import get_json, get_html

from bs4 import BeautifulSoup
from model.exploitdb_search import ExploitDBSearch
from model.system_info import SystemInfo

nmScan = nmap.PortScanner()

def get_system_info():
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

SEARCH_URL = "https://www.exploit-db.com/search?verified=true"
CVE_URL = "https://www.exploit-db.com/exploits/"

def port_scan(ip, ports):
    host = ip

    if ip == 'localhost':
        host = '127.0.0.1'

    if ports == 'top':
        nmScan.scan(host, arguments='--top-ports 20 -v')
    elif ports == 'all':
        nmScan.scan(host, arguments='-v -sU -sT -p- -T5')
    else:
        print('hello')
        nmScan.scan(host, arguments='-v -p ' + ports)

    display_open_ports()

    open_ports = []
    for p in nmScan[host]['tcp']:
        if nmScan[host]['tcp'][p]['state'] == 'open':
            open_ports.append(p)
    return open_ports

def display_open_ports():
    for host in nmScan.all_hosts():
        print('----------------------------------------------------')
        print('Host : %s (%s)' % (host, nmScan[host].hostname()))
        print('State : %s' % nmScan[host].state())
        for proto in nmScan[host].all_protocols():
            print('----------------------------------------------------')
            print('Protocol : %s' % proto)
            lport = nmScan[host][proto].keys()
            for port in lport:
                print('port : %s\tstate : %s' %
                      (port, nmScan[host][proto][port]['state']))
        print('----------------------------------------------------')

def search(ip, ports, keyword):
    if not ports:
        ports = 'top'

    if ip == "localhost" or ip == "127.0.0.1":
        system_platform = get_system_info().system
    else:
        nmScan.scan(ip, arguments='-O -v')
        system_platform = nmScan[ip]['osmatch'][0]['osclass'][0]['vendor'].lower(
        )

    open_ports = port_scan(ip, ports)
    port_params = ''

    for p in open_ports:
        port_params += '&port=' + str(p)

    if keyword:
        url = f"{SEARCH_URL}&q={keyword}&platform={system_platform}{port_params}"
    else:
        url = f"{SEARCH_URL}&platform={system_platform}{port_params}"

    results = []

    json = get_json(url, {"x-requested-with": "XMLHttpRequest",
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"})

    for v in json:
        for c in v['code']:
            if c['code_type'] == 'cve':
                results.append(ExploitDBSearch(
                    v['id'], 'CVE-' + c['code'], v['description'][1]))

    return results

def lookup(name):
    url = f"{CVE_URL}{name}"
    exploit_db_html = get_html(url)
    soup = BeautifulSoup(exploit_db_html, "lxml")
    title = soup.select_one(".card-title").text.strip()
    cve = 'CVE-' + soup.select_one(".info:nth-child(1) a").text.strip()
    download_url = 'https://www.exploit-db.com/download/' + name
    cve_url = soup.select_one(".info:nth-child(1) a").get("href")
    cve_html = get_html(cve_url, {"x-requested-with": "XMLHttpRequest",
                        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"})
    soup = BeautifulSoup(cve_html, "lxml")
    description = soup.select_one("[data-testid=vuln-description]").text
    return cve + '\n' + 'Download url: ' + download_url + '\n' + title + '\n' + 'Description: ' + description
