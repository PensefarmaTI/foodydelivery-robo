--select * from pdv_prevendas where LOJA = 1 and origem = 'T' AND DATA BETWEEN '01/06/2023' AND '30/06/2023'

select A.QUANTIDADE, B.DESCRICAO, A.TOTAL_ITEM, B.CONTROLADO
	from			pdv_prevendas_itens A
		JOIN				   PRODUTOS B
			ON		A.PRODUTO = B.PRODUTO

where prevenda = 185795 and loja = 1
