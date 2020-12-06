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
        i = 3
        while i > 0:
            try:
                msg.send_msg(self.conn, 'What do u want?')
                answer = msg.read_msg(self.conn)
                if answer:
                    if answer == 'exit':
                        msg.send_msg(self.conn, 'Bye')
                        print("Disconnected", self.addr)
                        break
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
                        message = 'hrrrr'
                    msg.send_msg(self.conn, message)
            except ValueError:
                print("Value problems")
            finally:
                i -= 1
                conn.close()


if __name__ == "__main__":

    sock = socket.socket()
    sock.bind(('', 1234))
    i = 5
    while i > 0:
        sock.listen(2)
        conn, address = sock.accept()
        my_thread = MyThread(conn, address)
        my_thread.start()
        print("Connected", address)
        i -= 1

