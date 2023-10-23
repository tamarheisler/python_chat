import socket
import msvcrt
import select
import protocol

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.connect(("127.0.0.1", 5556))
msg = ""
while True:
    try:
        if msvcrt.kbhit():
            char = msvcrt.getche().decode('ASCII')
            if char == '\r':
                my_socket.send(protocol.create_msg(msg))
                msg = ""
            msg += char
        ready_socket = select.select([my_socket], [], [], 0.01)
        if msg == "EXIT":
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            break
        if ready_socket[0]:
            data = protocol.get_msg(my_socket)
            message = data
            print("\nServer replied:", message)


    except Exception as err:
        print(repr(err))


my_socket.close()
