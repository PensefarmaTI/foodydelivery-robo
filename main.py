from config_db import conexao
from model import Prevenda_pedido

def get_list_of_db(query):
    cursor = conexao.cursor()    
    cursor.execute(query)

    list_to_return = cursor.fetchall()
    for item in list_to_return:
        list_to_return[list_to_return.index(item)] = list(item)
    return list_to_return

def get_details(prevenda_numero, loja):
    query  = f"select A.QUANTIDADE, B.DESCRICAO, A.TOTAL_ITEM, B.CONTROLADO "
    query += f"from	pdv_prevendas_itens A JOIN PRODUTOS B ON A.PRODUTO = B.PRODUTO "
    query += f"where prevenda = {prevenda_numero} and loja = {loja}"
 
    prevenda_itens_list = get_list_of_db(query)

    # 1x G CETOCONAZOL 200MG 30'S CIMED | R$ 95.83  *RETER RECEITA
    product_line = ''
    for item in prevenda_itens_list:
        quantidade = str(item[0])
        descricao = str(item[1])
        total = str(item[2])
        controlado = str(item[3])
        
        product_line += f'{quantidade.center(10)}x {descricao.ljust(100)} | R$ {total.center(10)}'
        if controlado == 'S':
            product_line += '  *RETER RECEITA'
        product_line += '\n'
    
    return product_line

def get_prevenda(loja, data):
    query = f"select * from pdv_prevendas where loja = {loja} and data = '{data}' and ORIGEM = 'T' -- and ENVIAR_FOODY = 'N'"
    
    prevenda_list = get_list_of_db(query)
    return prevenda_list


def filtra_dados_prevenda(loja, data):
    prevenda_pedido_list = []
    prevenda_list = get_prevenda(loja, data)
    for i in prevenda_list:
        i = list(i)
        prevenda_pedido = Prevenda_pedido().prevenda_pedido_default
        prevenda_pedido['id'] = str(i[0])
        prevenda_pedido['orderDetails'] = get_details(prevenda_pedido['id'], loja)

        prevenda_pedido_list.append(prevenda_pedido)
    
    for i in range(0, len(prevenda_pedido_list)):
        print(prevenda_pedido_list[i]['orderDetails'])
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

filtra_dados_prevenda(36, '04/09/2023')
#print(get_details(128774, 8))
#print(get_details(2129, 17))

conexao.close()