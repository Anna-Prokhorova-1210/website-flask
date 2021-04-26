from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from data.users import User
from data.books import Book
from data import db_session
from forms.user import RegisterForm
from forms.user import StudentLoginForm
from forms.booksForm import BooksForm
from flask_login import LoginManager, login_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/', methods=['GET', 'POST'])
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('index.html', form=form, message="Пароли не совпадают!")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('index.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            letter=form.letter.data,
            is_teacher=False,
            email=form.email.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        login_user(user)
        return redirect('/main-user-menu')
    return render_template('index.html', form=form)


@app.route('/student-login', methods=['GET', 'POST'])
def student_login():
    form = StudentLoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/main-user-menu")
        return render_template('student-login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('student-login.html', form=form)


@app.route('/main-user-menu', methods=['GET', 'POST'])
def main_user_menu():
    return render_template('main-user-menu.html')


@app.route('/add-book', methods=['GET', 'POST'])
def add_book():
    form = BooksForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        book = Book(
            title=form.title.data,
            letter=form.letter.data,)
        db_sess.add(book)
        db_sess.commit()
        return redirect('/add-book')
    return render_template('add-book.html', form=form)

@app.route('/view-books')
def view_books():
    db_sess = db_session.create_session()
    books = db_sess.query(Book)
    print(type(books))
    for item in books:
        print(item.title)
        print(item.letter)
    return render_template("view-books.html", books=books)


@app.route('/view-students')
def view_students():
    db_sess = db_session.create_session()
    users = db_sess.query(User)
    return render_template("view-students.html", users=users)


@app.route('/get-books', methods=['POST', 'GET'])
def get_books():
    if request.method == 'POST':
        db_sess = db_session.create_session()
        for key in request.form:
            for book in db_sess.query(Book).filter(Book.id == request.form[key]):
                for user in db_sess.query(User).filter(User.id == current_user.get_id()):
                    user.books.append(book)
        db_sess.commit()
        return redirect('/main-user-menu')
    db_sess = db_session.create_session()
    for user in db_sess.query(User).filter(User.id == current_user.get_id()):
        books = db_sess.query(Book).filter((Book.letter == user.letter) | (Book.letter == 'Общая'))
    return render_template("get-books.html", books=books)


@app.route('/check-statistics/<int:class_id>')
def check_statistics(class_id=99):
    students = list()
    if class_id == 100:
        db_sess = db_session.create_session()
        students = db_sess.query(User).filter(User.letter == 'А', User.is_teacher.is_(False))
    if class_id == 101:
        db_sess = db_session.create_session()
        students = db_sess.query(User).filter(User.letter == 'Б', User.is_teacher.is_(False))
    if class_id == 102:
        db_sess = db_session.create_session()
        students = db_sess.query(User).filter(User.letter == 'В', User.is_teacher.is_(False))
    if class_id == 103:
        db_sess = db_session.create_session()
        students = db_sess.query(User).filter(User.letter == 'Г', User.is_teacher.is_(False))
    return render_template('check-statistics.html', class_id=class_id, students=students)


@app.route('/personal-account')
def personal_account():
    db_sess = db_session.create_session()
    for student in db_sess.query(User).filter(User.id == current_user.get_id()):
        user = student
    return render_template('personal-account.html', user=user)


@app.route('/return-books', methods=['GET', 'POST'])
def return_books():
    if request.method == 'POST':
        db_sess = db_session.create_session()
        for key in request.form:
            for book in db_sess.query(Book).filter(Book.id == request.form[key]):
                for user in db_sess.query(User).filter(User.id == current_user.get_id()):
                    user.books.remove(book)
        db_sess.commit()
        return redirect('/main-user-menu')
    else:
        db_sess = db_session.create_session()
        for student in db_sess.query(User).filter(User.id == current_user.get_id()):
            user = student
        if len(user.books) != 0:
            need_to_return = True
        else:
            need_to_return = False
        return render_template('return-books.html', user=user, need_to_return=need_to_return)


if __name__ == "__main__":
    db_session.global_init("db/users.db")
    app.run(port=8080, host="127.0.0.1")

