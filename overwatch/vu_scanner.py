import platform
import os
import nmap
from api import get_json, get_html
from ssh_scan import ssh_connect, get_ssh_access
from processes_scan import get_running_processes
from port_scan import port_scan
from users import get_user_list
from bs4 import BeautifulSoup
from model.exploitdb_search import ExploitDBSearch
from model.system_info import SystemInfo

nmScan = nmap.PortScanner()
system_platform = ''


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

def search(ip, ports, keyword):
    if not ports:
        ports = 'top'

    if ip == "localhost" or ip == "127.0.0.1":
        system_platform = get_system_info().system
    else:
        nmScan.scan(ip, arguments='-O -v')
        system_platform = nmScan[ip]['osmatch'][0]['osclass'][0]['vendor'].lower(
        )
    print('----------------------------------------------------')
    get_user_list()
    print('----------------------------------------------------')
    open_ports = port_scan(ip, ports, nmScan)
    print('----------------------------------------------------')
    print('Running processes:')
    if ip == "localhost" or ip == "127.0.0.1":
        get_running_processes()
    else:
        print('TODO')
    print('----------------------------------------------------')

    if 22 in open_ports:
        valid_ssh_credentials = get_ssh_access(ip, nmScan)
        if valid_ssh_credentials:
            credentials = valid_ssh_credentials.split(':')
            ssh_connect(ip, 22, credentials[0], credentials[1], 'less /etc/passwd')
    print('----------------------------------------------------')

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
