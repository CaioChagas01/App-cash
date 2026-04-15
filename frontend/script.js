const API_URL = "COLE_AQUI_URL_DO_RENDER";

async function calcular() {
    const tipo = document.getElementById("tipo").value;
    const valor = parseFloat(document.getElementById("valor").value);

    const res = await fetch(API_URL + "/cashback", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            tipo_cliente: tipo,
            valor: valor
        })
    });

    const data = await res.json();
    document.getElementById("resultado").innerText =
        "Cashback: R$ " + data.cashback.toFixed(2);

    carregarHistorico();
}

async function carregarHistorico() {
    const res = await fetch(API_URL + "/historico");
    const data = await res.json();

    const lista = document.getElementById("historico");
    lista.innerHTML = "";

    data.forEach(item => {
        const li = document.createElement("li");
        li.innerText =
            `${item.tipo_cliente} - R$${item.valor} → R$${item.cashback}`;
        lista.appendChild(li);
    });
}

carregarHistorico();