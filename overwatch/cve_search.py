import click
from api import get_json, get_html
from model.exploitdb_search import ExploitDBSearch
from bs4 import BeautifulSoup
import reports.report as report

SEARCH_URL = "https://www.exploit-db.com/search?verified=true"
CVE_URL = "https://www.exploit-db.com/exploits/"


def cve_search(keyword, system_platform, open_ports):
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
                    v['id'], 'CVE-' + c['code'], " ".join(v['description'])))

    report.storeMessage("title", "CVE Search Result")
    report.storeMessage("search_url", url)
    report.storeMessage("keyword", keyword)
    report.storeMessage("platform", system_platform)
    report.storeMessage("ports", open_ports)
    report.storeMessage("results", results)
    for res in results:
        click.echo(f'{res}')


def cve_search_by_id(name):
    url = f"{CVE_URL}{name}"
    exploit_db_html = get_html(url, {"x-requested-with": "XMLHttpRequest",
                                     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"})
    soup = BeautifulSoup(exploit_db_html, 'lxml')
    title = soup.select_one(".card-title").text.strip()
    cve = 'CVE-' + soup.select_one(".info:nth-child(1) a").text.strip()
    download_url = 'https://www.exploit-db.com/download/' + name
    cve_url = soup.select_one(".info:nth-child(1) a").get("href")
    cve_html = get_html(cve_url, {"x-requested-with": "XMLHttpRequest",
                        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"})
    soup = BeautifulSoup(cve_html, "lxml")
    description = soup.select_one("[data-testid=vuln-description]").text

    report.storeMessage('cve', cve)
    report.storeMessage('download_url', download_url)
    report.storeMessage('title', title)
    report.storeMessage('description', description)

    return cve + '\n' + 'Download url: ' + download_url + '\n' + title + '\n' + 'Description: ' + description
