# Jogo da Velha no terminal
# Trabalho da 2a Avaliacao - Coding - Prof. Tiago Martins Ribeiro

# ==================== SECAO 1: VARIAVEIS E MATRIZ (Marlon) ====================
# O tabuleiro e uma matriz 3x3: tabuleiro[i][j], em que i e a linha e j a coluna
tabuleiro = [
    [" ", " ", " "],
    [" ", " ", " "],
    [" ", " ", " "]
]

simbolo = "X"          # simbolo de quem joga agora
jogadas = 0            # quantas casas ja foram marcadas no tabuleiro
programa_ativo = True  # controla o menu principal

# ==================== SECAO 2: VARIAVEIS DO PLACAR (Francisco) ====================
# O placar fica fora do menu para acumular os resultados de todas as partidas
vitorias_x = 0   # partidas vencidas pelo jogador X
vitorias_o = 0   # partidas vencidas pelo jogador O
empates = 0      # partidas que terminaram sem vencedor
jogar_novamente = False  # vira True quando os jogadores pedem revanche

# ==================== SECAO 3: MENU PRINCIPAL (Marlon) ====================
# Este while mantem o menu aberto ate o jogador escolher Sair
while programa_ativo == True:
    if jogar_novamente == True:
        # Revanche: pula o menu e comeca outra partida direto (Francisco)
        opcao = 1
        opcao_valida = True
        jogar_novamente = False
    else:
        print()
        print("===== JOGO DA VELHA =====")
        print("1 - Jogar")
        print("2 - Ver regras")
        print("3 - Ver placar")
        print("4 - Sair")

        # Repete a leitura ate a opcao ser valida
        opcao_valida = False
    while opcao_valida == False:
        entrada = input("Escolha uma opcao (1 a 4): ")
        # Compara o texto digitado com cada opcao: "1", "2", "3" e "4"
        for n in range(1, 5):
            if entrada == str(n):
                opcao_valida = True
                opcao = n
        if opcao_valida == False:
            # Mostra o que foi digitado para o jogador perceber o erro
            if entrada == "":
                print("Opcao invalida! Voce nao digitou nada. Digite um numero de 1 a 4.")
            else:
                print("Opcao invalida! Voce digitou '" + entrada + "'. Digite um numero de 1 a 4.")

    if opcao == 1:
        # ==================== SECAO 4: PARTIDA ====================
        # Limpeza do tabuleiro antes de cada partida (Francisco)
        # O for de fora percorre as linhas e o de dentro apaga cada casa
        for i in range(3):
            for j in range(3):
                tabuleiro[i][j] = " "
        jogadas = 0

        # Controle da partida (PG)
        partida_ativa = True   # vira False quando alguem vence ou quando empata
        vencedor = ""          # guarda "X" ou "O"; continua "" se empatar
        simbolo = "X"          # toda partida comeca com o jogador X

        # Este while repete as jogadas ate a partida terminar
        while partida_ativa == True:
            # Exibicao do tabuleiro (Marlon)
            print()
            print("         1   2   3   (colunas)")
            # O for de fora percorre as linhas da matriz
            for i in range(3):
                texto_linha = "Linha " + str(i + 1) + " "
                # O for de dentro percorre as colunas da linha i
                for j in range(3):
                    texto_linha = texto_linha + " " + tabuleiro[i][j] + " "
                    if j < 2:
                        texto_linha = texto_linha + "|"
                print(texto_linha)
                if i < 2:
                    print("        ---+---+---")
            print()

            print("Vez do jogador " + simbolo)

            # Leitura da jogada com validacao (Marlon)
            # Este while repete a jogada inteira se a casa estiver ocupada
            casa_livre = False
            while casa_livre == False:
                # Repete a leitura ate a linha ser valida
                linha_valida = False
                while linha_valida == False:
                    entrada = input("Escolha a linha (1 a 3): ")
                    # Compara o texto digitado com "1", "2" e "3"
                    for n in range(1, 4):
                        if entrada == str(n):
                            linha_valida = True
                            linha = n - 1  # indice da matriz (0 a 2)
                    if linha_valida == False:
                        if entrada == "":
                            print("Entrada invalida! Voce nao digitou nada. Digite um numero de 1 a 3.")
                        else:
                            print("Entrada invalida! Voce digitou '" + entrada + "'. Digite um numero de 1 a 3.")
                    else:
                        # Confere se a linha escolhida ainda tem alguma casa vazia
                        casas_vazias = 0
                        for j in range(3):
                            if tabuleiro[linha][j] == " ":
                                casas_vazias = casas_vazias + 1
                        if casas_vazias == 0:
                            print("A linha " + str(linha + 1) + " esta cheia! Escolha outra linha.")
                            linha_valida = False

                # Repete a leitura ate a coluna ser valida
                coluna_valida = False
                while coluna_valida == False:
                    entrada = input("Escolha a coluna (1 a 3): ")
                    # Compara o texto digitado com "1", "2" e "3"
                    for n in range(1, 4):
                        if entrada == str(n):
                            coluna_valida = True
                            coluna = n - 1  # indice da matriz (0 a 2)
                    if coluna_valida == False:
                        if entrada == "":
                            print("Entrada invalida! Voce nao digitou nada. Digite um numero de 1 a 3.")
                        else:
                            print("Entrada invalida! Voce digitou '" + entrada + "'. Digite um numero de 1 a 3.")

                # So aceita a jogada se a casa escolhida estiver vazia
                if tabuleiro[linha][coluna] == " ":
                    casa_livre = True
                else:
                    # Informa qual casa foi escolhida e quem ja marcou nela
                    print("Casa ocupada! A linha " + str(linha + 1) + ", coluna " + str(coluna + 1) + " ja esta marcada com " + tabuleiro[linha][coluna] + ". Escolha outra jogada.")

            tabuleiro[linha][coluna] = simbolo
            jogadas = jogadas + 1

            # Verificacao de vitoria e empate e troca de jogador (PG)
            # So o simbolo que acabou de jogar pode ter completado uma sequencia

            # Linhas: o for de fora escolhe a linha i, o de dentro conta as casas
            for i in range(3):
                marcadas = 0
                for j in range(3):
                    if tabuleiro[i][j] == simbolo:
                        marcadas = marcadas + 1
                if marcadas == 3:
                    vencedor = simbolo

            # Colunas: o for de fora escolhe a coluna j, o de dentro desce as linhas
            for j in range(3):
                marcadas = 0
                for i in range(3):
                    if tabuleiro[i][j] == simbolo:
                        marcadas = marcadas + 1
                if marcadas == 3:
                    vencedor = simbolo

            # Diagonais: na principal a linha e a coluna sao iguais (0,0 1,1 2,2);
            # na secundaria a coluna e 2 menos a linha (0,2 1,1 2,0)
            diagonal_principal = 0
            diagonal_secundaria = 0
            for i in range(3):
                if tabuleiro[i][i] == simbolo:
                    diagonal_principal = diagonal_principal + 1
                if tabuleiro[i][2 - i] == simbolo:
                    diagonal_secundaria = diagonal_secundaria + 1
            if diagonal_principal == 3 or diagonal_secundaria == 3:
                vencedor = simbolo

            if vencedor != "":
                partida_ativa = False
            # Com as 9 casas marcadas, nao ha mais jogada possivel
            elif jogadas == 9:
                partida_ativa = False
            else:
                # Troca de jogador: depois de X joga O, depois de O joga X
                if simbolo == "X":
                    simbolo = "O"
                else:
                    simbolo = "X"

        # Exibe o tabuleiro final da partida
        print()
        print("         1   2   3   (colunas)")
        # Mesmos lacos da exibicao: linhas por fora, colunas por dentro
        for i in range(3):
            texto_linha = "Linha " + str(i + 1) + " "
            for j in range(3):
                texto_linha = texto_linha + " " + tabuleiro[i][j] + " "
                if j < 2:
                    texto_linha = texto_linha + "|"
            print(texto_linha)
            if i < 2:
                print("        ---+---+---")
        print()
        print("Fim da partida.")

        # Resultado da partida (PG)
        if vencedor != "":
            print("O jogador " + vencedor + " venceu!")
        else:
            print("Deu velha! A partida terminou empatada.")

        # Placar acumulado (Francisco)
        # Soma 1 para quem venceu ou para os empates
        if vencedor == "X":
            vitorias_x = vitorias_x + 1
        elif vencedor == "O":
            vitorias_o = vitorias_o + 1
        else:
            empates = empates + 1
        print("Placar: X " + str(vitorias_x) + " x " + str(vitorias_o) + " O | Empates: " + str(empates))

        # Serie de melhor de 3 ou 5 (Francisco) - desafio extra, ainda nao feito

        # Jogar novamente (Francisco)
        # Repete a pergunta ate a resposta ser s ou n
        resposta_valida = False
        while resposta_valida == False:
            resposta = input("Jogar novamente? (s/n): ")
            if resposta == "s" or resposta == "S":
                jogar_novamente = True
                resposta_valida = True
            elif resposta == "n" or resposta == "N":
                jogar_novamente = False
                resposta_valida = True
            else:
                print("Resposta invalida! Digite s para sim ou n para nao.")

    elif opcao == 2:
        print()
        print("===== REGRAS =====")
        print("Dois jogadores se alternam marcando X e O em casas vazias.")
        print("Para jogar, informe a linha e a coluna da casa desejada.")
        print("Vence quem completar uma linha, uma coluna ou uma diagonal.")
        print("Se o tabuleiro encher sem vencedor, a partida termina empatada.")

    elif opcao == 3:
        # Exibicao do placar (Francisco)
        print()
        print("===== PLACAR =====")
        print("Jogador X: " + str(vitorias_x))
        print("Jogador O: " + str(vitorias_o))
        print("Empates: " + str(empates))

    else:
        # Estatisticas da sessao ao sair (Francisco)
        # O total e a soma dos tres contadores do placar
        total_partidas = vitorias_x + vitorias_o + empates
        print()
        print("===== ESTATISTICAS DA SESSAO =====")
        if total_partidas == 0:
            print("Nenhuma partida foi disputada nesta sessao.")
        else:
            print("Partidas disputadas: " + str(total_partidas))
            print("Vitorias de X: " + str(vitorias_x))
            print("Vitorias de O: " + str(vitorias_o))
            print("Empates: " + str(empates))
        print("Ate a proxima!")
        programa_ativo = False
