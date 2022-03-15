import os

def get_user_list():
    users = os.popen('dscl . list /Users | grep -v "^_"').read().split('\n')
    print('User list:')
    for user in users:
        print(user)
    return users