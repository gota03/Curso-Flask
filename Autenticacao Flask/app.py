from database import db
from models.user import User
from flask import Flask, request, jsonify
from flask_login import LoginManager, login_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username and password:
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            print(user)
            return jsonify({'message': 'Autenticação feita com sucesso'})
        
    return jsonify({'message': 'Credencias inválidas'}), 400


if __name__ == '__main__':
    app.run(debug=True)