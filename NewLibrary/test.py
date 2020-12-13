default_header_size = 10


def read_msg(connection, header_size: int = default_header_size, size_pack=1024):
    # try:
        data = connection.recv(header_size)

        if not data:
            return False

        size_msg = int(data.decode())
        print(size_msg)
        msg = ''

        while True:
            if size_msg <= size_pack:
                data = connection.recv(size_msg).decode()
                if not data:
                    print("nope")
                    return False
                msg += data
                break

            data = connection.recv(size_pack).decode()

            if not data:
                return False

            size_msg -= size_pack
            msg += data
        return msg
    # except Exception:
    #     return False


def send_msg(connection, msg: str, header_size: int = default_header_size) -> bool:
    # try:
        size_msg = f'{len(msg):{header_size}}'
        if connection.send(size_msg.encode()) <= 0:
            return False
        if connection.send(msg.encode()) <= 0:
            return False
        return True
    # except Exception:
    #     return False
