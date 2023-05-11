import os
import json
from os.path import exists
import reports.report as report
from helper.questions import read_recent_result_question
from termcolor import colored
from PyInquirer.prompt import prompt

def code_analysis(repo, version, level):
    report.storeMessage("title", "Code Analysis Report")
    l = ""
    if level:
        l = " " + level.upper()

    if exists('./static_code_analysis/repo/result.json'):
        if not prompt(read_recent_result_question()).get('read'):
            os.system('./static_code_analysis/start.sh ' + repo + ' ' + version + l)

    result = open('./static_code_analysis/repo/result.json')
    data = json.load(result)
    results = []
    print(colored('Result: ', attrs=['bold']))
    for i in data['results']:
        results.append({ "level": i['extra']['severity'], "msg": i['extra']['message'] })
        if i['extra']['severity'] == 'INFO':
            print(colored(i['extra']['severity'], 'green') +
                  ' - ' + i['extra']['message'])
        elif i['extra']['severity'] == 'WARNING':
            print(colored(i['extra']['severity'], 'yellow') +
                  ' - ' + i['extra']['message'])
        elif i['extra']['severity'] == 'ERROR':
            print(colored(i['extra']['severity'], 'red') +
                  ' - ' + i['extra']['message'])
        else:
            print(i['extra']['severity'] + ' - ' + i['extra']['message'])
    report.storeMessage("results", results)
    report.storeMessage("repo", repo)
    report.storeMessage("version", version)
    report.storeMessage("level", level)
    print(colored('For more information please check result.json in static_code_analysis directory.', attrs=['bold']))
