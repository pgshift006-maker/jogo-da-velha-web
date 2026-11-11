# Jogo da Velha no navegador

Versão jogável, em uma página web, do jogo da velha em Python feito como trabalho de programação (dois jogadores, no terminal).

**Jogar:** https://pgshift006-maker.github.io/jogo-da-velha-web/

## Como funciona

O jogo original é um programa de terminal, que lê as jogadas com `input()`. Esta página não reescreve o jogo: ela executa o próprio `main.py` dentro do navegador, usando o [Pyodide](https://pyodide.org/) (Python compilado para WebAssembly).

1. O navegador carrega o Pyodide (pasta `pyodide/`, sem depender de CDN).
2. A página busca o `main.py` e, **somente na memória**, troca cada `input(` por `await ainput(`. O arquivo `main.py` do repositório não é alterado.
3. `ainput` mostra o texto do pedido na tela e espera o jogador responder (digitando ou tocando nos botões de resposta rápida).
4. Tudo que o programa imprime aparece no terminal da página, com X e O coloridos nas linhas do tabuleiro.

Conferência: uma sessão completa (vitória, revanche, empate, placar e estatísticas) gera exatamente a mesma saída no Pyodide e no Python instalado no computador, linha por linha.

Nada que o jogador digita sai do navegador; não há servidor nem coleta de dados.

## Arquivos

| Arquivo | Função |
|---|---|
| `index.html`, `estilo.css` | Página e aparência |
| `jogo.js` | Carrega o Pyodide, adapta o `input()` e escreve a saída na tela |
| `main.py` | O jogo, sem alterações |
| `pyodide/` | Pyodide 0.27.7 (`pyodide.js`, `pyodide.asm.js`, `pyodide.asm.wasm`, `python_stdlib.zip`, `pyodide-lock.json`), sem modificações |

## Rodar no próprio computador

A página precisa ser servida por HTTP (abrir o `index.html` direto do disco não funciona):

```bash
python -m http.server 8000
```

Depois abra http://localhost:8000.

## Atualizar o jogo

Troque o `main.py` pela nova versão. Como a adaptação do `input()` usa `await` no nível do arquivo, o jogo precisa chamar `input()` fora de funções (`def`); dentro de uma função o Python recusa o `await`.

## Licenças

O Pyodide é distribuído sob a licença MPL 2.0 ([código-fonte](https://github.com/pyodide/pyodide)) e está incluído aqui sem modificações.
