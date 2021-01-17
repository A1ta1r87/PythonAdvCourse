from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
import re
from jinja2 import Environment, FileSystemLoader, select_autoescape
from library import Library
from book import Book
from reader import Reader
from datetime import date, timedelta

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'very secret key'

login_manager = LoginManager(app)
login_manager.login_view = 'auth'

# Создаем библиотеку
lib = Library()

if not lib['Books']:
    with open('books.txt', encoding='utf-8') as f:
        for line in f:
            book = line.rstrip('\n').split(',')
            title, author, year = book[0], book[1], book[2]
            lib.add_book(Book(title, author, year))

e = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html'])
)


def get_sort_books(request, books):
    """
    Отсортировать книги по заданному условию, если в запросе есть параметр 'sort'.
    Args:
        request: переменные запроса в виде словаря;
                условия сортировки, переданные в параметре 'sort': 'id' - по номеру
                                                                   'title' - по названию
                                                                   'author' - по имени автора
                                                                   'year' - по году издания
        books: книги, кот-ые необходимо отсортировать
    Returns:
        отсортированный словарь книг, либо False в случае неверно указанных параметров
    """
    if 'sort' in request:
        condition = request['sort']
        if condition and condition in ('id', 'title', 'author', 'year'):
            return dict(sorted(books.items(), key=lambda item: item[1].id if condition == 'id' else
            (item[1].title if condition == 'title' else
             (item[1].author if condition == 'author' else
              item[1].year))))
    return False


def check_email(email: str):
    """
    Проверить 'email' на валидность
    Args:
        email: строка с адресом электронной почты
    Returns:
        'True', если переданный адрес соответствует шаблону, в противном случае - 'False'
    """
    email_template = r'\w+[\._]?\w+@\w+\.\w{2,3}$'
    if re.match(email_template, email):
        return True
    return False


@app.route('/books', methods=['POST', 'GET'])
def api_get_books():
    """
    Вывести все книги в библиотеке.
    Если передан поисковый запрос через форму на сайте или адресную строку ('book_search') -
    перенаправить в функцию обработки поисковых запросов, с переданным значением параметра 'book_search'.
    Иначе, визуализировать страницу шаблона 'books.html', с переменными 'path' - для формирования адреса
    ссылок при сортировке значений, и 'books' - словаря объектов класса 'Book', неупорядоченных, либо отсортированных,
    при наличии такого запроса.
    Returns:
        визуализированную html страницу
    """
    books = lib.get_all_books()
    if request.method == 'POST':
        if 'book_search' in request.form:
            return redirect(url_for("api_search_book", book_search=request.form.get('book_search')))
    elif request.method == 'GET':
        if 'book_search' in request.args:
            return redirect(url_for("api_search_book", book_search=request.args.get('book_search')))
        sort_books = get_sort_books(request.args, books)
        if sort_books:
            books = sort_books
    return render_template('books.html', path='books', books=books)


@app.route('/given_books', methods=['POST', 'GET'])
def api_get_given_books():
    """ Визуализировать html страницу со  всеми книгами, отданными читателям."""
    books = lib.get_given_books()
    if request.method == 'POST':
        if 'book_search' in request.form:
            return redirect(url_for("api_search_book", book_search=request.form.get('book_search')))
    elif request.method == 'GET':
        if 'book_search' in request.args:
            return redirect(url_for("api_search_book", book_search=request.args.get('book_search')))
        sort_books = get_sort_books(request.args, books)
        if sort_books:
            books = sort_books
    return render_template('books.html', path='/given_books', books=books)


@app.route('/available_books', methods=['POST', 'GET'])
def api_get_available_books():
    """ Визуализировать html страницу со  всеми доступными книгами библиотеки."""
    books = lib.get_available_books()
    if request.method == 'POST':
        if 'book_search' in request.form:
            return redirect(url_for("api_search_book", book_search=request.form.get('book_search')))
    elif request.method == 'GET':
        if 'book_search' in request.args:
            return redirect(url_for("api_search_book", book_search=request.args.get('book_search')))
        sort_books = get_sort_books(request.args, books)
        if sort_books:
            books = sort_books
    return render_template('books.html', path='/available_books', books=books)


@app.route('/search_book', methods=['POST', 'GET'])
def api_search_book(book_search: str = None):
    """
    Вывести страницу с результатами поиска.
    Данные для поиска: 'POST', 'GET' запросы, а также необязательный параметр 'book_search',
    в котором передается значение из строки поиска, если данный запрос был сделан на других страницах сайта.
    В случае наличия параметра сортировки, результат сортируется по условию.
    Args:
        book_search: строка со значением для поиска (по умолчанию 'None')
    Returns:
        Отрисованный шаблон страницы 'search_book.html' с переменными 'path' для формирования адреса
        ссылок при сортировке значений, и 'books' - словаря объектов класса 'Book'.
        Если поисковых запросов не найдено - перенаправить на домашнюю страницу.
    """
    if request.method == 'POST' or book_search:
        if 'book_search' in request.form or book_search:
            if not book_search:
                book_search = request.form['book_search']
            books = lib.search_in_library(book_search)
            if books:
                message = 'Результаты поиска:'
                sort_books = get_sort_books(request.args, books)
                if sort_books:
                    books = sort_books
            else:
                message = 'К сожалению, ничего не найдено'
            path = f'/search_book?book_search={book_search}'
            return render_template('search_book.html', path=path, message=message, books=books)

    elif request.method == 'GET':
        print('Get')
        if 'book_search' in request.args:
            book_search = request.args['book_search']
            books = lib.search_in_library(book_search)
            if books:
                message = 'Результаты поиска:'
                sort_books = get_sort_books(request.args, books)
                if sort_books:
                    books = sort_books
            else:
                message = 'К сожалению, ничего не найдено'
            path = f'/search_book?book_search={book_search}'
            return render_template('search_book.html', path=path, message=message, books=books)
    return redirect(url_for('home_page'))


@app.route('/delete_book', methods=['POST', 'GET'])
@login_required
def api_delete_book():
    message = ''
    books = lib.get_all_books()
    if request.method == 'POST':
        if 'book_search' in request.form:
            return redirect(url_for("api_search_book", book_search=request.form.get('book_search')))
        if 'id' not in request.form:
            message = 'Данные указаны неверно'
        else:
            id = request.form['id']
            message = lib.delete_book(int(id))
    elif request.method == 'GET':
        if 'book_search' in request.args:
            return redirect(url_for("api_search_book", book_search=request.args.get('book_search')))
        if 'id' in request.args:
            id = request.args['id']
            if id.isnumeric():
                message = lib.delete_book(int(id))
    return render_template('delete_book.html', message=message, books=books)


@app.route('/add_book', methods=['POST', 'GET'])
@login_required
def api_add_book():
    message = ''
    if request.method == 'POST':
        if 'book_search' in request.form:
            return redirect(url_for("api_search_book", book_search=request.form.get('book_search')))
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']
        if not (title and author and year and year.isnumeric()):
            message = 'Данные указаны неверно'
        else:
            message = lib.add_book(Book(title=title, author=author, year=int(year)))
    elif request.method == 'GET':
        if 'book_search' in request.args:
            return redirect(url_for("api_search_book", book_search=request.args.get('book_search')))
        if 'title' in request.args and 'author' in request.args and 'year' in request.args:
            title = request.args['title']
            author = request.args['author']
            year = request.args['year']
            if title and author and year and year.isnumeric():
                message = lib.add_book(Book(title=title, author=author, year=year))
    return render_template('add_book.html', message=message)


@app.route('/take_book', methods=['POST', 'GET'])
@login_required
def api_take_book():
    user_id = int(current_user.get_id())
    message = ''
    if request.method == 'POST':
        if 'book_search' in request.form:
            return redirect(url_for("api_search_book", book_search=request.form.get('book_search')))
        if not ('book_id' in request.form):
            message = 'Данные указаны неверно'
        else:
            book_id = request.form['book_id']
            if not book_id.isnumeric():
                message = 'Данные указаны неверно'
            else:
                message = lib.give_book(reader_id=user_id, book_id=int(book_id))
    elif request.method == 'GET':
        if 'book_search' in request.args:
            return redirect(url_for("api_search_book", book_search=request.args.get('book_search')))
        if 'book_id' in request.args:
            book_id = request.args['book_id']
            if book_id.isnumeric():
                message = lib.give_book(reader_id=user_id, book_id=int(book_id))
    return render_template('take_book.html', message=message, books=lib.get_available_books())


@app.route('/return_book', methods=['POST', 'GET'])
@login_required
def api_return_book():
    user_id = int(current_user.get_id())
    message = ''
    if request.method == 'POST':
        if 'book_search' in request.form:
            return redirect(url_for("api_search_book", book_search=request.form.get('book_search')))
        if not 'book_id' in request.form:
            message = 'Данные указаны неверно'
        else:
            book_id = request.form['book_id']
            if not book_id.isnumeric():
                message = 'Данные указаны неверно'
            else:
                message = lib.return_book(reader_id=user_id, book_id=int(book_id))
    elif request.method == 'GET':
        if 'book_search' in request.args:
            return redirect(url_for("api_search_book", book_search=request.args.get('book_search')))
        if 'book_id' in request.args:
            book_id = request.args['book_id']
            if book_id.isnumeric():
                message = lib.return_book(reader_id=int(current_user.get_id()), book_id=int(book_id))
    return render_template('return_book.html', message=message, books=lib.get_given_books_to_reader(user_id))


@app.route('/index', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def home_page():
    if request.method == 'POST':
        if 'book_search' in request.form:
            return redirect(url_for("api_search_book", book_search=request.form.get('book_search')))
    elif request.method == 'GET':
        if 'book_search' in request.args:
            return redirect(url_for("api_search_book", book_search=request.args.get('book_search')))
    return render_template('index.html')


@login_manager.user_loader
def load_user(user_id):
    return lib['Readers'][int(user_id)]


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    message = ''
    if request.method == 'POST':
        if 'book_search' in request.form:
            return redirect(url_for("api_search_book", book_search=request.form.get('book_search')))
        email = request.form.get('email')
        password = request.form.get('password')
        next_url = request.args.get('next')

        if email and password:
            reader = lib.check_email_exists(email)
            if reader and reader.check_psw(password):
                login_user(reader)
                if next_url:
                    return redirect(next_url)
                return redirect(url_for("home_page"))
            else:
                message = "Введены неверные данные"
    elif request.method == 'GET':
        if 'book_search' in request.args:
            return redirect(url_for("api_search_book", book_search=request.args.get('book_search')))
    return render_template('auth.html', message=message)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home_page'))


@app.route('/register', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    errors = []
    if request.method == 'POST':
        if 'book_search' in request.form:
            return redirect(url_for("api_search_book", book_search=request.form.get('book_search')))
        email = request.form.get('email')
        password = request.form.get('password')
        repassword = request.form.get('repassword')
        name = request.form.get('name')
        surname = request.form.get('surname')
        birth_date = request.form.get('birth_date')
        if not (email and password and repassword and name and surname and birth_date):
            errors.append('Введены не все данные.')
        if not check_email(email):
            errors.append('Введен некорректный email.')
        if lib.check_email_exists(email) is not None:
            errors.append('Пользователь с таким email уже зарегестрирован')
        if password != repassword:
            errors.append('Пароли не совпадают')
        if not errors:
            message = lib.add_reader(Reader(name, surname, email, password, birth_date))
            if message:
                flash(message)
                return redirect(url_for('auth'))
    elif request.method == 'GET':
        if 'book_search' in request.args:
            return redirect(url_for("api_search_book", book_search=request.args.get('book_search')))
    max_date = date.today() - timedelta(days=3650)  # возрастной порог при регистрации (не младше 10 лет)
    return render_template('register.html', message=errors, max_date=max_date, data=request.form)


if __name__ == "__main__":
    app.run()