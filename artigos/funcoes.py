import xml.etree.ElementTree as et
import Levenshtein as lev
import csv
import os

def curriculos_com_artigos(arquivos):
    cv_com_artigos = []
    for _, _, i in os.walk(arquivos):
        for j in i:
            cv = parser_xml('/extrair_artigos/curriculos/' + j)

            try:
                if cv[1][1].tag == 'ARTIGOS-PUBLICADOS':
                    cv_com_artigos.append(j)

                else:
                    ignore = 0

            except IndexError:
                ignore = 0
                
    return cv_com_artigos
    
def parser_xml(curriculo):
    
    t = et.parse(curriculo)
    cv = t.getroot()

    return cv

def extrair_artigos(cv):
    m = []
    l = []
    a = 0
    
    while a <= len(cv[1][1])-1:
        for i in cv[1][1][a]:
            l.append(i.attrib)
        m.append(l)
        l = []
        a += 1
    print('Foram extraidos',len(m),'artigos')
    print()
    return m


def extrair_metadados(m):
    x = 0
    
    au = []
    pc = []
    tit = 0
    tiI = 0
    pais = 0
    ano = 0
    idi = 0
    doi = 0
    rev = 0
    issn = 0
    vol = 0
    num = 0

    metadados = []
    
    while x <= len(m)-1:
        for i in m[x]:
            try:
                tit = i['TITULO-DO-ARTIGO']
                tiI = i['TITULO-DO-ARTIGO-INGLES']
                ano = i['ANO-DO-ARTIGO']
                pais = i['PAIS-DE-PUBLICACAO']
                idi = i['IDIOMA']
                doi = i['DOI']
            except KeyError:
                try:
                    rev = i['TITULO-DO-PERIODICO-OU-REVISTA']
                    issn = i['ISSN']
                    vol = i['VOLUME']
                    num = i['FASCICULO']
                except KeyError:
                    try:
                        au.append(i['NOME-COMPLETO-DO-AUTOR'])
                    except KeyError:
                        try:
                           pc.append(i['PALAVRA-CHAVE-1'])
                           pc.append(i['PALAVRA-CHAVE-2'])
                           pc.append(i['PALAVRA-CHAVE-3'])
                        except:
                            ignore = 0

        d = {
            'titulo' : tit,
            'titulo-ingles' : tiI,
            'ano' : ano,
            'pais' : pais,
            'idioma' : idi,
            'doi' : doi,
            'revista' : rev,
            'issn' : issn,
            'volume' : vol,
            'numero' : num,
            'autores' : au,
            'assunto' : pc,
            }

        metadados.append(d)
        au = []
        pc = []

        x += 1

    return metadados

def eliminar_iguais_doi(metadados):
    repetidos = []
    for i in range(len(metadados)-1):
        for j in range(i+1, len(metadados)):
            if metadados[i]['doi'] == metadados[j]['doi']:
                if metadados[j]['doi'] != '':
                    repetidos.append(metadados[j])
                
    m = []
    print('Foram eliminadas',len(repetidos),'duplicatas\n')
    for i in metadados:
        if i not in repetidos:
            m.append(i)

    return m

def eliminar_similares_titulo(metadados):
    repetidos = []
    for i in range(len(metadados)-1):
        for j in range(i+1, len(metadados)):
            if lev.distance(metadados[i]['titulo'], metadados[j]['titulo']) <= 5:
                repetidos.append(metadados[j])

    m = []
    print('Foram eliminadas',len(repetidos),'duplicatas\n')
    for i in metadados:
        if i not in repetidos:
            m.append(i)

    return m
    

def escrever_csv(metadados):
    with open('metadados.csv', 'w', newline='', encoding='utf-8') as f:
        n = ['Autores',
             'Título',
             'Título em inglês',
             'Ano',
             'Pais',
             'Idioma',
             'Doi',
             'Revista',
             'Issn',
             'Vol.',
             'Núm',
             'Assunto']
        e = csv.DictWriter(f, fieldnames=n)

        e.writeheader()
        c = 0
        while c <= len(metadados)-1:
            e.writerow({'Autores' : metadados[c]['autores'],
                        'Título' : metadados[c]['titulo'],
                        'Título em inglês' : metadados[c]['titulo-ingles'],
                        'Ano' : metadados[c]['ano'],
                        'Pais' : metadados[c]['pais'],
                        'Idioma' : metadados[c]['idioma'],
                        'Doi' : metadados[c]['doi'],
                        'Revista' : metadados[c]['revista'],
                        'Issn' : metadados[c]['issn'],
                        'Vol.' : metadados[c]['volume'],
                        'Núm' : metadados[c]['numero'],
                    'Assunto' : metadados[c]['assunto']})
            c += 1
