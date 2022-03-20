import sys
import click
import pyfiglet
from PyInquirer import prompt
from examples import custom_style_1
from vu_scanner import search as vu_scan, lookup as lookup_cve
from code_analysis_scanner import code_analysis
from helper.questions import restart_question, exit_question


@click.group()
@click.version_option("0.0.1")
def main():
    """Vulnerability and exploit search engine"""
    ascii_banner = pyfiglet.figlet_format("overwatch")
    print(ascii_banner)
    pass


@main.command()
@click.argument('ip', required=False)
@click.argument('ports', required=False)
@click.argument('keyword', required=False)
def search(**kwargs):
    """Search through Exploit Database for vulnerabilities"""
    restart = True
    while restart:
        vu_scan(kwargs.get("ip"), kwargs.get("ports"), kwargs.get("keyword"))
        restart = prompt(restart_question(),
                         style=custom_style_1).get('restart')
        if not restart:
            if prompt(exit_question(), style=custom_style_1).get('exit'):
                break
            else:
                restart = True


@main.command()
@click.argument('keyword', required=False)
def lookup(**kwargs):
    """Get vulnerability details using its EDB-ID on Exploit Database"""
    lookup_cve(kwargs.get("keyword"))


@main.command()
@click.argument('repo', required=False)
@click.argument('version', required=False)
@click.argument('level', required=False)
def codeanalysis(**kwargs):
    """Run code analysis"""
    if kwargs.get("repo"):
        code_analysis(kwargs.get("repo"), kwargs.get(
            "version"), kwargs.get("level"))
    else:
        print('ERROR: Please give a repository')


if __name__ == '__main__':
    args = sys.argv
    if "--help" in args or len(args) == 1:
        print("CVE")
    main()
