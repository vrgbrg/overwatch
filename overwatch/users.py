import os
from helper.commands import FIND_USERS

def get_user_list(ip):
    if ip == "localhost" or ip == "127.0.0.1":
        users = os.popen(
            'dscl . list /Users | grep -v "^_"').read().split('\n')
        if len(users) > 0:
            for user in users:
                print(user)
    else:
        return FIND_USERS
