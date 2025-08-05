from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from bson.decimal128 import Decimal128
from decimal import Decimal
from datetime import datetime
# ===========================
# Configuração da conexão com o MongoDB Atlas
# ===========================

# Obtém a URI do MongoDB a partir das variáveis de ambiente
MONGO_URI = os.environ.get('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client.livraria  # nome do banco de dados

# Coleções utilizadas no banco de dados
livros = db.livros
usuarios = db.usuarios
pedidos = db.pedidos

# ===========================
# Classe Livro
# ===========================

class Livro:
    """
    Classe que representa um livro na livraria.
    """
    
    def __init__(self, titulo, preco, categoria, tags, autores, mais_recente_edicao, numero_autores, data_publicacao, editora, descricao, isbn, estoque, imagem_capa):
        """
        Inicializa um objeto Livro com os atributos fornecidos.
        """
        self.titulo = titulo
        self.preco = preco
        self.categoria = categoria
        self.tags = tags
        self.autores = autores
        self.mais_recente_edicao = mais_recente_edicao
        self.numero_autores = numero_autores
        self.data_publicacao = data_publicacao
        self.editora = editora
        self.descricao = descricao
        self.isbn = isbn
        self.estoque = estoque
        self.imagem_capa = imagem_capa

    def salvar(self):
        """
        Salva o livro no banco de dados.
        :return: ID do livro inserido.
        """
        livro_dicionario = {
            "titulo": self.titulo,
            "preco": Decimal128(Decimal(self.preco)),
            "categoria": self.categoria,
            "tags": self.tags,
            "autores": self.autores,
            "mais_recente_edicao": self.mais_recente_edicao,
            "numero_autores": self.numero_autores,
            "data_publicacao": datetime.strptime(self.data_publicacao, "%Y-%m-%d"),
            "editora": self.editora,
            "descricao": self.descricao,
            "isbn": self.isbn,
            "estoque": self.estoque,
            "imagem_capa": self.imagem_capa
        }
        return str(livros.insert_one(livro_dicionario).inserted_id)

    @staticmethod
    def buscar_por_id(id_livro):
        """
        Busca um livro pelo seu ID.
        :param id_livro: ID do livro (string ou ObjectId)
        :return: Dicionário com os dados do livro ou None.
        """
        return livros.find_one({'_id': id_livro})
    

    @staticmethod
    def buscar_todos():
        """
        Retorna todos os livros cadastrados.
        :return: Lista de livros.
        """
        return list(livros.find())
    
    @staticmethod
    def buscar_livros(filtros=None, pagina=1, por_pagina=12):
        """
        Busca livros com filtros e paginação.
        :param filtros: Dicionário de filtros para busca.
        :param pagina: Número da página.
        :param por_pagina: Quantidade de livros por página.
        :return: (Lista de livros, total de livros encontrados)
        """
        query = {}

        if filtros:
            if 'titulo' in filtros:
                query["titulo"] = {"$regex": filtros["titulo"], "$options": "i"}
            if 'tags' in filtros:
                tags = filtros["tags"]
                query["tags"] = {"$in": tags if isinstance(tags, list) else [tags]}

            if 'categoria' in filtros:
                query["categoria"] = filtros["categoria"]

            preco = {}
            if "preco_min" in filtros:
                preco["$gte"] = Decimal128(Decimal(filtros["preco_min"]))
            if "preco_max" in filtros:
                preco["$lte"] = Decimal128(Decimal(filtros["preco_max"]))
            if preco:
                query["preco"] = preco

        skip = (pagina -1) * por_pagina
        cursor = livros.find(query).skip(skip).limit(por_pagina)
        total = livros.count_documents(query)

        lista_livros = []
        for livro in cursor:
            livro["_id"] = str(livro["_id"])
            if "preco" in livro and isinstance(livro["preco"], Decimal128):
                livro["preco"] = float(livro["preco"].to_decimal())
            lista_livros.append(livro)

        return lista_livros, total

    @staticmethod
    def categorias_disponiveis():
        """
        Retorna todas as categorias disponíveis no acervo.
        :return: Lista de categorias.
        """
        return livros.distinct('categoria')

    @staticmethod
    def tags_disponiveis():
        """
        Retorna todas as categorias disponíveis no acervo.
        :return: Lista de categorias.
        """
        return livros.distinct('tags')

class Usuario:
    """
    Classe que representa um usuário da livraria.
    """
    
    def __init__(self, nome, email, senha):
        """
        Inicializa um objeto Usuario.
        :param nome: Nome do usuário.
        :param email: E-mail do usuário.
        :param senha: Senha do usuário (deve ser criptografada antes de salvar!).
        """
        self.nome = nome
        self.email = email
        self.senha = senha  # Importante: criptografar antes de salvar!

    def salvar(self):
        """
        Salva o usuário no banco de dados.
        :return: ID do usuário inserido.
        """
        usuario_dicionario = {
            "nome": self.nome,
            "email": self.email,
            "senha": self.senha
        }
        return str(usuarios.insert_one(usuario_dicionario).inserted_id)

    @staticmethod
    def buscar_por_email(email):
        """
        Busca um usuário pelo e-mail.
        :param email: E-mail do usuário.
        :return: Dicionário com os dados do usuário ou None.
        """
        return usuarios.find_one({'email': email})

    @staticmethod
    def buscar_por_id(id_usuario):
        """
        Busca um usuário pelo ID.
        :param id_usuario: ID do usuário (string ou ObjectId).
        :return: Dicionário com os dados do usuário ou None.
        """
        return usuarios.find_one({'_id': id_usuario})

# ===========================
# Classe Pedido
# ===========================

class Pedido:
    """
    Classe que representa um pedido realizado por um usuário.
    """
    
    def __init__(self, id_usuario, livros, data, total, status="pendente"):
        """
        Inicializa um objeto Pedido.
        :param id_usuario: ID do usuário que fez o pedido.
        :param livros: Lista de dicionários contendo id_livro, quantidade e preço.
        :param data: Data do pedido (ex: datetime.now()).
        :param total: Valor total do pedido.
        :param status: Status do pedido (default: "pendente").
        """
        self.id_usuario = id_usuario
        self.livros = livros  # lista de dicionários com id_livro, quantidade, preco
        self.data = data      # data do pedido (ex: datetime.now())
        self.total = total
        self.status = status

    def salvar(self):
        """
        Salva o pedido no banco de dados.
        :return: ID do pedido inserido.
        """
        pedido_dicionario = {
            "id_usuario": self.id_usuario,
            "livros": self.livros,
            "data": self.data,
            "total": self.total,
            "status": self.status,
        }
        return str(pedidos.insert_one(pedido_dicionario).inserted_id)

    @staticmethod
    def buscar_por_usuario(id_usuario):
        """
        Busca todos os pedidos de um usuário.
        :param id_usuario: ID do usuário.
        :return: Lista de pedidos.
        """
        pedidos_usuario = list(pedidos.find({'id_usuario': id_usuario}))
        return pedidos_usuario

    @staticmethod
    def buscar_por_id(id_pedido):
        """
        Busca um pedido pelo seu ID.
        :param id_pedido: ID do pedido (string ou ObjectId).
        :return: Dicionário com os dados do pedido ou None.
        """
        return pedidos.find_one({'_id': id_pedido})
