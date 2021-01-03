import socket
import threading
import msg
import library


class MyThread(threading.Thread):

    def __init__(self, conn, addr):
        super().__init__()
        self.conn = conn
        self.addr = addr

    def run(self):
        # commands = {'info': ('Server supported next command (without quotes): \n'
        #                      '"all" - shows all books in library \n'
        #                      '"given" - shows given to readers books \n'
        #                      '"available" - shows available books in library \n'
        #                      '"sortT" - shows sorted books by title \n'
        #                      '"sortA" - shows sorted books by author \n'
        #                      '"sortY" shows sorted books by year. \n'),
        #             'all': library2.national_library.show_all_books(),
        #             'given': library2.national_library.show_given_books(),
        #             'available': library2.national_library.show_available_books()}

        greeting_message = 'Hello, this is library server. What do u want to do? (Type "info" for help)'
        help_message = 'Server supported next command (without quotes): \n' \
                       '"all" shows all books in library \n' \
                       '"given" shows given to readers books \n' \
                       '"available" shows available books in library \n' \
                       '"sortT" shows sorted books by title \n' \
                       '"sortA" shows sorted books by author \n' \
                       '"sortY" shows sorted books by year \n' \
                       '"exit" for escape. \n'
        reader_id = None

        try:
            msg.send_msg(self.conn, greeting_message)
            while True:
                client_msg = msg.read_msg(self.conn)
                if not client_msg:
                    break
                else:
                    if client_msg == 'exit':
                        msg.send_msg(self.conn, 'Bye')
                        print("Disconnected", self.addr)
                        break
                    elif client_msg == 'info':
                        message = help_message
                    elif client_msg == 'all':
                        message = library.national_library.show_all_books()
                    elif client_msg == 'given':
                        message = library.national_library.show_given_books()
                    elif client_msg == 'available':
                        message = library.national_library.show_available_books()
                    elif client_msg[:-1] == 'sort':
                        condition = client_msg[-1]
                        if condition in ('T', 'A', 'Y'):
                            parameter = 'title' if condition == 'T' else ('author' if condition == 'A' else 'year')
                            message = library.national_library.sort_books(parameter)
                        else:
                            message = 'incorrect parameter'
                    elif client_msg == 'take' or client_msg == 'return':
                        if not reader_id:
                            msg.send_msg(self.conn, 'What`s ur reader id?')
                            reader_id = int(msg.read_msg(self.conn))
                        if reader_id in library.national_library['Readers'].keys():
                            reader_name = library.national_library['Readers'][reader_id][0]
                            if client_msg == 'take':
                                msg.send_msg(self.conn, f'Hello, {reader_name}! What book r u looking for?')
                            else:
                                msg.send_msg(self.conn, f'Hello, {reader_name}! What book do u want to return?')
                            book_id = int(msg.read_msg(self.conn))
                            if book_id in library.national_library['Books'].keys():
                                book = ', '.join(library.national_library['Books'][book_id][:2])
                                if client_msg == 'return':
                                    taken_books = library.national_library['Debtors'][reader_id][2]
                                    if book_id in taken_books:
                                        message = f'Thx, u successfully return the {book}'
                                        library.national_library.return_book(reader_id, book_id)
                                    else:
                                        message = 'There is no such book in your list'
                                else:
                                    if book_id in library.national_library['Given books'].keys():
                                        message = 'Sorry, this book was given to another reader'
                                    else:
                                        message = f'You have taken the {book}.'
                                        library.national_library.give_out_book(reader_id, book_id)
                            else:
                                message = 'This book is not in our library.'
                        else:
                            message = "There is no reader with such id."
                    else:
                        message = 'unknown command'
                    msg.send_msg(self.conn, message)
            conn.close()
        except ValueError:
            print("Value problems")


if __name__ == "__main__":

    sock = socket.socket()
    sock.bind(('', 1234))
    while True:
        sock.listen(5)
        conn, address = sock.accept()
        my_thread = MyThread(conn, address)
        my_thread.start()
        print("Connected", address)
