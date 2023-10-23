LEN = 2


def cmd_validation(command):
    if command in ["NAME", "GET_NAMES", "MSG", "EXIT"]:
        return True
    return False


def get_msg(socket):
    length = socket.recv(LEN).decode()
    message = socket.recv(int(length)).decode()
    return message


def create_msg(msg):
    length = str(len(str(msg)))
    zfill_length = length.zfill(LEN)
    message = zfill_length + msg
    return message.encode()
