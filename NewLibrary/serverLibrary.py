import socket
import msg
import library2


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
                    message = 'Bye'
                elif answer == 'all':
                    message = library2.national_library.show_all_books()
                elif answer == 'given':
                    message = library2.national_library.show_given_books()
                elif answer == 'available':
                    message = library2.national_library.show_available_books()
                elif answer == 'sort':
                    message = library2.national_library.sort_books()
                else:
                    message = 'hrrrr'
                msg.send_msg(conn, message)
            conn.close()
        except ValueError:
            print("Value problems")
        finally:
            i -= 1
