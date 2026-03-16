
from random import randint

historico = []
tentativas = 0
acertos = 0

while True:
    nrandom = randint(0,2)
    print(nrandom) #apenas p controle sem xitar safado
    print("digite -1 pra sair da gameplay")
    escolha = int(input("faca sua escolha do numero ai"))
    historico.append(escolha)
    if nrandom == escolha:
        print("\n\033[32macertou miseravi")
        acertos += 1
        tentativas +=1
    elif escolha == -1:
        print("\033[minterrompendo a gameplay")
        break
    else:
        print("\n\033[31merrou miseravi ai nao grr")
        tentativas += 1

    porcentagem = (acertos/tentativas*100)
    print("\n\033[mhistorico geral", historico)
    print("\nporcentagem de vitorias = ", porcentagem,"%")