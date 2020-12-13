import socket
import msg


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
            print(server_msg)
    except TypeError:
        print("Connection failed")