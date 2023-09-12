from model import Prevenda_pedido
from prevenda_methods import *
from menu import menu
import requests
import time
import json

inicializado = False
timezone = '-03:00'
filter_timer = 10

def filtra_dados_prevenda(loja, lista):
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
            
            lista.append(prevenda_pedido)
    except Exception as exp:
        print(exp)        

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


def inicia_robo(lista, lojas = '*'):
    inicializado = True
    while inicializado:
        start_time = time.time()
        if lojas == '*':
            lojas_list = get_lojas_list()
        else:
            # tem que ser uma string de lista de lojas de parametro
            lojas_list = lojas.split(',')

        for loja in lojas_list:
            filtra_dados_prevenda(loja, lista)
            if not lista:
                continue
            visualizacao_objeto(lista, loja)
            time.sleep(1)
            for prevenda in lista:
                envia_dados_foodydelivery(json.dumps(prevenda), loja, lista[lista.index(prevenda)]['id'] )
    
        end_time = time.time()
        elapsed_time = end_time - start_time
        # system('cls')
        print(f"\n\nTempo decorrido: {elapsed_time} segundos")
        time.sleep(filter_timer)


