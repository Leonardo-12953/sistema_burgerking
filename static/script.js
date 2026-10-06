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
            onerror="this.onerror=null; this.src='/static/img/default.png'" 
            alt="${produto.nome}">
            <span>${produto.nome}</span>
            <strong>R$ ${produto.preco.toFixed(2).replace('.', ',')}</strong>
        `;
        card.addEventListener('click', () => adicionarAoPedido(produto));
        grid.appendChild(card);
    });
}

const botoesCategoria = document.querySelectorAll('.cat-btn');

botoesCategoria.forEach(botao => {
    botao.addEventListener('click', async () => {

        botoesCategoria.forEach(b => b.classList.remove('ativo'));

        botao.classList.add('ativo');

        const categoria = botao.dataset.categoria;

        const resposta = await fetch('/produtos');
        const produtos = await resposta.json();

        const filtrados = categoria === 'todos'
            ? produtos
            : produtos.filter(p => p.categoria === categoria);

        montarGrid(filtrados);
    });
});

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

document.getElementById('busca').addEventListener('input', async function () {
    const termo = this.value.toLowerCase();
    const resposta = await fetch('/produtos');
    const produtos = await resposta.json();
    const filtrados = produtos.filter(p => p.nome.toLowerCase().includes(termo));
    montarGrid(filtrados);
});

let metodoPagamento = null;

const botoesMetodo = document.querySelectorAll('.btn-metodo');

botoesMetodo.forEach(botao => {
    botao.addEventListener('click', () => {
        botoesMetodo.forEach(b => b.classList.remove('selecionado'));
        botao.classList.add('selecionado');
        metodoPagamento = botao.dataset.metodo;
    });
});

const btn_pagar = document.getElementById('btn-pagar');
btn_pagar.addEventListener('click', async () => {
    
    if (pedido.length === 0) {
        alert('Carrinho vazio!');
        return;
    }

    if (!metodoPagamento) {
        alert('Selecione uma forma de pagamento!');
        return;
    }

    const nomeCliente = document.getElementById('nome-cliente').value.trim();

    const resposta = await fetch('/pedido', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            cliente: nomeCliente,
            metodo_pagamento: metodoPagamento,
            itens: pedido
        })
    });

    const dados = await resposta.json();

    if (resposta.ok) {
        pedido = [];
        metodoPagamento = null;
        botoesMetodo.forEach(b => b.classList.remove('selecionado'));
        document.getElementById('nome-cliente').value = '';
        atualizarPainel();
        alert(`${dados.mensagem}\nTotal: R$ ${dados.total.toFixed(2).replace('.', ',')}`);
    } else {
        alert('Erro ao finalizar o pedido!');
    }
});

function cancelarPedido() {
    
    if (pedido.length === 0) {
        alert("O carrinho já está vazio!");
        return;
    }

    const confirmar = confirm("Tem certeza de que deseja cancelar o pedido e limpar todos os itens?");

    if (confirmar) {
        zerarSelecoes();
        alert("Pedido cancelado e tela limpa com sucesso!");
    }
}

function zerarSelecoes() {
    pedido = [];

    const inputNome = document.getElementById('nome-cliente');
    if (inputNome) inputNome.value = '';

    metodoPagamento = null;
    botoesMetodo.forEach(b => b.classList.remove('selecionado'));

    atualizarPainel();
}

function abrirHistorico() {
    document.getElementById('modal-historico').style.display = 'flex';
    carregarHistorico();
}

function fecharHistorico() {
    document.getElementById('modal-historico').style.display = 'none';
}

async function carregarHistorico() {
    const status = document.getElementById('filtro-status').value;
    const resposta = await fetch(`/pedidos?status=${status}`);
    const pedidos = await resposta.json();

    const conteiner = document.getElementById('lista-historico');
    conteiner.innerHTML = '';

    if (pedidos.length === 0) {
        conteiner.innerHTML = '<p>Nenhum pedido encontrado.</p>';
        return;
    }

    for (const p of pedidos) {
        
        const resItens = await fetch(`/pedidos/${p.id}/itens`);
        const itens = await resItens.json();

        const textoItens = itens.map(i => `${i.quantidade}x ${i.nome}`).join(', ');

        const card = document.createElement('div');
        card.classList.add('card-historico');
        
        let classeStatus = 'status-pago';
        if (p.status === 'Cancelado') classeStatus = 'status-cancelado';
        if (p.status === 'Pendente') classeStatus = 'status-pendente';

        card.innerHTML = `
            <div class="historico-header">
                <strong>Pedido #${p.id}</strong>
                <span class="badge ${classeStatus}">${p.status}</span>
            </div>
            <div class="historico-corpo">
                <p><strong>Cliente:</strong> ${p.cliente || 'Consumidor'}</p>
                <p><strong>Data/Hora:</strong> ${p.data_hora}</p>
                <p><strong>Pagamento:</strong> ${p.metodo_pagamento}</p>
                <p><strong>Itens:</strong> ${textoItens}</p>
                <p><strong>Total:</strong> R$ ${p.total.toFixed(2).replace('.', ',')}</p>
            </div>
            ${p.status === 'Pago' ? `<button onclick="cancelarPedidoNoBanco(${p.id})" class="btn-estornar">Estornar Pedido</button>` : ''}
        `;

        conteiner.appendChild(card);
    }
}

async function cancelarPedidoNoBanco(id) {
    const confirmar = confirm(`Tem certeza que deseja estornar o pedido #${id}?`);
    if (!confirmar) return;

    const resposta = await fetch(`/pedidos/${id}/cancelar`, {
        method: 'POST'
    });

    if (resposta.ok) {
        alert(`Pedido #${id} estornado com sucesso!`);
        carregarHistorico();
    } else {
        alert('Erro ao estornar o pedido.');
    }
}

carregarProdutos();