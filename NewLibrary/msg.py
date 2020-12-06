def read_msg(connection, size_pack=1024, encoding='utf-8'):
    # try:
        size_msg = int(connection.recv(10).decode())
        msg = ''
        while size_msg > 0:
            data = connection.recv(size_pack).decode(encoding=encoding)
            size_msg -= size_pack
            msg += data
        return msg
    # except Exception:
    #     print("some problems with read message")
    #     return False


def send_msg(connection, msg):

    # try:
        print(connection)
        size_msg = f'{len(msg):10}'
        connection.send(size_msg.encode())
        connection.send(msg.encode())
        print("message was sent successfully")
        return True
    # except Exception:
    #     print("some problems")
    #     return False


