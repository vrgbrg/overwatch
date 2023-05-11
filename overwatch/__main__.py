import sys
import click
import pyfiglet
from PyInquirer.prompt import prompt
from vu_scanner import search as vu_scan, lookup as lookup_cve
from code_analysis_scanner import code_analysis
from helper.questions import restart_question, exit_question
import reports.report as report

def checkFormat(format):
    if format != "html" and format != "txt" and  format != "json" and format != "":
        raise BaseException("Invalid format flag value!")

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
@click.option('-f', '--format', 'format_', type=str, default="", required=False, show_default=True)
def search(ip, ports, keyword, format_):
    """Search through Exploit Database for vulnerabilities"""
    checkFormat(format_)
    report.setOutputFormat(format_)
    restart = True
    while restart:
        vu_scan(ip, ports, keyword)
        restart = prompt(restart_question()).get('restart')
        if not restart:
            if prompt(exit_question()).get('exit'):
                break
            else:
                restart = True


@main.command()
@click.argument('keyword', required=False)
@click.option('-f', '--format', 'format_', type=str, default="", required=False, show_default=True)
def lookup(keyword, format_):
    """Get vulnerability details using its EDB-ID on Exploit Database"""
    checkFormat(format_)
    report.setOutputFormat(format_)
    lookup_cve(keyword)
    report.render('lookup')


@main.command()
@click.argument('repo', required=False)
@click.argument('version', required=False)
@click.argument('level', required=False)
@click.option('-f', '--format', 'format_', type=str, default="", required=False, show_default=True)
def codeanalysis(repo, version, level, format_):
    """Run code analysis"""
    if repo:
        checkFormat(format_)
        report.setOutputFormat(format_)
        code_analysis(repo, version, level)
        report.render('codeanalysis')
    else:
        print('ERROR: Please give a repository')


if __name__ == '__main__':
    args = sys.argv
    if "--help" in args or len(args) == 1:
        print("CVE")
    main()
