from config_db import conexao
from model import Prevenda_pedido

def get_list_of_db(query):
    cursor = conexao.cursor()    
    cursor.execute(query)

    list = list(cursor.fetchall())
    return list

def get_details(prevenda_numero):
    query = f"SELECT * FROM VW_ITENS_PREVENDAS_FOODY WHERE PREVENDA = {prevenda_numero}"

    prevenda_itens_list = get_list_of_db(query)
    return prevenda_itens_list

def get_prevenda(loja, data):
    query = f"select * from pdv_prevendas where loja = {loja} and data = '{data}' and ORIGEM = 'T' -- and ENVIAR_FOODY = 'N'"
    
    prevenda_list = get_list_of_db(query)
    return prevenda_list


def filtra_dados_prevenda():
    prevenda_pedido_list = []
    prevenda_list = get_prevenda(36, '05/09/2023')
    for i in prevenda_list:
        i = list(i)
        prevenda_pedido = Prevenda_pedido().prevenda_pedido_default
        prevenda_pedido['id'] = str(i[0])
        # prevenda_itens = get_details(i[0])

        prevenda_pedido_list.append(prevenda_pedido)
    
    print(prevenda_pedido_list)
    # prevenda_pedido['id'] = '123'
    # print(prevenda_pedido)

def envia_dados_foodydelivery():
    # Url: https://app.foodydelivery.com/rest/1.2/orders
    # Method: POST
    pass

# cursor.execute('')
# row = cursor.fetchone()

# while row:
#     print(row)
#     row = cursor.fetchone()

filtra_dados_prevenda()

conexao.close()