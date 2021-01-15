from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_required, login_user, current_user, logout_user

from jinja2 import Environment, FileSystemLoader, select_autoescape
from library import Library
from book import Book
from reader import Reader

app = Flask(__name__)
app.config['DEBUG'] = True

# Создаем библиотеку
lib = Library()

if not lib['Books']:
    with open('books.txt', encoding='utf-8') as f:
        for line in f:
            book = line.rstrip('\n').split(',')
            title, author, year = book[0], book[1], book[2]
            lib.add_book(Book(title, author, year))


# if not lib['Readers']:
#     lib.add_reader(Reader('Andrii', 'Yaresko', 1994))
#     lib.add_reader(Reader('Ivan', 'Nochovkin', 2002))
#     lib.add_reader(Reader('Igor', 'Kudrya', 1974))
#     lib.add_reader(Reader('Alex', 'Popyuk', 1987))
#     lib.add_reader(Reader('Max', 'Polyakov', 1997))

e = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html'])
)


def is_number(x):
    """
    Вернуть True, если переданный элемент является числом
    или может быть преобразован в число (например число в виде строки)
    """
    try:
        int(x)
        return True
    except ValueError:
        return False


def get_sort_books(request, needed_books='all'):
    """
    Отсортировать книги, если в запросе есть параметр 'sort'.
    :param request: словарь, содержащий аргументы запроса
    :param needed_books: книги, кот-ые необходимо отсортировать: 'all' - все книги библиотеки (по умолчанию)
                                                                 'given' - выданные книги
                                                                 'available' - доступные книги
    :return: отсортированный словарь книг
    """
    if 'sort' in request:
        condition = request['sort']
        if condition:
            books = lib.sort_books(condition=condition, needed_books=needed_books)
            return books
    return False


@app.route('/books', methods=['GET'])
def api_get_books():
    sort_books = get_sort_books(request.args, 'all')
    if sort_books:
        return render_template('books.html', books=sort_books)
    return render_template('books.html', path='books', books=lib.get_all_books())


@app.route('/given_books', methods=['GET'])
def api_get_given_books():
    sort_books = get_sort_books(request.args, 'given')
    if sort_books:
        return render_template('books.html', books=sort_books)
    return render_template('books.html', path='/given_books', books=lib.get_given_books())


@app.route('/available_books', methods=['GET'])
def api_get_available_books():
    sort_books = get_sort_books(request.args, 'available')
    if sort_books:
        return render_template('books.html', books=sort_books)
    return render_template('books.html', path='/available_books', books=lib.get_available_books())


@app.route('/delete_book', methods=['POST', 'GET'])
def api_delete_book():
    message = ''
    if request.method == 'POST':
        if 'id' not in request.form:
            message = 'Данные указаны неверно'
        else:
            id = request.form['id']
            message = lib.delete_book(int(id))
    elif request.method == 'GET':
        if 'id' in request.args:
            id = request.args['id']
            if is_number(id):
                message = lib.delete_book(int(id))
    return render_template('delete_book.html', message=message, books=lib.get_all_books())


@app.route('/add_book', methods=['POST', 'GET'])
def api_add_book():
    message = ''
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']
        if not (title and author and year and is_number(year)):
            message = 'Данные указаны неверно'
        else:
            message = lib.add_book(Book(title=title, author=author, year=int(year)))
    elif request.method == 'GET':
        if 'title' in request.args and 'author' in request.args and 'year' in request.args:
            title = request.args['title']
            author = request.args['author']
            year = request.args['year']
            if title and author and year and is_number(year):
                message = lib.add_book(Book(title=title, author=author, year=year))
    return render_template('add_book.html', message=message)


@app.route('/take_book', methods=['POST', 'GET'])
def api_give_book():
    message = ''
    if request.method == 'POST':
        if not ('book_id' in request.form and 'reader_id' in request.form):
            message = 'Данные указаны неверно'
        else:
            book_id = request.form['book_id']
            reader_id = request.form['reader_id']
            if not (book_id and reader_id and is_number(book_id) and is_number(reader_id)):
                message = 'Данные указаны неверно'
            else:
                message = lib.give_book(reader_id=int(reader_id), book_id=int(book_id))
    elif request.method == 'GET':
        if 'reader_id' in request.args and 'book_id' in request.args:
            book_id = request.args['book_id']
            reader_id = request.args['reader_id']
            if is_number(book_id) and is_number(reader_id):
                message = lib.give_book(reader_id=int(reader_id), book_id=int(book_id))
    return render_template('take_book.html', message=message, books=lib.get_available_books())


@app.route('/return_book', methods=['POST', 'GET'])
def api_return_book():
    message = ''
    if request.method == 'POST':
        if not ('book_id' in request.form and 'reader_id' in request.form):
            message = 'Данные указаны неверно'
        else:
            book_id = request.form['book_id']
            reader_id = request.form['reader_id']
            if not (book_id and reader_id and is_number(book_id) and is_number(reader_id)):
                message = 'Данные указаны неверно'
            else:
                message = lib.return_book(reader_id=int(reader_id), book_id=int(book_id))
    elif request.method == 'GET':
        if 'reader_id' in request.args and 'book_id' in request.args:
            book_id = request.args['book_id']
            reader_id = request.args['reader_id']
            if is_number(book_id) and is_number(reader_id):
                message = lib.return_book(reader_id=int(reader_id), book_id=int(book_id))
    return render_template('return_book.html', message=message, books=lib.get_given_books())


@app.route('/index')
@app.route('/')
def home_page():
    return render_template('index.html')


if __name__ == "__main__":
    # app.run()
    pass

