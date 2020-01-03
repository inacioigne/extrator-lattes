import sys
import os

sys.path.append('funcoes')

from funcoes import *

#ABRIR ARQUIVO
for _, _, i in os.walk('curriculos'):
    curriculos = i

#PARSER XML 
trabalhos_totais = []
for i in curriculos:
    curriculo = '/lattes/curriculos/' + i
    cv = parser_xml(curriculo)
    print('Lendo curriculo de',cv[0].attrib['NOME-COMPLETO'])
    trabalhos_autor = extrair_trabalhos_em_evento(cv)
    trabalhos_totais.append(trabalhos_autor)

#EXTRAI METADADOS
metadados = []
for i in trabalhos_totais:
    m = extrair_metadados(i)
    for d in m:
        metadados.append(d)

#ELIMINANDO TÍTULOS SIMILARES
m = eliminar_titulos_similares(metadados)
   
#ESCREVER CSV
escrever_csv(m)
