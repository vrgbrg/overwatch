# Overwatch
Vulnerability and exploit search engine

------
## Usage
\
Search through Exploit Database for vulnerabilities:

`python ./overwatch/__main__.py search 127.0.0.1`

or with dedicated keyword:

`python ./overwatch/__main__.py search 127.0.0.1 ssh`

\
Get vulnerability details using its EDB-ID on Exploit Database

`python ./overwatch/__main__.py lookup 40653`

Run static code analysis:

`python ./overwatch/__main__.py codeanalysis https://github.com/vrgbrg/overwatch`

Run static code analysis for dedicated version:

`python ./overwatch/__main__.py codeanalysis https://github.com/vrgbrg/overwatch <branch_name>/<version>`

------
## Help

`python ./overwatch/__main__.py --help`

------
## Version

`python ./overwatch/__main__.py --version`
