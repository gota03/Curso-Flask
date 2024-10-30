from database import db
from models.user import User
from flask import Flask, request, jsonify
from flask_login import LoginManager, login_user, current_user, login_required, logout_user

app = Flask(__name__)
login_manager = LoginManager()

app.config['SECRET_KEY'] = 'Gote03/18'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login' # nome da função responsável pela rota de login


@login_manager.user_loader # decorador responsável por informar ao flask que a função irá carregar um usuário a partir do seu id
def load_user(user_id): # o parâmetro user_id é o id do usuário armazenado na sessão pela função login_user()
    return User.query.get(user_id) # faz a busca pela chave primária, o id, e retorna um objeto User


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']

    if username and password:
        user_db = User.query.filter_by(username=username).first() # retornando o primeiro objeto User de acordo com o username fornecido

        if user_db and user_db.password == password:
            login_user(user_db) # salva o ID do usuário na sessão
            print(current_user.is_authenticated)

            return jsonify({'message': 'Logado com sucesso'})

    return jsonify({'message': 'Credenciais inválidas!'}), 400


@app.route('/logout', methods=['GET'])
@login_required # decorador que protege a rota, só pode ser acessada por usuários autenticados
def logout():
    logout_user() # remove o usuário atual da sessão e invalida o cookie de autenticação usado para manter o login
    return jsonify({'message': 'Logout realizado com sucesso'})


@app.route('/user', methods=['POST'])
def create_user():
    data = request.json
    username = data['username']
    password = data['password']

    if username and password:
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'Usuário cadastrado com sucesso'})
    
    return jsonify({'message': 'Dados inválidos'}), 400


if __name__ == '__main__':
    app.run(debug=True)