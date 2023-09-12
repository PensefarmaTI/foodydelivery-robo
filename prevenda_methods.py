from config_db import conexao
from datetime import datetime

data = datetime.now().strftime("%d/%m/%Y")

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
                payment_method['method'] = 'online'
                payment_method['value'] = str(payment[payment_index])
            elif payment_index == 3:
                payment_method['method'] = 'card'
                payment_method['value'] = str(payment[payment_index])
            else:
                continue
            return payment_method



def get_client_info(loja, prevenda_numero):
    client_info = get_prevenda(loja, columns='nome, telefone',where_filter=f'and prevenda = {prevenda_numero}')[0]
    telefone = client_info[0]
    nome = client_info[1]
    client_info = {
        'customerPhone': nome,
        'customerName': telefone,
        'customerEmail': ''
    }
    return client_info


def get_address_info(loja, prevenda_numero):
    address_info = get_prevenda(loja, columns='cep, tipo_endereco, endereco, numero, complemento, bairro, cidade, estado', where_filter=f'and prevenda = {prevenda_numero}')[0]
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

def limpa_lista(lista):
    for item in lista:
        lista.remove(item)
    return lista

if __name__ == '__main__':
    pass
