from flask import Flask, request, render_template
from models import db, User
from flask_wtf import CSRFProtect
from forms import Registration

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///homework_3.db'
app.config['SECRET_KEY'] = '1b34f46e88e5fdfc80890aae026eb318b26526754125a17dbee9678019ff4a2c'
csrf = CSRFProtect(app)
db.init_app(app)


@app.cli.command("init-db")
def init_db():
    db.create_all()


@app.route('/registration/', methods=['POST', 'GET'])
def register():
    form = Registration()
    if request.method == 'POST' and form.validate():
        name = form.name.data
        surname = form.surname.data
        email = form.email.data
        password = form.password.data
        existing_user = User.query.filter(User.email == email).first()
        if existing_user:
            message = 'This email is existing'
            form.email.errors.append(message)
            return render_template('index.html', form=form)
        new_user = User(name=name, surname=surname, email=email, password=password)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return '<h1>Registration successful!</h1>'
    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)