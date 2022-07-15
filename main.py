import json
from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from wtforms import StringField, SubmitField, SelectField, PasswordField, BooleanField
from wtforms.validators import DataRequired, EqualTo
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


class MorseEncryptor:
    def __init__(self, user_input):
        with open("morse_code.json", "r", encoding="utf-8") as f:
            self.morse = json.load(f)
        self.words = user_input.split(' ')
        self.language = ''
        self.words_l = list(map(list, self.words))

    def to_morse(self):
        for k, v in self.morse[self.language].items():
            for i in range(len(self.words_l)):
                for j in range(len(self.words_l[i])):
                    if self.words_l[i][j] == k or self.words_l[i][j] == k.lower():
                        self.words_l[i][j] = v
        return ' '.join(list(map(lambda x: ' '.join(x), self.words_l)))

    def to_normal(self):
        for k, v in self.morse[self.language].items():
            for i in range(len(self.words)):
                if self.words[i] == v:
                    self.words[i] = k
        return ' '.join(self.words)


app = Flask(__name__)
app.config["SECRET_KEY"] = 'povsekakiy_bogdanov'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///crypt_base.db"
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'


@app.route('/', methods=["GET", "POST"])
def main():
    return render_template("main.html")


@app.route('/encrypt', methods=["GET", "POST"])
@login_required
def encryptor():
    n_word = ''
    form = EncryptForm()
    if form.validate_on_submit():
        coder = MorseEncryptor(form.word.data)
        coder.language = form.language.data
        if form.select.data == "Закодировать":
            n_word = coder.to_morse()
        if form.select.data == "Раскодировать":
            n_word = coder.to_normal()
        encrypt = Encrypts(first=form.word.data, last=n_word, user_id=current_user.id)
        db.session.add(encrypt)
        db.session.commit()
    return render_template("encryptor.html", form=form, n_word=n_word)


@app.route('/dict')
def crypt_dict():
    coder = MorseEncryptor('')
    return render_template('crypt.html', morse=coder.morse)


@login.user_loader
def load_user(id):
    return Users.query.get(id)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    user = Users().query.filter_by(username=form.username.data).first()
    if user and user.check_password(form.password.data):
        login_user(user, remember=form.remember.data)
        return redirect('/')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/regist', methods=['GET', "POST"])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(username=form.username.data, email=form.email.data, phone=form.phone.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect('/')
    return render_template('registration.html', form=form)


@app.route('/encrypts/')
@login_required
def encrypts():
    return render_template('encrypts.html', user=current_user)


@app.route('/delete_encrypt/<int:id>')
@login_required
def delete_encrypt(id):
    encrypt = Encrypts.query.filter_by(id=id).first()
    db.session.delete(encrypt)
    db.session.commit()
    return redirect('/encrypts')


@app.route('/about_user')
@login_required
def about_user():
    about = {}
    about["Имя пользователя"] = current_user.username
    about["Email"] = current_user.email
    about["Номер телефона"] = current_user.phone
    return render_template('about.html', user=current_user, about=about)


@app.route('/about_app')
def about_app():
    return render_template('about_app.html')


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    email = db.Column(db.String())
    phone = db.Column(db.String())
    password_hash = db.Column(db.String())
    encrypts = db.relationship('Encrypts')

    def __repr__(self):
        return f'<Users {self.id}r>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Encrypts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String())
    last = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))


class EncryptForm(FlaskForm):
    word = StringField("Введите слово", validators=[DataRequired()])
    select = SelectField("Выберите режим", choices=['Закодировать', "Раскодировать"])
    language = SelectField("Выберите язык", choices=["Русский", "English", "Цифры"])
    submit = SubmitField("Готово")


class LoginForm(FlaskForm):
    username = StringField("Логин", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    remember = BooleanField("Запомнить")
    submit = SubmitField("Войти")


class RegistrationForm(FlaskForm):
    username = StringField("Логин", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    phone = StringField("Номер телефона", validators=[DataRequired()])
    repeat_password = PasswordField("Повторите пароль", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Зарегистрироваться")


if __name__ == "__main__":
    app.run(debug=True)
