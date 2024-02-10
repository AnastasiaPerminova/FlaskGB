from flask import Flask, render_template, url_for, request
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegistrationForm
from models import db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db.init_app(app)
migrate = Migrate(app, db)

app.config[
    'SECRET_KEY'] = b'b0ee5a2c6515091072087d57c6693be951cd9fc4629e5e66324c8c33331b5768'
csrf = CSRFProtect(app)


@app.context_processor
def menu_items():
    menu_items = [
        {'name': 'Домой', 'url': url_for("index")},
        {'name': 'Регистрация', 'url': url_for("registration")},
        {'name': 'Все пользователи', 'url': url_for("all_users")}

    ]
    return dict(menu_items=menu_items)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/all_users/')
def all_users():
    all_users = User.query.order_by(-User.id).all()
    return render_template('all_users.html', users=all_users)


@app.route('/registration/', methods=['GET', 'POST'])
def registration():
    context = {'alert_message': "Добро пожаловать!"}
    form = RegistrationForm()
    username = form.username.data
    usersurname = form.usersurname.data
    email = form.email.data
    password = form.password.data

    if request.method == 'POST' and form.validate():
        if User.query.filter(User.username == username).all() or \
                User.query.filter(User.email == email).all():
            context = {'alert_message': "Пользователь уже существует!"}
            return render_template('registration.html', form=form, **context)
        else:

            new_user = User(username=username, usersurname=usersurname, email=email,
                            password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            return render_template('registration.html', form=form, **context)
    return render_template('registration.html', form=form)
