import sqlite3
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# CONFIGURAÇÃO E CONEXÃO DO BANCO DE DADOS
def conectar_banco():
    conexao = sqlite3.connect("drive_thru.db")
    conexao.row_factory = sqlite3.Row
    cursor = conexao.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE,
        preco REAL NOT NULL,
        categoria TEXT DEFAULT 'lanches',
        imagem TEXT DEFAULT 'default.png'
    )
""")
    conexao.commit()
    return conexao, cursor


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/produtos", methods=["GET"])
def listar_produtos():
    conexao, cursor = conectar_banco()
    cursor.execute("SELECT * FROM produtos")
    produtos = [dict(row) for row in cursor.fetchall()]
    conexao.close()
    return jsonify(produtos)

@app.route("/produtos", methods=["POST"])
def cadastrar_produto():
    dados = request.get_json()
    nome = dados.get("nome")
    preco = dados.get("preco")
    conexao, cursor = conectar_banco()
    try:
        cursor.execute("INSERT INTO produtos (nome, preco) VALUES (?, ?)", (nome, preco))
        conexao.commit()
        return jsonify({"mensagem": f"🎉 Produto '{nome}' cadastrado com sucesso!"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"erro": f"⚠️ Produto '{nome}' já cadastrado."}), 409
    finally:
        conexao.close()

@app.route("/produtos/<int:id>", methods=["DELETE"])
def remover_produto(id):
    conexao, cursor = conectar_banco()
    cursor.execute("DELETE FROM produtos WHERE id = ?", (id,))
    conexao.commit()
    rowcount = cursor.rowcount
    conexao.close()
    if rowcount > 0:
        return jsonify({"mensagem": f"🗑️ Produto {id} removido."})
    return jsonify({"erro": "Produto não encontrado."}), 404

@app.route("/banco_produtos")
def banco_produtos():
    produtos = [
        # lanches
        ("Whopper", 35.90, "lanches", "Whopper.png"),
        ("Whopper Duplo", 42.90, "lanches", "Whopper_Duplo.png"),
        ("Whopper Jr", 24.90, "lanches", "Whopper_Jr.png"),
        ("Whopper Furioso", 38.90, "lanches", "Whopper_Furioso.png"),
        ("Whopper Rodeio", 38.90, "lanches", "Whopper_Rodeio.png"),
        ("Big King", 32.90, "lanches", "Big_King.png"),
        ("King Bacon", 34.90, "lanches", "King_Bacon.png"),
        ("King Duplo Bacon", 41.90, "lanches", "King_Duplo_Bacon.png"),
        ("King Fraldinha", 39.90, "lanches", "King_Fraldinha.png"),
        ("Rodeio", 29.90, "lanches", "Rodeio.png"),
        ("Rodeio Duplo", 36.90, "lanches", "Rodeio_Duplo.png"),
        ("Cheddar Jr", 22.90, "lanches", "Cheddar_Jr.png"),
        ("Cheddar Duplo", 32.90, "lanches", "Cheddar_Duplo.png"),
        ("Cheeseburger", 14.90, "lanches", "Cheeseburger.png"),
        ("Cheeseburger Duplo", 19.90, "lanches", "Cheeseburger_Duplo.png"),
        ("BK Chicken", 28.90, "lanches", "BK_Chicken.png"),
        ("Chicken Jr", 22.90, "lanches", "Chicken_Jr.png"),
        ("Chicken Duplo Bacon", 34.90, "lanches", "Chicken_Duplo_Bacon.png"),
        ("Stacker Duplo", 38.90, "lanches", "Stacker_Duplo.png"),
        ("Mega Stacker Cheddar", 44.90, "lanches", "Mega_Stacker_Cheddar_3.png"),
        ("Mega Stacker Rodeio", 44.90, "lanches", "Mega_Stacker_Rodeio_3.png"),
        ("Batata Media", 10.90, "lanches", "Batata_Media.png"),
        ("Balde de Batata", 29.90, "lanches", "Balde_Batata.png"),
        ("Onion Rings", 14.90, "lanches", "Onion_Rings.png"),
        # bebidas
        ("Coca-Cola", 9.90, "bebidas", "Coca.png"),
        ("Coca-Cola Zero", 9.90, "bebidas", "Coca_zero.png"),
        ("Fanta Laranja", 9.90, "bebidas", "Fanta_Laranja.png"),
        ("Sprite", 9.90, "bebidas", "Sprite.png"),
        ("Suco de Laranja", 11.90, "bebidas", "Suco_Laranja.png"),
        ("Água", 5.90, "bebidas", "Agua.png"),
        ("BK Shake Crocante", 16.90, "bebidas", "BK_Shake_Crocante.png"),
        ("BK Shake Morango", 16.90, "bebidas", "BK_Shake_Morango.png"),
        # sobremesas
        ("BK Mix Brownie", 14.90, "sobremesa", "BK_Mix_Brownie.png"),
        ("BK Mix Nutella", 14.90, "sobremesa", "BK_Mix_LeitePo_Nutella.png"),
        ("BK Mix Ovomaltine", 14.90, "sobremesa", "BK_Mix_Ovomaltine.png"),
        ("Casquinha Baunilha", 6.90, "sobremesa", "Casquinha_Baunilha.png"),
        # molhos
        ("Baconese", 2.90, "molhos", "Baconese.png"),
        ("Maionese", 2.90, "molhos", "Maionese.png"),
        ("Maionese Temperada", 2.90, "molhos", "Sache_Maionese_Temperada.png"),
    ]

    conexao, cursor = conectar_banco()
    inseridos = 0
    for nome, preco, categoria, imagem in produtos:
        try:
            cursor.execute(
                "INSERT INTO produtos (nome, preco, categoria, imagem) VALUES (?, ?, ?, ?)",
                (nome, preco, categoria, imagem)
            )
            inseridos += 1
        except sqlite3.IntegrityError:
            pass
    conexao.commit()
    conexao.close()
    return jsonify({"mensagem": f"{inseridos} produtos cadastrados com sucesso!"})

if __name__ == "__main__":
    conectar_banco()
    app.run(debug=True)