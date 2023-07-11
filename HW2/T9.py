from flask import Flask, request, redirect, url_for, render_template, make_response

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def get_login():

    if request.method == "POST":
        login = request.form.get('login')
        email_ = request.form.get('email')
        response = make_response(render_template('set_cookie.html'))
        response.set_cookie('login', login)
        response.set_cookie('email', email_)
        if request.cookies.get('login') and request.cookies.get('email'):
            return redirect(url_for('get_cookie'))
        return response
    return render_template('set_cookie.html')


@app.route('/cookie/', methods=["POST", "GET"])
def get_cookie():
    login = request.cookies.get('login')
    email_ = request.cookies.get('email')
    print(f'{login = }')
    context = {'login': login}
    response = make_response(render_template('get_cookie.html', **context))
    if request.method == "POST":
        response.delete_cookie('login')
        response.delete_cookie('email')
        if not (request.cookies.get('login') and request.cookies.get('email')):
            return redirect(url_for('get_login'))
        return response
    return response


if __name__ == '__main__':
    app.run()