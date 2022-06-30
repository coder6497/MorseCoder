from flask import Flask, render_template
from code_files.forms import EncryptForm
from code_files.morse_coder import MorseCoder


app = Flask(__name__)
app.config["SECRET_KEY"] = 'povsekakiy_bogdanov'


@app.route('/', methods=["GET", "POST"])
def main():
    form = EncryptForm()
    n_word = ''
    if form.validate_on_submit():
        coder = MorseCoder(form.word.data)
        if form.select.data == "Закодировать":
            n_word = coder.to_morse()
        if form.select.data == "Раскодировать":
            n_word = coder.to_normal()
    return render_template("main.html", form=form, n_word=n_word)


if __name__ == "__main__":
    app.run(debug=True)
