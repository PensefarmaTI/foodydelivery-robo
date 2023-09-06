from config_db import conexao
from config_access import *


def get_prevenda(columns='*', where_filter=''):
    query = f"select {columns} from pdv_prevendas where loja = {loja} and data = '{data}' and ORIGEM = 'T' and versao <> 'IFOOD' {where_filter} -- and ENVIAR_FOODY = 'N'"
    
    prevenda_list = get_list_of_db(query)
    for item in prevenda_list:
        item = list(item)
    return prevenda_list



def get_list_of_db(query):
    cursor = conexao.cursor()    
    cursor.execute(query)

    list_to_return = cursor.fetchall()
    for item in list_to_return:
        list_to_return[list_to_return.index(item)] = list(item)
    return list_to_return



def get_details(prevenda_numero):
    query  = f"select A.QUANTIDADE, B.DESCRICAO, A.TOTAL_ITEM, B.CONTROLADO "
    query += f"from	pdv_prevendas_itens A JOIN PRODUTOS B ON A.PRODUTO = B.PRODUTO "
    query += f"where prevenda = {prevenda_numero} and loja = {loja}"
 
    prevenda_itens_list = get_list_of_db(query)

    # 1x G CETOCONAZOL 200MG 30'S CIMED | R$ 95.83  *RETER RECEITA
    product_line = ''
    total_geral = 0
    for item in prevenda_itens_list:
        quantidade = str(item[0]) + ' x'
        descricao = str(item[1])
        total = item[2]
        controlado = str(item[3])
        total_geral += total
        
        product_line += f'{quantidade.center(10)} {descricao.ljust(100)} | R$ {str(total).center(10)}'
        if controlado == 'S':
            product_line += '  *RETER RECEITA'
        product_line += '\n'
    total_geral = ('Total | R$ ' + str(total_geral).center(10))
    #product_line += f"{total_geral.rjust(127)}"
    return product_line



def get_payment_method(prevenda_numero):
    payment_list = get_prevenda(columns='dinheiro, troco, convenio, cartao, prevenda', where_filter=f'and prevenda = {prevenda_numero}')

    for payment in payment_list:
        for payment_index in range(0, len(payment)):
            payment_method = {}
            if payment[payment_index] != 0:
                if payment_index == 0:
                    payment_method['method'] = 'money'
                    payment_method['value'] = str(payment[payment_index])
                    payment_method['exchange'] = str(payment[1])
                elif payment_index == 2:
                    payment_method['method'] = 'online'
                    payment_method['value'] = str(payment[payment_index])
                elif payment_index == 3:
                    payment_method['method'] = 'card'
                    payment_method['value'] = str(payment[payment_index])
                else:
                    continue
                return payment_method
