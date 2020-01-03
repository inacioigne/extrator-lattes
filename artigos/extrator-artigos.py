import sys

sys.path.append('funcoes')

from funcoes import *

#ESCOLHER CURRICULOS COM ARTIGOS
print('Escolhendo curriculos com artigos publicados\n')
curriculos = curriculos_com_artigos('curriculos')
print(len(curriculos),'curriculos com artigos')

#PARSER XML 
artigos_totais = []
for i in curriculos:
    curriculo = '/extrair_artigos/curriculos/' + i
    cv = parser_xml(curriculo)
    print('Lendo curriculo de',cv[0].attrib['NOME-COMPLETO'])
    artigos_autor = extrair_artigos(cv)
    artigos_totais.append(artigos_autor)

#EXTRAI METADADOS
print('Extraindo metadados...\n')
metadados = []
for i in artigos_totais:
    m = extrair_metadados(i)
    for d in m:
        metadados.append(d)
print('Foram extraidos',len(metadados),'artigos\n')

#ELIMINAR DOIS IGUAIS
print('Eliminando duplicatas apartir do DOI...\n')
metadados_doi = eliminar_iguais_doi(metadados)

#ELIMINANDO TÍTULOS SIMILARES
print('Eliminando duplicatas apartir do título...\n')
metadados = eliminar_similares_titulo(metadados_doi)
   
#ESCREVER CSV
print('Gravando metadados...\n')
escrever_csv(metadados)
print('Metadados extraidos e gravados com sucesso!')
