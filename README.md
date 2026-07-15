#  Burger King PDV - Sistema de Ponto de Venda

Projeto pessoal de portfólio que simula o sistema de PDV (Ponto de Venda) do Burger King.  
Desenvolvido com Python, Flask, HTML, CSS e JavaScript.

---

##  Tecnologias utilizadas

- Python 3 + Flask (backend/API)
- SQLite (banco de dados)
- HTML + CSS + JavaScript (frontend)

---

##  Estrutura do projeto

sistema_burgerking/
├── app.py              # Backend Flask com as rotas da API
├── drive_thru.db       # Banco de dados SQLite (gerado automaticamente)
├── notas_pedidos/      # Cupons gerados auto (ignorado pelo git)
├── templates/
│   └── index.html      # Interface principal do PDV
├── static/
│   ├── img/
│   │   ├── lanches/
│   │   ├── bebidas/
│   │   ├── sobremesas/
│   │   └── molhos/
│   ├── style.css       # Estilização da interface
│   └── script.js       # Lógica do frontend
├── .gitignore
└── README.md

---

##  O que já foi feito

- [x] Banco de dados SQLite com tabela de produtos
- [x] CRUD de produtos via API REST (Flask)
  - [x] Cadastrar produto
  - [x] Listar produtos
  - [x] Remover produto
- [x] Estrutura do frontend (HTML base)
- [x] Pack de imagens do cardápio
- [x] Estilização completa do PDV (style.css)
- [x] Grid de produtos com cards clicáveis (script.js)
- [x] Filtro de produtos por categoria
- [x] Carrinho de pedidos (adicionar/remover itens)
- [x] Cálculo de subtotal e total
- [x] Simulação de processamento de pagamento
- [x] Botão de finalizar pedido (salva no banco com status Pendente/Pago)
- [x] Nome do cliente no pedido (opcional)
- [x] Geração de cupom .txt simulando impressora térmica 80mm
- [x] Banco de dados populado automaticamente na primeira execução
- [x] Seleção de forma de pagamento (Débito, Crédito, PIX, Dinheiro)


---

## Próximos passos

- [ ] Criar função cancelar pedido, e zerar as seleções.
- [ ] Histórico / relatório de vendas
- [ ] Imprimir ou mostrar na tela da cozinha o pedido, no caso o que precisa ser preparado.

> Sempre que fizer alguma dessas tarefas, não esquecer de atualizar o README

---

## ▶ Como rodar o projeto


1. Clone o repositório

2. Crie e ative o ambiente virtual
\`\`\`bash
python3 -m venv venv
source venv/bin/activate
\`\`\`

3. Instale as dependências
\`\`\`bash
pip install -r requirements.txt
\`\`\`

4. Rode o servidor
\`\`\`bash
python app.py
\`\`\`
O banco de dados é criado e populado automaticamente na primeira execução.

5. Acesse no navegador
\`\`\`
http://127.0.0.1:5000
\`\`\`