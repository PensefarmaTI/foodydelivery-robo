from model import Prevenda_pedido
from prevenda_methods import *
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
