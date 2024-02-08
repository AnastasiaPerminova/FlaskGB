from pathlib import PurePath, Path
from re import split

from flask import Flask, render_template, request, redirect, url_for, flash, session

from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = b'b0ee5a2c6515091072087d57c6693be951cd9fc4629e5e66324c8c33331b5768'


@app.context_processor
def menu_items():
    menu_items = [
        {'name': 'Home', 'url': url_for("index")},
        {'name': 'Task 1', 'url': url_for("task_1")},
        {'name': 'Task 2', 'url': url_for("task_2")},
        {'name': 'Task 3', 'url': url_for("task_3")},
        {'name': 'Task 4', 'url': url_for("task_4")},
        {'name': 'Task 5', 'url': url_for("task_5")},
        {'name': 'Task 6', 'url': url_for("task_6")},
        {'name': 'Task 7', 'url': url_for("task_7")},
        {'name': 'Task 8', 'url': url_for("task_8")},
        {'name': 'Task 9.Homework', 'url': url_for("task_9")}
    ]
    return dict(menu_items=menu_items)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/task_1', methods=['GET', 'POST'])
def task_1():
    if request.method == 'POST':
        return redirect(url_for('hello', name='User'))
    return render_template('task_1.html')


@app.route('/hello/<name>')
def hello(name):
    return f'Привет, {name}!'


@app.route('/task_2')
def task_2():
    return render_template('task_2.html')


@app.route('/task_2_upload', methods=['GET', 'POST'])
def task_2_upload():
    if request.method == 'POST':
        image = request.files.get('image')
        file_name = secure_filename(image.filename)
        Path(Path.cwd(), 'static', 'uploads').mkdir(exist_ok=True)
        image.save(
            PurePath.joinpath(Path.cwd(), 'static', 'uploads', file_name))
        return f"""Файл {file_name} загружен на сервер<br>
            <a href='{url_for('task_2_upload')}'>Назад</a>"""
    return render_template('form_task_2.html')


@app.route('/task_3', methods=['GET', 'POST'])
def task_3():
    login = 'l'
    password = 'p'
    if request.method == 'POST':
        l_r = request.form.get('login')
        p_r = request.form.get('password')
        if l_r == login and p_r == password:
            return redirect(url_for('hello', name=login))
        else:
            flash('Ошибка!, неверный логин или пароль', 'danger')
            return redirect(url_for('task_3'))
    return render_template('task_3.html')


@app.route('/task_4', methods=['GET', 'POST'])
def task_4():
    if request.method == 'POST':
        text = request.form.get('text').strip()
        words = split(r"[,.\s]+", text)
        return f'Слов в тексте: {len(words)}'
    return render_template('task_4.html')


@app.route('/task_5', methods=['GET', 'POST'])
def task_5():
    if request.method == 'POST':
        res = 0
        num1 = int(request.form.get('num1'))
        num2 = int(request.form.get('num2'))
        operation = request.form.get('operation')
        if operation == 'plus':
            res = num1 + num2
        elif operation == 'minus':
            res = num1 - num2
        elif operation == 'mult':
            res = num1 * num2
        elif operation == 'div':
            if num2 == 0:
                return 'На ноль делить нельзя!'
            res = num1 / num2
        return str(res)

    return render_template('task_5.html')


@app.route('/task_6', methods=['GET', 'POST'])
def task_6():
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        if age > '18':
            return render_template('index.html')
        else:
            return render_template('404.html')
    return render_template('task_6.html')


@app.route('/task_7', methods=['GET', 'POST'])
def task_7():
    if request.method == 'POST':
        num = int(request.form.get('num'))
        return f'{num} в квадрате = {num ** 2}'
    return render_template('task_7.html')


@app.route('/task_8', methods=['GET', 'POST'])
def task_8():
    if request.method == 'POST':
        if not request.form['name']:
            flash('Ошибка, введите имя!', 'danger')
            return redirect(url_for('task_8'))
        name = request.form['name']
        flash('Сообщение отправлено', 'success')
        return f'Привет, {name}'
    return render_template('task_8.html')


@app.route('/task_9', methods=['GET', 'POST'])
def task_9():
    if request.method == 'POST':
        if not request.form['name']:
            flash('Ошибка, введите имя!', 'danger')
            return redirect(url_for('task_9'))
        if not request.form['e-mail']:
            flash('Ошибка, введите e-mail!', 'danger')
            return redirect(url_for('task_9'))
        name = request.form['name']
        e_mail = request.form['e-mail']
        session['name'] = request.form.get('name')
        return redirect(url_for('hello2', name=name))
    return render_template('task_9.html')


@app.route('/hello2/<name>', methods=['GET', 'POST'])
def hello2(name):
    if 'name' in session:
        if request.method == 'POST':
            session.pop('name', None)
            return redirect(url_for('task_9'))

    return render_template('hello2.html', name=name)


if __name__ == '__main__':
    app.run(debug=True)
