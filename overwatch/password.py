import os
import re
from termcolor import colored

def credential_scan(etc_password, etc_shadow):
    file = open("./utils/password/etc_password.txt", "w")
    for row in etc_password:
        file.write(row)
    file.close()
    file = open("./utils/password/etc_shadow.txt", "w")
    for row in etc_shadow:
        file.write(row)
    file.close()
    os.popen(
        'unshadow ./utils/password/etc_password.txt ./utils/password/etc_shadow.txt > ./utils/password/john.txt')
    os.popen('john --wordlist=./utils/word_lists/rockyou.txt ./utils/password/john.txt').read()
    credentials = os.popen('john --show ./utils/password/john.txt').read()
    available_credentials = re.finditer(r"^[1-9]\d* password hashes cracked", credentials, re.MULTILINE)
    is_available_credentials = False
    for match in available_credentials:
            is_available_credentials = True
    
    if is_available_credentials:
        print('\n----------------------------------------------------\n')
        print(colored('Available credentials: \n', 'green'))
        for credential in credentials.split('\n'):
            if (len(credential) <= 0):
                break
            c = credential.split(":")
            print(colored(c[0] + " : " + c[1], 'green'))
    else:
        print('\nNo credential found.\n')
