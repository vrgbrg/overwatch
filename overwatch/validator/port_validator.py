from prompt_toolkit.validation import ValidationError


def open_port_validate(choosen_port, open_ports):
    try:
        port = int(choosen_port)
        if port not in open_ports:
            raise ValueError()
        return True
    except ValueError:
        raise ValidationError(message="Please enter an open port",
                              cursor_position=len(choosen_port))
