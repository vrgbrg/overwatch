import os


def get_user_list(ip):
    if ip == "localhost" or ip == "127.0.0.1":
        users = os.popen(
            'dscl . list /Users | grep -v "^_"').read().split('\n')
        if len(users) > 0:
            print('User list: \n')
            for user in users:
                print(user)
    else:
        return 'getent passwd | awk -F: \'{ print $1}\''
