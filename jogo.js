"use strict";

// Roda o main.py do trabalho, sem editar o arquivo, dentro do Pyodide.
// O main.py usa input(), que bloqueia. No navegador nao da para bloquear, entao,
// so na memoria, cada "input(" vira "await ainput(" antes de executar. O main.py
// nao tem funcoes (def), entao o await no nivel do modulo e aceito.

const saida = document.getElementById("saida");
const carregando = document.getElementById("carregando");
const form = document.getElementById("entrada-form");
const campo = document.getElementById("entrada");
const rotulo = document.getElementById("prompt");
const atalhos = document.getElementById("atalhos");
const fim = document.getElementById("fim");
const recomecar = document.getElementById("recomecar");

let resolverEntrada = null;
let promptAtual = "";

// ---------- escrita na tela ----------

// Pinta X e O so nas linhas do tabuleiro ("Linha 1  X | O |  ") e em "Vez do jogador X".
function pintar(texto) {
  const frag = document.createDocumentFragment();
  let corpo = texto;
  const tab = /^(Linha \d)(.*)$/.exec(texto);
  const vez = /^(Vez do jogador )([XO])$/.exec(texto);
  if (tab) {
    frag.append(tab[1]);
    corpo = tab[2];
  } else if (vez) {
    frag.append(vez[1]);
    corpo = vez[2];
  } else {
    frag.append(texto);
    return frag;
  }
  for (const c of corpo) {
    if (c === "X" || c === "O") {
      const s = document.createElement("span");
      s.className = c === "X" ? "x" : "o";
      s.textContent = c;
      frag.append(s);
    } else {
      frag.append(c);
    }
  }
  return frag;
}

function linha(texto, classe) {
  const div = document.createElement("div");
  div.className = "linha" + (classe ? " " + classe : "");
  if (classe) div.textContent = texto;
  else div.append(pintar(texto));
  saida.append(div);
  saida.scrollTop = saida.scrollHeight;
  return div;
}

function ecoDaResposta(prompt, valor) {
  const div = document.createElement("div");
  div.className = "linha";
  div.append(prompt);
  const v = document.createElement("span");
  v.className = "digitado";
  v.textContent = valor;
  div.append(v);
  saida.append(div);
  saida.scrollTop = saida.scrollHeight;
}

// ---------- entrada do jogador ----------

// Respostas rapidas para quem usa o celular, deduzidas do texto do proprio prompt.
function atalhosDoPrompt(prompt) {
  const faixa = /\((\d) a (\d)\)/.exec(prompt);
  if (faixa) {
    const lista = [];
    for (let n = Number(faixa[1]); n <= Number(faixa[2]); n++) lista.push([String(n), String(n)]);
    return lista;
  }
  if (/\(s\/n\)/.test(prompt)) return [["s", "Sim (s)"], ["n", "Não (n)"]];
  return [];
}

function enviar(valor) {
  if (!resolverEntrada) return;
  const resolver = resolverEntrada;
  resolverEntrada = null;
  ecoDaResposta(promptAtual, valor);
  form.hidden = true;
  campo.value = "";
  atalhos.replaceChildren();
  resolver(valor);
}

// Chamada pelo Python: mostra o prompt e espera a resposta do jogador.
function pedirEntrada(prompt) {
  return new Promise((resolver) => {
    promptAtual = prompt;
    resolverEntrada = resolver;
    rotulo.textContent = prompt;
    atalhos.replaceChildren();
    for (const [valor, rotuloBotao] of atalhosDoPrompt(prompt)) {
      const b = document.createElement("button");
      b.type = "button";
      b.className = "botao";
      b.textContent = rotuloBotao;
      b.addEventListener("click", () => enviar(valor));
      atalhos.append(b);
    }
    form.hidden = false;
    // Em telas de toque, focar o campo abriria o teclado a cada jogada.
    if (window.matchMedia("(pointer: fine)").matches) campo.focus();
  });
}

form.addEventListener("submit", (e) => {
  e.preventDefault();
  enviar(campo.value);
});
recomecar.addEventListener("click", () => window.location.reload());

// ---------- execucao ----------

async function iniciar() {
  const pyodide = await loadPyodide({ indexURL: "./pyodide/" });
  pyodide.setStdout({ batched: (texto) => linha(texto) });
  pyodide.setStderr({ batched: (texto) => linha(texto, "erro") });

  const ambiente = pyodide.globals.get("dict")();
  ambiente.set("pedir_entrada_js", pedirEntrada);
  pyodide.runPython(
    [
      "import sys",
      "async def ainput(prompt=''):",
      "    sys.stdout.flush()",
      "    return await pedir_entrada_js(prompt)",
    ].join("\n"),
    { globals: ambiente }
  );

  const resposta = await fetch("main.py");
  if (!resposta.ok) throw new Error("nao consegui carregar o main.py (" + resposta.status + ")");
  const fonte = (await resposta.text()).replace(/\binput\(/g, "await ainput(");

  carregando.remove();
  await pyodide.runPythonAsync(fonte, { globals: ambiente });
  fim.hidden = false;
  recomecar.focus();
}

iniciar().catch((erro) => {
  if (carregando.isConnected) carregando.remove();
  linha("Não foi possível iniciar o jogo: " + erro.message, "erro");
  linha("Recarregue a página para tentar de novo.", "suave");
});
