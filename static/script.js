let pedido = [];

async function carregarProdutos() {
    const resposta = await fetch('/produtos');
    const produtos = await resposta.json();
    montarGrid(produtos);
}

function montarGrid(produtos) {
    const grid = document.getElementById('grid-produtos');
    grid.innerHTML = '';

    produtos.forEach(produto => {
        const card = document.createElement('div');
        card.classList.add('card-produto');
        card.innerHTML = `
            <img src="/static/img/${produto.categoria}/${produto.imagem}" 
                 onerror="this.src='/static/img/default.png'" 
                 alt="${produto.nome}">
            <span>${produto.nome}</span>
            <strong>R$ ${produto.preco.toFixed(2).replace('.', ',')}</strong>
        `;
        card.addEventListener('click', () => adicionarAoPedido(produto));
        grid.appendChild(card);
    });
}

// gerencia 

function adicionarAoPedido(produto) {
    const existente = pedido.find(item => item.id === produto.id);
    if (existente) {
        existente.quantidade++;
    } else {
        pedido.push({ ...produto, quantidade: 1 });
    }
    atualizarPainel();
}

function removerDoPedido(id) {
    pedido = pedido.filter(item => item.id !== id);
    atualizarPainel();
}

function atualizarPainel() {
    const lista = document.getElementById('lista-pedido');
    const totalItens = document.getElementById('total-itens');
    const subtotalEl = document.getElementById('subtotal');
    const totalEl = document.getElementById('total');

    lista.innerHTML = '';

    let subtotal = 0;

    pedido.forEach(item => {
        subtotal += item.preco * item.quantidade;

        const div = document.createElement('div');
        div.classList.add('item-pedido');
        div.innerHTML = `
            <span>${item.quantidade}x ${item.nome}</span>
            <span>R$ ${(item.preco * item.quantidade).toFixed(2).replace('.', ',')}</span>
            <button onclick="removerDoPedido(${item.id})">✕</button>
        `;
        lista.appendChild(div);
    });

    const taxa = subtotal > 0 ? 5.00 : 0;
    const total = subtotal + taxa;

    totalItens.textContent = `${pedido.length} ${pedido.length === 1 ? 'item' : 'itens'}`;
    subtotalEl.textContent = `R$ ${subtotal.toFixed(2).replace('.', ',')}`;
    document.getElementById('taxa').textContent = `R$ ${taxa.toFixed(2).replace('.', ',')}`;
    totalEl.textContent = `R$ ${total.toFixed(2).replace('.', ',')}`;
}

// busca em tempo real

document.getElementById('busca').addEventListener('input', async function () {
    const termo = this.value.toLowerCase();
    const resposta = await fetch('/produtos');
    const produtos = await resposta.json();
    const filtrados = produtos.filter(p => p.nome.toLowerCase().includes(termo));
    montarGrid(filtrados);
});



carregarProdutos();