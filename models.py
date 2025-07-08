from pymongo import MongoClient
from bson.objectid import ObjectId
import os

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
        # Todo
        pass

    @staticmethod
    def buscar_por_id(id_livro):
        """
        Busca um livro pelo seu ID.
        :param id_livro: ID do livro (string ou ObjectId)
        :return: Dicionário com os dados do livro ou None.
        """
        try:
            id_livro = ObjectId(id_livro)
        except Exception:
            return None  # ID inválido
        return livros.find_one({'_id': id_livro})
    

    @staticmethod
    def buscar_todos():
        """
        Retorna todos os livros cadastrados.
        :return: Lista de livros.
        """
        # Todo
        pass
    
    @staticmethod
    def buscar_livros(filtros=None, pagina=1, por_pagina=12):
        """
        Busca livros com filtros e paginação.
        :param filtros: Dicionário de filtros para busca.
        :param pagina: Número da página.
        :param por_pagina: Quantidade de livros por página.
        :return: (Lista de livros, total de livros encontrados)
        """
        # Todo
        pass

    @staticmethod
    def categorias_disponiveis():
        """
        Retorna todas as categorias disponíveis no acervo.
        :return: Lista de categorias.
        """
        # Todo
        pass

    @staticmethod
    def tags_disponiveis():
        """
        Retorna todas as categorias disponíveis no acervo.
        :return: Lista de categorias.
        """
        # Todo
        pass

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
        # Todo
        pass

    @staticmethod
    def buscar_por_email(email):
        """
        Busca um usuário pelo e-mail.
        :param email: E-mail do usuário.
        :return: Dicionário com os dados do usuário ou None.
        """
        # Todo
        pass

    @staticmethod
    def buscar_por_id(id_usuario):
        """
        Busca um usuário pelo ID.
        :param id_usuario: ID do usuário (string ou ObjectId).
        :return: Dicionário com os dados do usuário ou None.
        """
        # Todo
        pass

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
        # Todo
        pass

    @staticmethod
    def buscar_por_usuario(id_usuario):
        """
        Busca todos os pedidos de um usuário.
        :param id_usuario: ID do usuário.
        :return: Lista de pedidos.
        """
        # Todo
        pass

    @staticmethod
    def buscar_por_id(id_pedido):
        """
        Busca um pedido pelo seu ID.
        :param id_pedido: ID do pedido (string ou ObjectId).
        :return: Dicionário com os dados do pedido ou None.
        """
        # Todo
        pass
