from model import Prevenda_pedido
from prevenda_methods import *

prevenda_pedido_list = []

def filtra_dados_prevenda():
    prevenda_list = get_prevenda(columns='prevenda, observacoes, total_liquido')
    orderDate = datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z")
    for prevenda in prevenda_list:
        prevenda_pedido = Prevenda_pedido().prevenda_pedido_default
        prevenda_pedido['id'] = str(prevenda[0])
        prevenda_pedido['orderDetails'] = get_details(prevenda_pedido['id'])
        prevenda_pedido['notes'] = str(prevenda[1])
        prevenda_pedido['paymentMethod'] = get_payment_method(prevenda_pedido['id'])['method']
        prevenda_pedido['orderTotal'] = str(prevenda[2])
        prevenda_pedido['date'] = orderDate
        prevenda_pedido['customer'] = get_client_info(prevenda_pedido['id'])
        prevenda_pedido['deliveryPoint'] = get_address_info(prevenda_pedido['id'])


        prevenda_pedido_list.append(prevenda_pedido)
    
    # prevenda_pedido['id'] = '123'
    # print(prevenda_pedido)

def visualizacao_objeto(prevenda_list):
    for i in range(0, len(prevenda_list)):
        print(f"\n\nprevenda {i+1}")
        print(f"id: {prevenda_list[i]['id']}")
        print(f"prevenda_itens: \n{prevenda_list[i]['orderDetails']}")
        print(f"prevenda_obs: {prevenda_list[i]['notes']}")
        print(f"prevenda_pagamento: {prevenda_list[i]['paymentMethod']}")
        print(f"total: {prevenda_list[i]['orderTotal']}")
        print(f"endereço: {prevenda_list[i]['deliveryPoint']['address']}")
        print(f"data: {prevenda_list[i]['date']}")

def envia_dados_foodydelivery():
    # Url: https://app.foodydelivery.com/rest/1.2/orders
    # Method: POST
    pass

filtra_dados_prevenda()
visualizacao_objeto(prevenda_pedido_list)
# print(prevenda_pedido_list)

conexao.close()