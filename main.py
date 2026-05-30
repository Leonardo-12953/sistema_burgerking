import sqlite3

# CONFIGURAÇÃO E CONEXÃO DO BANCO DE DADOS
def conectar_banco():
    conexao = sqlite3.connect("drive_thru.db")
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            preco REAL NOT NULL
        )
    """)
    conexao.commit()
    return conexao, cursor


# FUNÇÕES DO ADMINISTRADOR (C.R.U.D)

def cadastrar_produto(nome, preco):
    conexao, cursor = conectar_banco()
    try:
        cursor.execute("INSERT INTO produtos (nome, preco) VALUES (?, ?)", (nome, preco))
        conexao.commit()
        print(f"🎉 Produto '{nome}' cadastrado com sucesso!")
    except sqlite3.IntegrityError:
        print(f"⚠️ Erro: O produto '{nome}' já está cadastrado no menu.")
    finally:
        conexao.close()


def listar_produtos():
    conexao, cursor = conectar_banco()
    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()
    conexao.close()
    
    if not produtos:
        print("\nℹ️ O menu está vazio.")
        return
        
    print("\n" + "="*39)
    print("         MENU ATUAL")
    print("="*39)
    for prod in produtos:
        nome = prod[1]
        preco = prod[2]

        # Se o nome passar de 18 caracteres vai truncar
        if len(nome) > 18:
            nome = nome[:17] + "…"

        print(f"ID: {prod[0]} | {nome:<18} - R$ {preco:>7.2f}")
    print("="*39 + "\n")


def remover_produto(id_produto):
    conexao, cursor = conectar_banco()
    
    
    cursor.execute("DELETE FROM produtos WHERE id = ?", (id_produto,))
    conexao.commit()

    if cursor.rowcount > 0:
        print(f"🗑️ Produto com ID {id_produto} foi removido.")
    else:
        print(f"❌ Erro: Não foi encontrado nenhum produto com o ID {id_produto}.")   
    conexao.close()


# FLUXO PRINCIPAL DE TESTES (MENU INTERATIVO)

if __name__ == "__main__":
    # Garante que o banco e a tabela existam ao iniciar
    conectar_banco()
    
    print("--- SISTEMA DE GERENCIAMENTO DRIVE-THRU ---")
    
    # Cadastrando os itens iniciais
    cadastrar_produto("Whopper", 35.90)
    cadastrar_produto("Chicken Duplo", 20.90)
    cadastrar_produto("Batata Media", 10.90)
    cadastrar_produto("Mega Stacker Cheddar 3.0", 40.90)

    # listar o que foi cadastrado
    listar_produtos()

    # Remove o produto de ID 2
    remover_produto(2)

    # lista novamente pra ver se o produto saiu
    listar_produtos()
    
    