from flask import Flask, flash, make_response, redirect, request, render_template, url_for


app = Flask(__name__)
app.secret_key = '123'


@app.route('/', methods=['POST', 'GET'])
def index():
    context = {'title': 'index'}
    return render_template('index.html', **context)


@app.route('/hello_cookies/', methods=['POST', 'GET'])
def hello_cookies():
    name = request.form.get('name')
    email = request.form.get('email')
    context = {'name': name,
               'title': 'hello_' + name}
    response = make_response(render_template(
        'hello_user_page.html', **context))
    response.set_cookie('name', name)
    response.set_cookie('email', email)
    cookies = request.cookies
    return response


@app.route('/exit_/', methods=['POST', 'GET'])
def exit_():
    response = redirect(url_for('index'))
    response.delete_cookie('name')
    response.delete_cookie('email')
    cookies = request.cookies
    flash(f'{cookies = }', 'warning')
    return response


if __name__ == '__main__':
    app.run(debug=True)
