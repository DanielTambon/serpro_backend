'''FIZ ESTE ARQUIVO PARA INSERIR SERVIDORES FAKES NO SISTEMA'''

import requests
import json

# URL da API (ajuste conforme necessário)
url = 'http://localhost:5000/cadastro_servidor'

# Dados do servidor a ser cadastrado
servidores = [
    {
  "nome": "João Silva",
  "cpf": "123.456.789-00",
  "matricula": "12345",
  "codigo_orgao": "123",
  "ativo": True,
  "cargo": "Analista de Sistemas",
  "lotacao": "Departamento de TI"
},
{
  "nome": "Maria Oliveira",
  "cpf": "234.567.890-11",
  "matricula": "67890",
  "codigo_orgao": "456",
  "ativo": True,
  "cargo": "Assistente Administrativo",
  "lotacao": "Departamento de Recursos Humanos"
},
{
  "nome": "Carlos Pereira",
  "cpf": "345.678.901-22",
  "matricula": "11223",
  "codigo_orgao": "789",
  "ativo": True,
  "cargo": "Coordenador de Projetos",
  "lotacao": "Departamento de Projetos"
},
{
  "nome": "Ana Souza",
  "cpf": "456.789.012-33",
  "matricula": "44556",
  "codigo_orgao": "012",
  "ativo": False,
  "cargo": "Recepcionista",
  "lotacao": "Recepção"
},

{
  "nome": "Felipe Santos",
  "cpf": "567.890.123-44",
  "matricula": "78901",
  "codigo_orgao": "321",
  "ativo": True,
  "cargo": "Gestor de Projetos",
  "lotacao": "Departamento de Marketing"
}
,
{
  "nome": "Lucas Almeida",
  "cpf": "678.901.234-55",
  "matricula": "12367",
  "codigo_orgao": "987",
  "ativo": True,
  "cargo": "Desenvolvedor Front-end",
  "lotacao": "Departamento de TI"
}
,
{
  "nome": "Patrícia Costa",
  "cpf": "789.012.345-66",
  "matricula": "23478",
  "codigo_orgao": "654",
  "ativo": False,
  "cargo": "Analista de Marketing",
  "lotacao": "Departamento de Marketing"
}
,
{
  "nome": "Ricardo Gomes",
  "cpf": "890.123.456-77",
  "matricula": "34589",
  "codigo_orgao": "321",
  "ativo": True,
  "cargo": "Gerente de TI",
  "lotacao": "Departamento de TI"
}
,

{
  "nome": "Fernanda Martins",
  "cpf": "901.234.567-88",
  "matricula": "45690",
  "codigo_orgao": "123",
  "ativo": False,
  "cargo": "Assistente de Recursos Humanos",
  "lotacao": "Departamento de RH"
}
,
{
  "nome": "Juliana Ferreira",
  "cpf": "123.345.678-99",
  "matricula": "56701",
  "codigo_orgao": "234",
  "ativo": True,
  "cargo": "Analista de Suporte",
  "lotacao": "Departamento de TI"
}
,
{
  "nome": "Eduardo Souza",
  "cpf": "234.456.789-10",
  "matricula": "67812",
  "codigo_orgao": "876",
  "ativo": False,
  "cargo": "Coordenador de Comunicação",
  "lotacao": "Departamento de Comunicação"
}
,
{
  "nome": "Gustavo Lima",
  "cpf": "345.567.890-21",
  "matricula": "78923",
  "codigo_orgao": "432",
  "ativo": True,
  "cargo": "Desenvolvedor Backend",
  "lotacao": "Departamento de TI"
}
,
{
  "nome": "Mariana Rocha",
  "cpf": "456.678.901-32",
  "matricula": "89034",
  "codigo_orgao": "654",
  "ativo": False,
  "cargo": "Secretária Executiva",
  "lotacao": "Secretaria Executiva"
}
,
{
  "nome": "Roberto Oliveira",
  "cpf": "567.789.012-43",
  "matricula": "90145",
  "codigo_orgao": "210",
  "ativo": True,
  "cargo": "Especialista em Redes",
  "lotacao": "Departamento de Redes"
}
,
{
  "nome": "Cláudia Santos",
  "cpf": "678.890.123-54",
  "matricula": "11256",
  "codigo_orgao": "321",
  "ativo": False,
  "cargo": "Contadora",
  "lotacao": "Departamento Financeiro"
},
{
  "nome": "Cláudia Rodrigues",
  "cpf": "679.450.124-64",
  "matricula": "45789",
  "codigo_orgao": "321",
  "ativo": False,
  "cargo": "Contadora",
  "lotacao": "Departamento Financeiro"
}
]

# Enviar a requisição POST para a API
def inserir_servidores():
    for servidor in servidores:
        response = requests.post(url, json=servidor)

        # Verificar a resposta da API
        if response.status_code == 201:
            print("Servidor cadastrado com sucesso!")
            print("Resposta:", response.json())
        elif response.status_code == 400:
            print("Erro de cadastro:", response.json())
        else:
            print("Erro inesperado:", response.status_code, response.text)

inserir_servidores()