import requests
import platform
import json
import os
from bs4 import BeautifulSoup
from model.exploitdb_search import ExploitDBSearch
from model.system_info import SystemInfo


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


def get_json(url):
    request = requests.get(url, headers={"x-requested-with": "XMLHttpRequest",
                           "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"})
    if request.status_code == 200:
        return json.loads(request.content)['data']
    else:
        raise Exception("Bad request")


def get_html(url):
    request = requests.get(url, headers={"x-requested-with": "XMLHttpRequest",
                           "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"})
    if request.status_code == 200:
        return request.content
    else:
        raise Exception("Bad request")


def search(s):
    system_platform = get_system_info().system
    if s:
        url = f"{SEARCH_URL}&q={s}&platform={system_platform}"
    else:
        url = f"{SEARCH_URL}&platform={system_platform}"
    results = []
    json = get_json(url)
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
    cve_html = get_html(cve_url)
    soup = BeautifulSoup(cve_html, "lxml")
    description = soup.select_one("[data-testid=vuln-description]").text
    return cve + '\n' + 'Download url: ' + download_url + '\n' + title + '\n' + 'Description: ' + description
