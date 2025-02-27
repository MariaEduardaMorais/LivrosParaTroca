from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_DIR = os.path.join(BASE_DIR, 'database')
os.makedirs(DATABASE_DIR, exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(DATABASE_DIR, 'db.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Livro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    edicao = db.Column(db.String(50), nullable=False)
    estado = db.Column(db.String(50), nullable=False)
    resenhas = db.relationship('Resenha', backref='livro', lazy=True)


class Resenha(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.Text, nullable=False)
    livro_id = db.Column(db.Integer, db.ForeignKey('livro.id'), nullable=False)

@app.route('/')
def index():
    livros = Livro.query.all()
    return render_template('index.html', livros=livros)

@app.route('/add', methods=['POST'])
def add_livro():
    data = request.get_json()
    
    if not data or not all(k in data for k in ("titulo", "autor", "edicao", "estado")):
        return jsonify({"erro": "Todos os campos são obrigatórios"}), 400

    novo_livro = Livro(
        titulo=data["titulo"], 
        autor=data["autor"], 
        edicao=data["edicao"], 
        estado=data["estado"]
    )
    
    db.session.add(novo_livro)
    db.session.commit()
    
    return jsonify({
        "id": novo_livro.id,
        "titulo": novo_livro.titulo,
        "autor": novo_livro.autor,
        "edicao": novo_livro.edicao,
        "estado": novo_livro.estado,
        "mensagem": "Livro adicionado com sucesso!"
    })

@app.route('/update/<int:id>', methods=['PUT'])
def update_livro(id):
    data = request.get_json()
    
    if not data or not all(k in data for k in ("titulo", "autor", "edicao", "estado")):
        return jsonify({"erro": "Todos os campos são obrigatórios"}), 400

    livro = Livro.query.get_or_404(id)
    livro.titulo = data["titulo"]
    livro.autor = data["autor"]
    livro.edicao = data["edicao"]
    livro.estado = data["estado"]
    
    db.session.commit()
    
    return jsonify({
        "id": livro.id,
        "titulo": livro.titulo,
        "autor": livro.autor,
        "edicao": livro.edicao,
        "estado": livro.estado,
        "mensagem": "Livro atualizado com sucesso!"
    })

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_livro(id):
    livro = Livro.query.get_or_404(id)
    db.session.delete(livro)
    db.session.commit()
    return jsonify({"mensagem": "Livro excluído com sucesso!"})


@app.route('/livro/<int:livro_id>', methods=['GET', 'POST'])
def detalhes_livro(livro_id):
    livro = Livro.query.get_or_404(livro_id)
    if request.method == 'POST':
        conteudo = request.form['conteudo']
        nova_resenha = Resenha(conteudo=conteudo, livro_id=livro_id)
        db.session.add(nova_resenha)
        db.session.commit()
        return redirect(url_for('detalhes_livro', livro_id=livro_id))
    return render_template('detalhes.html', livro=livro)


@app.route('/delete_resenha/<int:resenha_id>/<int:livro_id>')
def delete_resenha(resenha_id, livro_id):
    resenha = Resenha.query.get_or_404(resenha_id)
    db.session.delete(resenha)
    db.session.commit()
    return redirect(url_for('detalhes_livro', livro_id=livro_id))

if __name__ == '__main__':
    os.makedirs(os.path.join(BASE_DIR, 'database'), exist_ok=True)
    with app.app_context():
        db.create_all()
    app.run(debug=True)