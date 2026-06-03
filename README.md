# 🍔 Burger King PDV - Sistema de Ponto de Venda

Projeto pessoal de portfólio que simula o sistema de PDV (Ponto de Venda) do Burger King.  
Desenvolvido com Python, Flask, HTML, CSS e JavaScript.

---

## 🛠️ Tecnologias utilizadas

- Python 3 + Flask (backend/API)
- SQLite (banco de dados)
- HTML + CSS + JavaScript (frontend)

---

## 📁 Estrutura do projeto

sistema_burgerking/
├── app.py              # Backend Flask com as rotas da API
├── drive_thru.db       # Banco de dados SQLite (gerado automaticamente)
├── templates/
│   └── index.html      # Interface principal do PDV
├── static/
│   ├── img/
│   │   ├── lanches/
│   │   ├── bebidas/
│   │   ├── sobremesas/
│   │   └── molho/
│   ├── style.css       # Estilização da interface
│   └── script.js       # Lógica do frontend
├── .gitignore
└── README.md

---

## ✅ O que já foi feito

- [x] Banco de dados SQLite com tabela de produtos
- [x] CRUD de produtos via API REST (Flask)
  - [x] Cadastrar produto
  - [x] Listar produtos
  - [x] Remover produto
- [x] Estrutura do frontend (HTML base)
- [x] Pac de imagens do cardápio

---

## 🚧 Próximos passos

- [ ] Estilização completa do PDV (style.css)
- [ ] Grid de produtos com cards clicáveis (script.js)
- [ ] Carrinho de pedidos (adicionar/remover itens)
- [ ] Cálculo de subtotal e total
- [ ] Botão de finalizar pedido
- [ ] Tabela de pedidos no banco de dados
- [ ] Histórico / relatório de vendas

> ⚠️ Sempre que fizer alguma dessas tarefas, não esquecer de atualizar o README

---

## ▶️ Como rodar o projeto


# 1. Crie e ative o ambiente virtual
python3 -m venv venv
source venv/bin/activate

# 2. Instale as dependências
pip install flask

# 3. Rode o servidor
python app.py

# 4. Acesse no navegador
http://127.0.0.1:5000
