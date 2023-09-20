from model import Prevenda_pedido
from prevenda_methods import *
from menu import menu
import requests
import time
import json

inicializado = False
lista_prevendas = []
timezone = '-03:00'
filter_timer = 2

def filtra_dados_prevenda(loja):
    global data
    data = datetime.now().strftime("%d/%m/%Y")
    prevenda_list = get_prevenda(loja, columns='prevenda, observacoes, total_liquido')
    orderDate = datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z")
    try:
        for prevenda in prevenda_list:
            prevenda_pedido = Prevenda_pedido().prevenda_pedido_default
            prevenda_pedido['id'] = str(prevenda[0])
            prevenda_pedido['orderDetails'] = f'LOJA {loja}'
            prevenda_pedido['notes'] = f'{prevenda[1]}' if prevenda[1] is not None else f'LOJA {loja}'
            prevenda_pedido['paymentMethod'] = get_payment_method(loja, prevenda_pedido['id'])['method']
            prevenda_pedido['orderTotal'] = float(prevenda[2])
            prevenda_pedido['date'] = orderDate + timezone
            prevenda_pedido['customer'] = get_client_info(loja, prevenda_pedido['id'])
            prevenda_pedido['deliveryPoint'] = get_address_info(loja, prevenda_pedido['id'])
            
            lista_prevendas.append(prevenda_pedido)
    except Exception as exp:
        print(exp)        

def envia_dados_foodydelivery(order_to_send, loja, prevenda):
    prevenda_id = prevenda['id']
    url = 'https://app.foodydelivery.com/rest/1.2/orders'
    dados = order_to_send
    cabecalhos = {"Authorization": get_loja_token(loja), "Content-Type":"application/json"}
    
    response = requests.post(url, data=dados, headers=cabecalhos)

    # Verificando a resposta
    if response.status_code == 200:
        print('Solicitação bem-sucedida!')
        update_enviar_field_to_S(loja, prevenda_id)
        print(response.content)
    else:
        print(f'Falha na solicitação com código de status {response.status_code}')


def inicia_robo(lojas = '*'):
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

            for prevenda in lista_prevendas.copy():
                print(prevenda['id'])
                visualizacao_objeto(prevenda, loja)
                envia_dados_foodydelivery(json.dumps(prevenda), loja, prevenda)
                lista_prevendas.remove(prevenda)
                time.sleep(6)

    
        end_time = time.time()
        elapsed_time = end_time - start_time
        # system('cls')
        print(f"\n\nTempo decorrido: {elapsed_time:.2f} segundos")
        time.sleep(filter_timer)



