import sqlite3
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)


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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT,
            total REAL NOT NULL,
            data_hora TEXT NOT NULL
            )
        """)
    
    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS itens_pedido (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pedido_id INTEGER NOT NULL,
            produto_id INTEGER NOT NULL,
            nome TEXT NOT NULL,
            preco REAL NOT NULL,
            quantidade INTEGER NOT NULL,
            FOREIGN KEY (pedido_id) REFERENCES pedidos(id)
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


def popular_banco_se_vazio():
    conexao, cursor = conectar_banco()
    cursor.execute("SELECT COUNT(*) FROM produtos")
    total = cursor.fetchone()[0]

    if total > 0:
        conexao.close()
        return # caso já tenha produto cadastrado não fazer nada.

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
        ("BK Mix Brownie", 14.90, "sobremesas", "BK_Mix_Brownie.png"),
        ("BK Mix Nutella", 14.90, "sobremesas", "BK_Mix_LeitePo_Nutella.png"),
        ("BK Mix Ovomaltine", 14.90, "sobremesas", "BK_Mix_Ovomaltine.png"),
        ("Casquinha Baunilha", 6.90, "sobremesas", "Casquinha_Baunilha.png"),
        # molhos
        ("Baconese", 2.90, "molhos", "Baconese.png"),
        ("Maionese", 2.90, "molhos", "Maionese.png"),
        ("Maionese Temperada", 2.90, "molhos", "Sache_Maionese_Temperada.png"),
    ]

    
    for nome, preco, categoria, imagem in produtos:
        try:
            cursor.execute(
                "INSERT INTO produtos (nome, preco, categoria, imagem) VALUES (?, ?, ?, ?)",
                (nome, preco, categoria, imagem)
            )
        except sqlite3.IntegrityError:
            pass

    conexao.commit()
    conexao.close()
    print("Banco populado automaticamente!")

def gerar_cupom(pedido_id, cliente, itens, subtotal, taxa, total, data_hora):
    L = 42 # caracteres para simular 80mm

    def centralizar(texto):
        return texto.center(L)

    def linha_tracejada():
        return "-" * L

    def coluna(esquerda, direita):
        espacos = L - len(esquerda) - len(direita)
        return esquerda + " " * espacos + direita

    linhas = []

    # cabeçalho
    linhas.append(centralizar("BK BRASIL OPERACAO E ASSESSORIA"))
    linhas.append(centralizar("A RESTAURANTES S.A"))
    linhas.append(centralizar("AV. PAULISTA, 1000 - BELA VISTA"))
    linhas.append(centralizar("SAO PAULO, SP 01310-100"))
    linhas.append(centralizar("CNPJ: 13.574.594/0001-89"))
    linhas.append(centralizar("IE: 142405765111  IM: 0012345"))
    linhas.append(linha_tracejada())
    linhas.append(centralizar("Auxiliar da Nota Fiscal"))
    linhas.append(centralizar("de Consumidor Eletronica"))
    linhas.append(linha_tracejada())

    # pedido
    linhas.append(centralizar(f"Pedido #{pedido_id}"))
    linhas.append(centralizar(data_hora))
    linhas.append(linha_tracejada())

    # colunas dos itens
    linhas.append(coluna("DESCR", "QTD    VL UNIT    TOTAL"))
    linhas.append(linha_tracejada())

    total_itens = 0
    for item in itens:
        total_itens += item['quantidade']
        nome = item['nome'][:18]
        qtd = f"{item['quantidade']}.000un"
        vl_unit = f"{item['preco']:.2f}".replace('.', ',')
        vl_total = f"{item['preco'] * item['quantidade']:.2f}".replace('.', ',')
        linhas.append(nome)
        linhas.append(coluna(f"  {qtd}", f"{vl_unit}    {vl_total}"))

    linhas.append(linha_tracejada())

    # totais
    linhas.append(coluna("QTD. TOTAL DE ITENS", str(total_itens)))
    linhas.append(coluna("VALOR TOTAL RS", f"RS {subtotal:.2f}".replace('.', ',')))
    linhas.append(coluna("DESCONTO", "RS 0,00"))
    linhas.append(coluna("TAXA DE SERVICO", f"RS {taxa:.2f}".replace('.', ',')))
    linhas.append(coluna("VALOR A PAGAR", f"RS {total:.2f}".replace('.', ',')))
    linhas.append(linha_tracejada())

    # forma de pagamento (ficticia por enquanto)
    linhas.append(coluna("FORMA DE PAGAMENTO", "Valor Pago"))
    linhas.append(coluna("CARTAO DEBITO", f"RS {total:.2f}".replace('.', ',')))
    linhas.append(linha_tracejada())

    # painel de retirada
    linhas.append(centralizar("PAINEL DE RETIRADA - VOCE SERA CHAMADO POR:"))
    linhas.append("")
    nome_painel = cliente.upper() if cliente else "CONSUMIDOR"
    linhas.append(centralizar(f"*** {nome_painel} ***"))
    linhas.append("")
    linhas.append(linha_tracejada())

    # tributos
    trib_fed = subtotal * 0.0420
    trib_est = subtotal * 0.1800
    trib_total = trib_fed + trib_est
    linhas.append(centralizar("Valor aproximado dos tributos"))
    linhas.append(coluna("deste cupom", f"RS {trib_total:.2f}".replace('.', ',')))
    linhas.append(coluna(f"Fed = RS {trib_fed:.2f} (4,20%)".replace('.', ','),
                         f"Est = RS {trib_est:.2f} (18,00%)".replace('.', ',')))
    linhas.append(linha_tracejada())

    # consumidor
    consumidor = cliente.upper() if cliente else "NAO INFORMADO"
    linhas.append(centralizar(f"CONSUMIDOR: {consumidor}"))
    linhas.append(linha_tracejada())

    # rodapé
    linhas.append("")
    linhas.append(centralizar("Obrigado pela preferencia!"))
    linhas.append(centralizar("Volte sempre!"))
    linhas.append("")

    # salva o arquivo
    texto_cupom = "\n".join(linhas)
    nome_arquivo = f"notas_pedidos/pedido_{pedido_id}.txt"
    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write(texto_cupom)

    return nome_arquivo

@app.route("/pedido", methods=["POST"])
def finalizar_pedido():
    dados = request.get_json()
    cliente = dados.get("cliente", "")
    itens = dados.get("itens", [])

    # verifica se o carinho não está vazio
    if not itens:
        return jsonify({"erro": "Carrinho vazio!"}), 400

    # calcula o total
    subtotal = sum(item["preco"] * item["quantidade"] for item in itens)
    taxa = 5.00
    total = subtotal + taxa

    # pega a data e hora atual
    from datetime import datetime
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    conexao, cursor = conectar_banco()

    # salva o pedido na tabela pedidos
    cursor.execute(
        "INSERT INTO pedidos (cliente, total, data_hora) VALUES (?, ?, ?)",
        (cliente, total, data_hora)
    )
    pedido_id = cursor.lastrowid # pega o id do pedido recém criado

    # salva cada item na tabela itens_pedido
    for item in itens:
        cursor.execute(
            "INSERT INTO itens_pedido (pedido_id, produto_id, nome, preco, quantidade) VALUES (?, ?, ?, ?, ?)",
            (pedido_id, item["id"], item["nome"], item["preco"], item["quantidade"])
        )
    
    conexao.commit()
    conexao.close()

    gerar_cupom(pedido_id, cliente, itens, subtotal, taxa, total, data_hora)

    return jsonify({
        "mensagem": f"Pedido #{pedido_id} finalizado com sucesso!",
        "total": total
    }), 201
if __name__ == "__main__":
    conectar_banco()
    popular_banco_se_vazio()
    app.run(debug=True)