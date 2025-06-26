import json
from pymongo import MongoClient
from bson.decimal128 import Decimal128
from decimal import Decimal
import os
from os import path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

json_path = path.join("banco", "livros.json")
with open(json_path, "r", encoding="utf-8") as file:
    livros = json.load(file)

MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("Variável de ambiente MONGO_URI não encontrada!")

client = MongoClient(MONGO_URI)
db = client.livraria
livros_collection = db.livros

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except Exception:
        return None

for livro in livros:
    livro_doc = {
        "titulo": livro["titulo"],
        "preco": Decimal128(Decimal(str(livro["preco"]))),  # Conversão para Decimal128
        "categoria": livro["categoria"],
        "tags": livro["tags"],
        "autores": livro["autores"],
        "mais_recente_edicao": livro.get("mais_recente_edicao", False),
        "data_publicacao": parse_date(livro["data_publicacao"]),
        "editora": livro["editora"],
        "descricao": livro["descricao"],
        "isbn": livro["isbn"],
        "estoque": livro["estoque"]
    }
    livros_collection.insert_one(livro_doc)

client.close()
print("Banco de dados populado com sucesso!")
