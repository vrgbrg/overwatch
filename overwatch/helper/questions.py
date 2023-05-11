from validator.port_validator import open_port_validate


def open_port_question(open_ports):
    return [
        {
            'type': "input",
            "name": "port",
            "message": "Please select a port",
            "validate": lambda port: open_port_validate(port, open_ports),
            "filter": lambda port: int(port)
        }
    ]


def localhost_question():
    return [
        {
            'type': 'list',
            'name': 'scan',
            'message': 'What scan?',
            'choices': ['User list', 'Running processes', 'Suid binaries', 'Useful binaries', 'Available compilers', 'Mounted devices', 'CVE Search', 'Continue'],
            'filter': lambda val: val.lower()
        }
    ]


def ssh_question():
    return [
        {
            'type': 'list',
            'name': 'scan',
            'message': 'What scan?',
            'choices': ['User list', 'Suid binaries', 'Useful binaries', 'Available compilers', 'Reverse shell', 'Available credentials', 'Continue'],
            'filter': lambda val: val.lower()
        }
    ]

def telnet_question():
    return [
        {
            'type': 'list',
            'name': 'scan',
            'message': 'What scan?',
            'choices': ['User list', 'Suid binaries', 'Useful binaries', 'Available compilers', 'Reverse shell', 'Available credentials', 'Continue'],
            'filter': lambda val: val.lower()
        }
    ]

def continue_question():
    return [
        {
            'type': 'confirm',
            'message': 'Do you want to continue?',
            'name': 'continue',
            'default': True,
        }
    ]


def restart_question():
    return [
        {
            'type': 'confirm',
            'message': 'Do you want to restart?',
            'name': 'restart',
            'default': True,
        }
    ]


def exit_question():
    return [
        {
            'type': 'confirm',
            'message': 'Do you want to exit?',
            'name': 'exit',
            'default': False,
        },
    ]

def read_recent_result_question():
    return [
        {
            'type': 'confirm',
            'message': 'Do want to read the recent result?',
            'name': 'read',
            'default': False,
        },
    ]
