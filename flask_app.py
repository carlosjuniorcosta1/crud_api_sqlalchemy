from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:jose1984br@localhost:3306/youtube'
db = SQLAlchemy(app)

class Usuario(db.Model):
    
    id = db.Column(db.Integer,primary_key=True, autoincrement = True)
    nome = db.Column(db.String(50))
    email = db.Column(db.String(100))

    def to_json(self):
        return {'id': self.id, 'nome': self.nome, 'email': self.email}
    

with app.app_context():
    db.metadata.create_all(checkfirst=True, bind=db.engine)

@app.route('/usuarios', methods=["GET"])
def seleciona_usuario():
    usuarios_objetos= Usuario.query.all()
    usuarios_json = [x.to_json() for x in usuarios_objetos]
    return jsonify(data=usuarios_json), 200   

@app.route('/usuario/<id>', methods=['GET'])
def seleciona_usuario_id(id):
    usuario_objeto = Usuario.query.filter_by(id=id).first()
    usuario_json = usuario_objeto.to_json()
    return jsonify(data=usuario_json), 200

@app.route('/usuario', methods=['POST'])
def cria_usuario():
    body = request.get_json()
    try:
        novo_usuario = Usuario(nome=body['nome'], email=body['email'])
        db.session.add(novo_usuario)     
        db.session.commit() 
        ultimo_id = novo_usuario.id
        response = {
            "data": novo_usuario.to_json()
        }      
        return jsonify(response), 201

    except Exception as e:
        print(e)
        return jsonify(message="Erro ao cadastrar"), 400
    
@app.route('/usuario/<id>', methods=['PUT'])
def atualiza_usuario(id):
    usuario_objeto = Usuario.query.filter_by(id=id).first()
    body = request.get_json()
    try:
        usuario_objeto.nome = body['nome']
        usuario_objeto.email = body['email']

        db.session.add(usuario_objeto)
        db.session.commit()
        return jsonify(data= usuario_objeto.to_json()),200
    except Exception as e:
        print('Erro', e)
        return jsonify(data=usuario_objeto.to_json())

@app.route('/usuario/<id>', methods=['DELETE'])
def deleta_usuario(id):
    usuario_objeto = Usuario.query.filter_by(id=id).first()
    try:
        db.session.delete(usuario_objeto)
        db.session.commit()
        return jsonify(data=usuario_objeto.to_json(), message="Esse usuário foi apagado")
    except Exception as e:
        print('Erro', e)
        return jsonify(message="Usuário não apagado erro")
    
app.run()

