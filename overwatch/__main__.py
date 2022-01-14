import sys
import click
import pyfiglet
from vu_scanner import search as cve_search, lookup as lookup_cve


@click.group()
@click.version_option("0.0.1")
def main():
    """Vulnerability and exploit search engine"""
    ascii_banner = pyfiglet.figlet_format("overwatch")
    print(ascii_banner)
    pass


@main.command()
@click.argument('keyword', required=False)
def search(**kwargs):
    """Search through Exploit Database for vulnerabilities"""
    results = cve_search(kwargs.get("keyword"))
    for res in results:
        click.echo(f'{res}')


@main.command()
@click.argument('keyword', required=False)
def lookup(**kwargs):
    """Get vulnerability details using its EDB-ID on Exploit Database"""
    result = lookup_cve(kwargs.get("keyword"))
    click.echo(f'{result}')


if __name__ == '__main__':
    args = sys.argv
    if "--help" in args or len(args) == 1:
        print("CVE")
    main()
