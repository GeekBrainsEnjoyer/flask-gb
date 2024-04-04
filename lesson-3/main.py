from flask import Flask, redirect, render_template, request, url_for
from flask_wtf.csrf import CSRFProtect


from models import db, User
from forms import RegisterForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'gagag'
csrf = CSRFProtect(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'

db.init_app(app)


@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('gagaga')


@app.route('/')
def index():
    return redirect(url_for('register'))


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate():
        first_name = form.first_name.data
        second_name = form.second_name.data
        email = form.email.data
        password = form.password.data
        user = User(first_name=first_name, second_name=second_name,
                    email=email, password=password)
        db.session.add(user)
        db.session.commit()
        print(User.query.all())
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
