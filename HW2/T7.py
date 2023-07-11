from flask import Flask, request, redirect, url_for, render_template

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def check_number():
    if request.method == 'POST':
        num = request.form.get('number')
        return redirect(url_for('print_num', num=num))
    return render_template("get_num.html")


@app.route('/num')
def print_num():
    num = int(request.args.get('num'))
    return f'Number: {num}<br>Square number: {num ** 2}'


if __name__ == '__main__':
    app.run()