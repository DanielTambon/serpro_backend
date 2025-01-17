from flask_jwt_extended import JWTManager, create_access_token
from flask import Flask, jsonify, request, send_file
from models import db, Usuario, Documento, Servidor
from flasgger import Swagger
from werkzeug.utils import secure_filename
from datetime import datetime
import secrets
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Habilita o CORS para todas as rotas

# Configuração do banco de dados (exemplo com SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meu_banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
UPLOAD_FOLDER = 'uploads/documentos'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Garante que a pasta exista
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db.init_app(app)

with app.app_context():
    db.create_all()  # Cria as tabelas no banco de dados


# Configuração do JWT
app.config['JWT_SECRET_KEY'] = secrets.token_hex(32)  # Substitua por uma chave secreta segura
jwt = JWTManager(app)

swagger = Swagger(app)

@app.route('/login', methods=['POST'])
def login():
    """
    Realiza o login do usuário.
    ---
    parameters:
      - in: body
        name: body
        description: Dados de login
        schema:
          type: object
          required:
            - email
            - senha
          properties:
            email:
              type: string
              description: Email do usuário
            senha:
              type: string
              description: Senha do usuário
    responses:
      200:
        description: Login bem-sucedido, retorna o token
      400:
        description: Erro de validação, falta email ou senha
      401:
        description: Credenciais inválidas
    """
    dados = request.json
    email = dados.get('email')
    senha = dados.get('senha')

    if not email or not senha:
        return jsonify({'erro': 'Email e senha são obrigatórios.'}), 400

    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario or not usuario.verificar_senha(senha):
        return jsonify({'erro': 'Credenciais inválidas.'}), 401

    # Cria o token de acesso
    token = create_access_token(identity={'id': usuario.id, 'tipo': usuario.tipo})
    return jsonify({'mensagem': 'Login bem-sucedido.', 'token': token}), 200


@app.route('/cadastro', methods=['POST'])
def cadastro():
    """
    Realiza o cadastro de um novo usuário.
    ---
    parameters:
      - in: body
        name: body
        description: Dados de cadastro
        schema:
          type: object
          required:
            - nome
            - email
            - senha
            - tipo
          properties:
            nome:
              type: string
              description: Nome do usuário
            email:
              type: string
              description: Email do usuário
            senha:
              type: string
              description: Senha do usuário
            tipo:
              type: string
              description: Tipo do usuário ('gestor' ou 'comum')
    responses:
      201:
        description: Usuário cadastrado com sucesso
      400:
        description: Dados obrigatórios não fornecidos
      409:
        description: Email já cadastrado
    """
    dados = request.json
    nome = dados.get('nome')
    email = dados.get('email')
    senha = dados.get('senha')
    tipo = dados.get('tipo')  # 'gestor' ou 'comum'

    # Validação dos campos obrigatórios
    if not nome or not email or not senha or not tipo:
        return jsonify({'erro': 'Todos os campos (nome, email, senha, tipo) são obrigatórios.'}), 400

    # Verificar se o tipo de usuário é válido
    if tipo not in ['gestor', 'comum']:
        return jsonify({'erro': "O campo 'tipo' deve ser 'gestor' ou 'comum'."}), 400

    # Verificar se o email já está cadastrado
    if Usuario.query.filter_by(email=email).first():
        return jsonify({'erro': 'Este email já está cadastrado.'}), 409

    # Criar o novo usuário
    novo_usuario = Usuario(nome=nome, email=email, tipo=tipo)
    novo_usuario.set_senha(senha)

    # Salvar no banco de dados
    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify({'mensagem': 'Usuário cadastrado com sucesso!'}), 201


@app.route('/upload', methods=['POST'])
def upload_documento():
    """
    Realiza o upload de um documento.
    ---
    parameters:
      - in: formData
        name: arquivo
        type: file
        description: Arquivo a ser enviado
      - in: formData
        name: cpf_servidor
        type: string
        description: CPF do servidor
      - in: formData
        name: tipo_documento
        type: string
        description: Tipo do documento
    responses:
      201:
        description: Documento enviado com sucesso
      400:
        description: Erro de validação, falta de arquivo, CPF ou tipo de documento
    """
    if 'arquivo' not in request.files:
        return jsonify({'erro': 'Nenhum arquivo enviado.'}), 400

    arquivo = request.files['arquivo']
    cpf_servidor = request.form.get('cpf_servidor')
    tipo_documento = request.form.get('tipo_documento')

    if not arquivo or not cpf_servidor or not tipo_documento:
        return jsonify({'erro': 'Arquivo, CPF e tipo do documento são obrigatórios.'}), 400

    # Salvar o arquivo
    nome_arquivo = secure_filename(f"{cpf_servidor}_{tipo_documento}_{datetime.now().isoformat()}.pdf")
    caminho_arquivo = os.path.join(app.config['UPLOAD_FOLDER'], nome_arquivo)
    arquivo.save(caminho_arquivo)

    # Salvar registro no banco
    novo_documento = Documento(
        cpf_servidor=cpf_servidor,
        hora_cadastro=datetime.now(),
        tipo=tipo_documento,
        caminho_arquivo=caminho_arquivo
    )
    db.session.add(novo_documento)
    db.session.commit()

    return jsonify({'mensagem': 'Documento enviado com sucesso!'}), 201

@app.route('/download/<int:id>', methods=['GET'])
def download_documento(id):
    """
    Realiza o download de um documento.
    ---
    parameters:
      - in: path
        name: id
        type: integer
        description: ID do documento
    responses:
      200:
        description: Documento encontrado e enviado para download
      404:
        description: Documento não encontrado
    """
    documento = Documento.query.get(id)
    if not documento:
        return jsonify({'erro': 'Documento não encontrado.'}), 404

    caminho_arquivo = documento.caminho_arquivo
    if not os.path.exists(caminho_arquivo):
        return jsonify({'erro': 'Arquivo não encontrado no servidor.'}), 404

    return send_file(caminho_arquivo, as_attachment=True)

@app.route('/cadastro_servidor', methods=['POST'])
def cadastro_servidor():
    """
    Realiza o cadastro de um servidor.
    ---
    parameters:
      - in: body
        name: body
        description: Dados do servidor
        schema:
          type: object
          required:
            - nome
            - cpf
            - matricula
            - codigo_orgao
            - ativo
            - cargo
            - lotacao
          properties:
            nome:
              type: string
              description: Nome do servidor
            cpf:
              type: string
              description: CPF do servidor
            matricula:
              type: string
              description: Matrícula do servidor
            codigo_orgao:
              type: string
              description: Código do órgão
            ativo:
              type: boolean
              description: Status de ativo/inativo
            cargo:
              type: string
              description: Cargo do servidor
            lotacao:
              type: string
              description: Lotação do servidor
    responses:
      201:
        description: Servidor cadastrado com sucesso
      400:
        description: Erro de validação, campos obrigatórios ausentes
    """
    data = request.get_json()

    # Verificar se todos os campos foram preenchidos
    if not data or not all(key in data for key in ['nome', 'cpf', 'matricula', 'codigo_orgao', 'ativo', 'cargo', 'lotacao']):
        return jsonify({'erro': 'Todos os campos são obrigatórios.'}), 400

    try:
        # Criar o servidor a partir dos dados recebidos
        novo_servidor = Servidor(
            nome=data['nome'],
            cpf=data['cpf'],
            matricula=data['matricula'],
            codigo_orgao=data['codigo_orgao'],
            ativo=data['ativo'],
            cargo=data['cargo'],
            lotacao=data['lotacao']
        )

        # Adicionar e salvar o servidor no banco de dados
        db.session.add(novo_servidor)
        db.session.commit()

        return jsonify({'mensagem': 'Servidor cadastrado com sucesso!'}), 201
    
    except Exception as e:
        # Tratar outros erros
        return jsonify({'erro': str(e)}), 500
    
@app.route('/consulta_servidor', methods=['GET'])
def consulta_servidor():
    """
    Consulta servidores de acordo com os parâmetros fornecidos.
    ---
    parameters:
      - in: query
        name: nome
        type: string
        description: Nome do servidor (parcial ou completo)
      - in: query
        name: cpf
        type: string
        description: CPF do servidor
      - in: query
        name: matricula
        type: string
        description: Matrícula do servidor
      - in: query
        name: codigo_orgao
        type: string
        description: Código do órgão do servidor
    responses:
      200:
        description: Lista de servidores encontrados
        schema:
          type: object
          properties:
            servidores:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  nome:
                    type: string
                  cpf:
                    type: string
                  matricula:
                    type: string
                  codigo_orgao:
                    type: string
                  ativo:
                    type: boolean
                  cargo:
                    type: string
                  lotacao:
                    type: string
      404:
        description: Nenhum servidor encontrado com os parâmetros fornecidos
    """
    # Pegando parâmetros da query string
    nome = request.args.get('nome')
    cpf = request.args.get('cpf')
    matricula = request.args.get('matricula')
    codigo_orgao = request.args.get('codigo_orgao')

    # Construindo a consulta de acordo com os parâmetros passados
    query = Servidor.query

    if nome:
        query = query.filter(Servidor.nome.ilike(f'%{nome}%'))  # Filtra pelo nome (case-insensitive)
    if cpf:
        query = query.filter(Servidor.cpf == cpf)  # Filtra pelo CPF exato
    if matricula:
        query = query.filter(Servidor.matricula == matricula)  # Filtra pela matrícula exata
    if codigo_orgao:
        query = query.filter(Servidor.codigo_orgao == codigo_orgao)  # Filtra pelo código do órgão exato

    # Executa a consulta
    servidores = query.all()

    # Verifica se algum servidor foi encontrado
    if servidores:
        # Retorna a lista de servidores encontrados
        servidores_list = [{
            'id': servidor.id,
            'nome': servidor.nome,
            'cpf': servidor.cpf,
            'matricula': servidor.matricula,
            'codigo_orgao': servidor.codigo_orgao,
            'ativo': servidor.ativo,
            'cargo': servidor.cargo,
            'lotacao': servidor.lotacao
        } for servidor in servidores]
        
        return jsonify({'servidores': servidores_list}), 200
    else:
        return jsonify({'mensagem': 'Nenhum servidor encontrado para os parâmetros fornecidos.'}), 404
    
@app.route('/consulta_documentos', methods=['GET'])
def consulta_documentos():
    """
    Consulta documentos vinculados a um servidor pelo CPF.
    ---
    parameters:
      - in: query
        name: cpf
        type: string
        description: CPF do servidor, utilizado para buscar os documentos
    responses:
      200:
        description: Lista de documentos encontrados para o servidor
        schema:
          type: object
          properties:
            documentos:
              type: array
              items:
                type: object
                properties:
                  id_documento:
                    type: integer
                  cpf_servidor:
                    type: string
                  hora_cadastro_documento:
                    type: string
                    format: date-time
                  tipo_documento:
                    type: string
      400:
        description: CPF do servidor é obrigatório
      404:
        description: Nenhum documento encontrado para o CPF do servidor fornecido
    """
    cpf_servidor = request.args.get('cpf')
    
    if not cpf_servidor:
        return jsonify({'mensagem': 'CPF do servidor é obrigatório.'}), 400
    
    # Consultando documentos vinculados ao servidor
    documentos = Documento.query.filter(Documento.cpf_servidor == cpf_servidor).all()
    
    if documentos:
        # Montando a resposta com os dados dos documentos
        documentos_list = [{
            'id_documento': documento.id,
            'cpf_servidor': documento.cpf_servidor,
            'hora_cadastro_documento': documento.hora_cadastro,
            'tipo_documento': documento.tipo,
            'caminho_arquivo': documento.caminho_arquivo
        } for documento in documentos]
        
        return jsonify({'documentos': documentos_list}), 200
    else:
        return jsonify({'mensagem': 'Nenhum documento encontrado para o servidor com CPF fornecido.'}), 404
    
@app.route('/consulta_documentos_', methods=['GET'])
def consulta_documentos_():
    """
    Consulta documentos vinculados a um servidor pelo CPF.
    ---
    parameters:
      - in: query
        name: cpf
        type: string
        description: CPF do servidor, utilizado para buscar os documentos
    responses:
      200:
        description: Lista de documentos encontrados para o servidor
        schema:
          type: object
          properties:
            documentos:
              type: array
              items:
                type: object
                properties:
                  id_documento:
                    type: integer
                  cpf_servidor:
                    type: string
                  hora_cadastro_documento:
                    type: string
                    format: date-time
                  tipo_documento:
                    type: string
      400:
        description: CPF do servidor é obrigatório
      404:
        description: Nenhum documento encontrado para o CPF do servidor fornecido
    """
    
    
    # Consultando documentos vinculados ao servidor
    documentos = Documento.query.all()
    
    if documentos:
        # Montando a resposta com os dados dos documentos
        documentos_list = [documento.__dict__ for documento in documentos]
        
        return {'documentos': documentos_list}, 200
    else:
        return jsonify({'mensagem': 'Nenhum documento encontrado .'}), 404

if __name__ == '__main__':
    app.run(debug=True)
