from logic import *

sair = False
while not sair:
    menu()
    opcao = int(input('Escolha uma das opções acima: '))
    if opcao == 1:
        loja = str(input('Selecione a loja que deseja iniciar o robo (* para todas): '))
        inicia_robo(loja)   
    elif opcao == 2:
        loja = int(input('Selecione a loja que deseja visualizar os prevendas ainda não enviados: '))
        filtra_dados_prevenda(loja)
        visualizacao_objeto(prevenda_pedido_list, loja)
        limpa_lista_prevendas()
    elif opcao == 4:
        loja = int(input('Selecione a loja que deseja resetar os prevendas para NULL: '))
        reset_enviado_field(loja)
    elif opcao == 0:
        sair = True



conexao.close()