import socket
import msg

sizePacket = 5

sock = socket.socket()
sock.bind(('', 1234))
i = 3
while i > 0:
    sock.listen(2)
    conn, address = sock.accept()
    try:
        data = msg.read_msg(conn, sizePacket)
        if data:
            new_data = data.upper()
            msg.send_msg(conn, new_data)
        conn.close()
    except ValueError:
        print("Value problems")
    finally:
        i -= 1
