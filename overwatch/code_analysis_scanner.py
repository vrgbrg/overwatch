import os
import json
from termcolor import colored

def code_analysis(repo, version, level):
    os.system('./static_code_analysis/start.sh ' + repo + ' ' + version + ' ' + level.upper())
    result = open('./static_code_analysis/result.json')
    data = json.load(result)
    print(colored('Result: ', attrs=['bold']))
    for i in data['results']:
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
    print(colored('For more information please check result.json in static_code_analysis directory.', attrs=['bold']))
