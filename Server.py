import socket
import msg

sizePacket = 5

sock = socket.socket()
sock.bind(('', 1234))
i = 3
while i > 0:
    sock.listen(2)
    conn, address = sock.accept()
    if conn:
        try:
            msg.send_msg(conn, 'What do u want?')
            answer = msg.read_msg(conn)
            if answer:
                print(answer)
            conn.close()
        except ValueError:
            print("Value problems")
        finally:
            i -= 1
