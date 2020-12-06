import socket
import json
import msg


def is_json(string):
    try:
        json.loads(string)
    except ValueError:
        return False
    return True
i = 5
while i > 0:
    with socket.socket() as client_sock:
        address = ('localhost', 1234)
        client_sock.connect(address)
        try:
            query = msg.read_msg(client_sock)
            if query:
                print(query)
                answer = input()
                client_answer = msg.send_msg(client_sock, answer)
                server_answer = msg.read_msg(client_sock)
                if is_json(server_answer):
                    server_answer = json.loads(server_answer)
                    for index, value in server_answer.items():
                        print(f'{index}  {value}')
                else:
                    print(server_answer)
        except TypeError:
            print("Connection failed")
    i -= 1




