const API_URL = "https://app-cash-api.onrender.com";

async function calcular() {
  const valor = document.getElementById("valor").value;
  const tipo = document.getElementById("tipo").value;

  const res = await fetch(API_URL + "/cashback", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      valor: Number(valor),
      tipo_cliente: tipo
    })
  });

  const data = await res.json();

  document.getElementById("resultado").innerText =
    "Cashback: " + data.cashback;
}