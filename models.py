from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # Valores possíveis: 'gestor' ou 'comum'

    def set_senha(self, senha):
        """Define o hash da senha."""
        self.senha_hash = generate_password_hash(senha)

    def verificar_senha(self, senha):
        """Verifica se a senha corresponde ao hash armazenado."""
        return check_password_hash(self.senha_hash, senha)

class Servidor(db.Model):
    __tablename__ = 'servidores'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)  # CPF formatado como "XXX.XXX.XXX-XX"
    matricula = db.Column(db.String(50), unique=True, nullable=False)
    codigo_orgao = db.Column(db.String(10), nullable=False)
    ativo = db.Column(db.Boolean, nullable=False, default=True)  # True = Ativo, False = Inativo
    cargo = db.Column(db.String(100), nullable=False)
    lotacao = db.Column(db.String(100), nullable=False)

    # Relacionamento com documentos (um servidor pode ter vários documentos)
    documentos = db.relationship('Documento', backref='servidor', lazy=True)

class Documento(db.Model):
    __tablename__ = 'documentos'

    id = db.Column(db.Integer, primary_key=True)  # ID único do documento
    cpf_servidor = db.Column(db.String(14), db.ForeignKey('servidores.cpf'), nullable=False)
    hora_cadastro = db.Column(db.DateTime, nullable=False)  # Hora em que o documento foi cadastrado
    tipo = db.Column(db.String(50), nullable=False)  # Tipo do documento (exemplo: "RG", "Certidão")
    caminho_arquivo = db.Column(db.String(255), nullable=False)  # Caminho para o arquivo armazenado no servidor