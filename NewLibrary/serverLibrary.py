import socket
import msg



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
                if answer == 'exit':
                    msg.send_msg(conn, 'Bye')
                elif answer == 'show all books':
                    msg.send_msg(conn, ClassLibraryNew.show_all_books(national_library))
            conn.close()
        except ValueError:
            print("Value problems")
        finally:
            i -= 1
