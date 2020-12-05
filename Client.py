import socket
import msg
with socket.socket() as client_sock:
    address = ('localhost', 1234)
    client_sock.connect(address)
    message = "Helloooooooooooooasdfkjlwkejrasdfuuuuuuuu"
    try:
        query = msg.send_msg(client_sock, message)
        if query:
            answer = msg.read_msg(client_sock, 5)
            if answer:
                print(answer)

    except TypeError:
        print("Connection failed")




