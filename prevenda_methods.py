from config_db import conexao, api_token
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
        
        #product_line += f'{quantidade.center(10)} {descricao.ljust(100)} | R$ {str(total).center(10)}'
        product_line += f'{quantidade} {descricao} | R$ {str(total)}'
        if controlado == 'S':
            product_line += '  *RETER RECEITA'
        product_line += '\n'
    total_geral = ('Total | R$ ' + str(total_geral).center(10))
    #product_line += f"{total_geral.rjust(127)}"
    return product_line



def get_payment_method(prevenda_numero):
    payment = get_prevenda(columns='dinheiro, troco, convenio, cartao, prevenda', where_filter=f'and prevenda = {prevenda_numero}')[0]

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



def get_client_info(prevenda_numero):
    client_info = get_prevenda(columns='nome, telefone',where_filter=f'and prevenda = {prevenda_numero}')[0]
    telefone = client_info[0]
    nome = client_info[1]
    client_info = {
        'customerPhone': nome,
        'customerName': telefone,
        'customerEmail': ''
    }
    return client_info


def get_address_info(prevenda_numero):
    address_info = get_prevenda(columns='cep, tipo_endereco, endereco, numero, complemento, bairro, cidade, estado', where_filter=f'and prevenda = {prevenda_numero}')[0]
    cep = address_info[0]
    tipo_endereco = address_info[1]
    endereco = address_info[2]
    numero = str(address_info[3])
    complemento = address_info[4]
    bairro = address_info[5]
    cidade = address_info[6]
    estado = address_info[7]
    pais = "brasil"
    coordinates = {"lat":"","lng":""}

    #avenida argentina 683, parque paraiso, itapecerica da serra - sp

    address =  f'{tipo_endereco} {endereco}'
    find_numero = endereco.find(str(numero))
    if find_numero == -1:
        address += f' - Número: {str(numero)}, '
    else:
        address += ', '
    address += f'{bairro}, {cidade} - {estado}'
    if complemento != "":
        address += f' complem.: {complemento}'
    address += f' cep.: {cep}'
    address_info = {
        "address": address,
        "street": endereco,
        "houseNumber": numero,
        "coordinates": coordinates,
        "city": cidade,
        "region": bairro,
        "country": pais,
        "complement": complemento
    }
    return address_info

    

if __name__ == '__main__':
    loja = 1
    data = '06/09/2023'
    # get_address_info(199249)
    # get_client_info(199249)
    # get_payment_method(199249)