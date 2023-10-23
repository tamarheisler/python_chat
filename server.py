import socket
import select

import protocol

MAX_MSG_LENGTH = 1024
SERVER_PORT = 5556
CMD_WORD_LOCATION = 0

def print_client_sockets(all_client_sockets):
    for cs in all_client_sockets:
        print("\t", cs.getpeername())


def print_all_connection_names():
    all_names = ""
    for con in client_sockets:
        all_names += con[0]
    return all_names


def NAME_PRESSED(name, c_socket):
    dict_client_sockets[name] = c_socket
    messages_to_send.append((current_socket, protocol.create_msg("Hello " + name)))


def GET_NAMES_PRESSED(c_socket, clients_dict):
    messages_to_send.append((c_socket, protocol.create_msg((" ".join(clients_dict.keys())))))


def MSG_PRESSED(command_line, current_socket, clients_dict):
    dest_socket = command_line[1]
    msg_to_send = command_line[2]
    current_socket_name = get_socket_name(current_socket)
    data_ = (clients_dict[dest_socket], protocol.create_msg(current_socket_name + " sent " + msg_to_send))
    messages_to_send.append(data_)


def get_socket_name(one_socket):
    for key, val in dict_client_sockets.items():
        if val == one_socket:
            return key
    return None


SERVER_IP = "0.0.0.0"
print("Setting up server...")
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen()
print("Listening for clients...")
client_sockets = []
dict_client_sockets = {}
messages_to_send = []


while True:
    try:
        r_list, w_list, x_list = select.select([server_socket] + client_sockets, client_sockets, [])
        for current_socket in r_list:
            if current_socket is server_socket:
                connection, client_address = current_socket.accept()
                print("New client joined!", client_address)
                client_sockets.append(connection)
                print_client_sockets(client_sockets)
            else:
                # data = current_socket.recv(MAX_MSG_LENGTH).decode()
                data = protocol.get_msg(current_socket)
                split_data = data.split()
                if protocol.cmd_validation(split_data[0]) is not True:
                    print("command not valid")
                    break
                if split_data[CMD_WORD_LOCATION] == 'NAME':  # when socket want to call a name to himself
                    NAME_PRESSED(split_data[1], current_socket)
                elif split_data[CMD_WORD_LOCATION] == "GET_NAMES":
                    GET_NAMES_PRESSED(current_socket, dict_client_sockets)
                elif split_data[CMD_WORD_LOCATION] == "MSG":
                    MSG_PRESSED(split_data, current_socket, dict_client_sockets)
                elif split_data[CMD_WORD_LOCATION] == "EXIT":
                    # dict_client_sockets.pop(get_socket_name(current_socket))
                    print("connection closed")
                    client_sockets.remove(current_socket)
                    del dict_client_sockets[get_socket_name(current_socket)]
                    current_socket.close()
                if data == "":
                    print("Connection closed", )
                    client_sockets.remove(current_socket)
                    del dict_client_sockets[get_socket_name(current_socket)]
                    current_socket.close()
    except Exception as err:
        print(repr(err))


    for message in messages_to_send:
        current_socket, data = message
        if current_socket in w_list:
            current_socket.send(data)
        messages_to_send.remove(message)

