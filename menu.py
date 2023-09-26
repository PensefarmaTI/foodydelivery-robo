from datetime import datetime
data = datetime.now().strftime("%d/%m/%Y")

author = 'Michel Rodrigues Mota - TI'
divisao = '-'
tamanho_menu = 80
divisao_continua = divisao*tamanho_menu
nome_robo = 'INTEGRAÇÃO FOODY'
data_in_menu = divisao + f'  {nome_robo}' + f'data: {data}  '.rjust(tamanho_menu-4-len(nome_robo)) + divisao
espaco_branco_menu = divisao + ' '.center(tamanho_menu-2) + divisao
author_in_menu = divisao + f'Author: {author}  '.rjust(tamanho_menu-2) + divisao

def banner():
    print(divisao_continua)
    print(data_in_menu)
    print(espaco_branco_menu)
    print(espaco_branco_menu)
    print(author_in_menu)
    print(divisao_continua)

def menu_opcoes():
    print()
    print('\t1 - Iniciar robo')
    print('\t2 - Visualização de prevendas não enviadas')
    # print('\t3 - Filtrar')
    print('\t3 - Resetar Enviado Null')
    print('\t0 - Sair')
    print()

def menu():
    banner()
    menu_opcoes()