import socket
import json
import msg


def is_json(string):
    try:
        json.loads(string)
    except ValueError:
        return False
    return True


with socket.socket() as client_sock:
    address = ('localhost', 1234)
    client_sock.connect(address)
    try:
        server_msg = msg.read_msg(client_sock)
        print(server_msg)
        while server_msg:
            msg.send_msg(client_sock, input())
            server_msg = msg.read_msg(client_sock)
            if server_msg == 'Bye':
                print(server_msg)
                break
            if is_json(server_msg):
                server_msg = json.loads(server_msg)
                for index, value in server_msg.items():
                    print(f'{index}  {value}')
            else:
                print(server_msg)
    except TypeError:
        print("Connection failed")





