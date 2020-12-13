def read_msg(connection, size_pack=1024):
    size_msg = int(connection.recv(10).decode())
    msg = ''
    while size_msg > 0:
        data = connection.recv(size_pack).decode()
        size_msg -= size_pack
        msg += data
    return msg


def send_msg(connection, msg):
    size_msg = f'{len(msg):10}'
    connection.send(size_msg.encode())
    connection.send(msg.encode())
    print("message was sent successfully")


