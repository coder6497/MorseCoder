from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField, BooleanField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import json


class MorseCoder:
    def __init__(self, user_input):
        with open("morse_code.json", "r", encoding="utf-8") as f:
            self.morse = json.load(f)
        self.words = user_input.split(' ')
        self.words_l = list(map(list, self.words))

    def to_morse(self):
        for k, v in self.morse.items():
            for i in range(len(self.words_l)):
                for j in range(len(self.words_l[i])):
                    if self.words_l[i][j] == k or self.words_l[i][j] == k.lower():
                        self.words_l[i][j] = v
        return ' '.join(list(map(lambda x: ' '.join(x), self.words_l)))

    def to_normal(self):
        for k, v in self.morse.items():
            for i in range(len(self.words)):
                if self.words[i] == v:
                    self.words[i] = k
        return ' '.join(self.words)


app = Flask(__name__)
app.config["SECRET_KEY"] = 'povsekakiy_bogdanov'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///crypt_base.db"
db = SQLAlchemy(app)


@app.route('/', methods=["GET", "POST"])
def main():
    return render_template("main.html")


@app.route('/encrypt', methods=["GET", "POST"])
def encryptor():
    n_word = ''
    form = EncryptForm()
    if form.validate_on_submit():
        coder = MorseCoder(form.word.data)
        if form.select.data == "Закодировать":
            n_word = coder.to_morse()
        if form.select.data == "Раскодировать":
            n_word = coder.to_normal()
    return render_template("encryptor.html", form=form, n_word=n_word)


@app.route('/dict')
def crypt_dict():
    coder = MorseCoder('')
    return render_template('crypt.html', morse=coder.morse)


@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', form=form)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    email = db.Column(db.String())
    password = db.Column(db.String())

    def __repr__(self):
        return f'<Users {self.id}r>'


class EncryptForm(FlaskForm):
    word = StringField("Введите слово", validators=[DataRequired()])
    select = SelectField("Выберите режим", choices=['Закодировать', "Раскодировать"])
    submit = SubmitField("Готово")


class LoginForm(FlaskForm):
    username = StringField("Логин", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    remember = BooleanField("Запомнить")
    submit = SubmitField("Войти")


if __name__ == "__main__":
    app.run(debug=True)
