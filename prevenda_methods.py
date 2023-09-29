from config_db import conexao
from datetime import datetime
from utils import *
from os import environ

data = datetime.now().strftime("%d/%m/%Y")

class Prevenda():
    def __init__(self):
        pass


def get_prevenda(loja, columns='*', where_filter=''):
    query = f"select {columns} from pdv_prevendas where loja = {loja} and data = '{data}' and ORIGEM = 'T' and canal_venda <> 8 {where_filter} and ENVIADO_FOODY = 'N'"
    
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



def get_details(loja, prevenda_numero):
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



def get_payment_method(loja, prevenda_numero):
    payment = get_prevenda(loja, columns='dinheiro, troco, convenio, cartao, prevenda', where_filter=f'and prevenda = {prevenda_numero}')[0]

    for payment_index in range(0, len(payment)):
        payment_method = {}
        if payment[payment_index] != 0:
            if payment_index == 0:
                payment_method['method'] = 'money'
                payment_method['value'] = str(payment[payment_index])
                payment_method['exchange'] = str(payment[1])
            elif payment_index == 2:
                payment_method['method'] = 'on_credit'
                payment_method['value'] = str(payment[payment_index])
            elif payment_index == 3:
                payment_method['method'] = 'card'
                payment_method['value'] = str(payment[payment_index])
            else:
                continue
            return payment_method



def get_client_info(loja, prevenda_numero=''):

    client_info = get_prevenda(loja, columns='nome, telefone',where_filter=f' and prevenda = {prevenda_numero}')[0]
    
    telefone = client_info[1]

    query = "SELECT CASE WHEN A.CODIGO_CONVENIO IS NULL THEN A.NOME ELSE B.NOME END AS NOME "
    query += "FROM PDV_PREVENDAS A WITH(NOLOCK) LEFT JOIN ENTIDADES_CONVENIOS_CARTOES B WITH(NOLOCK) "
    query += "ON A.CODIGO_CONVENIO = B.ENTIDADE AND A.CLIENTE = B.CONVENIO_CARTAO "
    query += f"where prevenda = {prevenda_numero} and loja = {loja}"

    nome = get_list_of_db(query)[0][0]
   

    client_info = {
        'customerPhone': telefone,
        'customerName': nome,
        'customerEmail': ''
    }
    return client_info


def get_address_info(loja, prevenda_numero):
    address_info_prevenda = get_prevenda(loja, columns='cep, tipo_endereco, endereco, numero, complemento, bairro, cidade, estado', where_filter=f'and prevenda = {prevenda_numero}')[0]
    
    cep = address_info_prevenda[0]
    tipo_endereco = address_info_prevenda[1]
    endereco = address_info_prevenda[2]
    numero = str(address_info_prevenda[3])
    complemento = address_info_prevenda[4]
    bairro = address_info_prevenda[5]
    cidade = address_info_prevenda[6]
    estado = address_info_prevenda[7]
    pais = "brasil"

    
    

    endereco = endereco.replace(',','')

    address =  f'{tipo_endereco} {endereco} {cep}, {numero}, {bairro}'

    # geolocator = Nominatim(user_agent="wazeyes")
    # location = geolocator.geocode(address)

    # print(location.address)
    # coordinates = {"lat":location.Location.latitude ,"lng":location.log}

    rua = f'{tipo_endereco} {endereco}, {bairro} CEP.:{cep}'

    address_info = {
        "address": address,
        "street": rua,
        "houseNumber": numero,
        # "coordinates": coordinates,
        "city": cidade,
        "region": bairro,
        "country": pais,
        "complement": complemento
    }


    return address_info


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

def visualizacao_objeto(prevenda, loja):
    if isinstance(prevenda, list):
        for prevenda_ in prevenda.copy():
            visualiza_prevenda(prevenda_, loja)
            prevenda.remove(prevenda_)
    else:
        visualiza_prevenda(prevenda, loja)

@log
def visualiza_prevenda(prevenda, loja):
    string_prevenda  = f'\n\nLOJA: {loja}\n'
    string_prevenda += f"id: {prevenda['id']}\n"
    string_prevenda += f"prevenda_itens: \n{prevenda['orderDetails']}\n"
    string_prevenda += f"prevenda_obs: {prevenda['notes']}\n"
    string_prevenda += f"prevenda_pagamento: {prevenda['paymentMethod']}\n"
    string_prevenda += f"total: {prevenda['orderTotal']}\n"
    string_prevenda += f"endereço: {prevenda['deliveryPoint']}\n"
    string_prevenda += f"data: {prevenda['date']}\n"

    print(string_prevenda)
    return string_prevenda

def get_lojas_from_file():
    lojas = ''
    
    file_path = environ['PATH']
    file_name = '\lista_lojas.txt'
    file = file_path + file_name

    with open(file, 'r+') as f:
        while True:
            line = f.readline()
            if line.startswith('#'):
                continue
            if line != '':
                lojas += f'{line}'
            else:
                break

    if lojas == '':
        lojas = '*'

    lojas = ', '.join(lojas.split('\n'))
    return lojas
    


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



def verify_data():
    global data
    if data != datetime.now().strftime("%d/%m/%Y"):
        data = datetime.now().strftime("%d/%m/%Y")
    

if __name__ == '__main__':
    get_client_info(36)



