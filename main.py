from model import Prevenda_pedido
from prevenda_methods import *
from os import system
from menu import menu
import requests
import time
import json

inicializado = False
prevenda_pedido_list = []
timezone = '-03:00'
filter_timer = 10

def filtra_dados_prevenda(loja):
    prevenda_list = get_prevenda(loja, columns='prevenda, observacoes, total_liquido')
    orderDate = datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z")
    try:
        for prevenda in prevenda_list:
            prevenda_pedido = Prevenda_pedido().prevenda_pedido_default
            prevenda_pedido['id'] = str(prevenda[0])
            prevenda_pedido['orderDetails'] = get_details(loja, prevenda_pedido['id'])
            prevenda_pedido['notes'] = str(prevenda[1]) if prevenda[1] is not None else ""
            prevenda_pedido['paymentMethod'] = get_payment_method(loja, prevenda_pedido['id'])['method']
            prevenda_pedido['orderTotal'] = float(prevenda[2])
            prevenda_pedido['date'] = orderDate + timezone
            prevenda_pedido['customer'] = get_client_info(loja, prevenda_pedido['id'])
            prevenda_pedido['deliveryPoint'] = get_address_info(loja, prevenda_pedido['id'])
            
            prevenda_pedido_list.append(prevenda_pedido)
    except Exception as exp:
        print(exp)        
    
    # prevenda_pedido['id'] = '123'
    # print(prevenda_pedido)

def visualizacao_objeto(prevenda_list, loja):
    print(f'\n\nLOJA: {loja}\n')
    for i in range(0, len(prevenda_list)):
        print(f"prevenda {i+1}")
        print(f"id: {prevenda_list[i]['id']}")
        print(f"prevenda_itens: \n{prevenda_list[i]['orderDetails']}")
        print(f"prevenda_obs: {prevenda_list[i]['notes']}")
        print(f"prevenda_pagamento: {prevenda_list[i]['paymentMethod']}")
        print(f"total: {prevenda_list[i]['orderTotal']}")
        print(f"endereço: {prevenda_list[i]['deliveryPoint']['address']}")
        print(f"data: {prevenda_list[i]['date']}\n")

def envia_dados_foodydelivery(order_to_send, loja, prevenda):
    url = 'https://app.foodydelivery.com/rest/1.2/orders'
    dados = order_to_send
    cabecalhos = {"Authorization": get_loja_token(loja), "Content-Type":"application/json"}
    
    response = requests.post(url, data=dados, headers=cabecalhos, timeout=10)

    # Verificando a resposta
    if response.status_code == 200:
        print('Solicitação bem-sucedida!')
        update_enviar_field_to_S(loja, prevenda)
    else:
        print(f'Falha na solicitação com código de status {response.status_code}')


def limpa_lista_prevendas():
    global prevenda_pedido_list
    prevenda_pedido_list = []


def get_loja_token(loja):
    query = f'select TOKEN from PARAMETRIZACOES_LOJAS_FOODY where EMPRESA = {loja}'
    cursor = conexao.cursor()    
    cursor.execute(query)
    for token in cursor:
        return token[0]

def get_lojas_list():
    query = f'select empresa from PARAMETRIZACOES_LOJAS_FOODY'
    cursor = conexao.cursor()
    cursor.execute(query)

    lojas_list = []
    for empresa in cursor:
        lojas_list.append(empresa[0])

    lojas_list.sort()
    return lojas_list

def update(query):
    try:
        cursor = conexao.execute(query)
        conexao.commit()
        print("UPDATE executado com sucesso.")
    except Exception as e:
        print(f"Erro ao executar o UPDATE: {e}")
        conexao.rollback()
    finally:
        cursor.close()

def update_enviar_field_to_S(loja, prevenda):
    query = f"update PDV_PREVENDAS set ENVIADO_FOODY = 'S' where loja = {loja} and data = '{data}' and ORIGEM = 'T' and versao <> 'IFOOD' and PREVENDA={prevenda}"
    update(query)

def reset_enviado_field(loja):
    query = f"update PDV_PREVENDAS set ENVIADO_FOODY = NULL where loja = {loja} and data = '{data}' and ORIGEM = 'T' and versao <> 'IFOOD'"
    update(query)




def inicia_robo(lojas = '*'):
    global inicializado
    inicializado = True
    while inicializado:
        start_time = time.time()

        if lojas == '*':
            lojas_list = get_lojas_list()
        else:
            # tem que ser uma string de lista de lojas de parametro
            lojas_list = lojas.split(',')

        for loja in lojas_list:
            filtra_dados_prevenda(loja)
            if not prevenda_pedido_list:
                continue
            visualizacao_objeto(prevenda_pedido_list, loja)
            time.sleep(1)
            for prevenda in prevenda_pedido_list:
                envia_dados_foodydelivery(json.dumps(prevenda), loja, prevenda_pedido_list[prevenda_pedido_list.index(prevenda)]['id'] )
            limpa_lista_prevendas()
    
        end_time = time.time()
        elapsed_time = end_time - start_time
        # system('cls')
        print(f"\n\nTempo decorrido: {elapsed_time} segundos")
        time.sleep(filter_timer)




# filtra_dados_prevenda(1)
# update_enviar_field_to_S(1, prevenda_pedido_list[0]['id'])
# filtra_dados_prevenda(43)
# visualizacao_objeto(prevenda_pedido_list)
# print(prevenda_pedido_list)
# envia_dados_foodydelivery(json.dumps(prevenda_pedido_list[6]))
# reset_enviado_field(19)
# print(get_loja_token(25))

# inicia_robo('44,1')



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