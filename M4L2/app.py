from flask import Flask, render_template, request, redirect
from models import db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login_form():

    return render_template('login.html')

@app.route("/login", methods=["POST"])
def login():
    form_username = request.form["username"]
    form_password = request.form["password"]

    user_db = User.query.all()

    for user in user_db:
        if user.login == form_username and user.password == form_password:
            return redirect('/')
    
    error = "Nombre de usuario o contraseña incorrectos"
    return render_template('login.html', error=error)

@app.route('/register')
def register_form():
    return render_template('register.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    username = request.form["username"]
    password = request.form["password"]

    user = User(login=username, password=password)
    db.session.add(user)
    db.session.commit()

    return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)