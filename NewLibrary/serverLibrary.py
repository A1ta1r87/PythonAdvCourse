import socket
import threading
import msg
import library2

class MyThread(threading.Thread):

    def __init__(self, conn, addr):
        super().__init__()
        self.conn = conn
        self.addr = addr

    def run(self):
        while True:
            try:
                greeting_message = 'Hello, this is library server. What do u want to do? (Type "info" for help)'
                help_message = 'Server supported next command (without quotes): \n' \
                               '"all" - shows all books in library \n' \
                               '"given" - shows given to readers books \n' \
                               '"available" - shows available books in library \n' \
                               '"sortT" - shows sorted books by title \n' \
                               '"sortA" - shows sorted books by author \n' \
                               '"sortY" shows sorted books by year. \n'
                msg.send_msg(self.conn, greeting_message)
                answer = msg.read_msg(self.conn)
                if answer:
                    if answer == 'exit':
                        msg.send_msg(self.conn, 'Bye')
                        print("Disconnected", self.addr)
                        break
                    elif answer == 'info':
                        message = help_message
                    elif answer == 'all':
                        message = library2.national_library.show_all_books()
                    elif answer == 'given':
                        message = library2.national_library.show_given_books()
                    elif answer == 'available':
                        message = library2.national_library.show_available_books()
                    elif answer[:-1] == 'sort':
                        condition = answer[-1]
                        if condition in ('T', 'A', 'Y'):
                            parameter = 'title' if condition == 'T' else ('author' if condition == 'A' else 'year')
                            message = library2.national_library.sort_books(parameter)
                        else:
                            message = 'incorrect parameter'
                    else:
                        message = 'unknown command'
                    msg.send_msg(self.conn, message)
            except ValueError:
                print("Value problems")
        conn.close()


if __name__ == "__main__":

    sock = socket.socket()
    sock.bind(('', 1234))
    while True:
        sock.listen(5)
        conn, address = sock.accept()
        my_thread = MyThread(conn, address)
        my_thread.start()
        print("Connected", address)


