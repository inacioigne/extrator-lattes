import xml.etree.ElementTree as et
import Levenshtein as lev
import csv

def parser_xml(curriculo):
    
    t = et.parse(curriculo)
    cv = t.getroot()

    return cv

def extrair_livros(cv):
    m = []
    l = []
    a = 0
    
    while a <= len(cv[1][2][1])-1:
        for i in cv[1][2][1][a]:
            l.append(i.attrib)
        m.append(l)
        l = []
        a += 1
    print('Foram extraidos',len(m),'livros')
    print()
    return m


def extrair_metadados(m):
    x = 0
    au = []
    pc = []
    metadados = []
    while x <= len(m)-1:
        for i in m[x]:
            try:
                tit = i['TITULO-DO-CAPITULO-DO-LIVRO']
                ano = i['ANO']
                idi = i['IDIOMA']
            except KeyError:
                try:
                    livro = i['TITULO-DO-LIVRO']
                    pg_i = i['PAGINA-INICIAL']
                    pg_f = i['PAGINA-FINAL']
                    cidade = i['CIDADE-DA-EDITORA']
                    editora = i['NOME-DA-EDITORA']
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
            'ano' : ano,
            'idioma' : idi,
            'livro' : livro,
            'pag. inicial' : pg_i,
            'pag. final' : pg_f,
            'cidade' : cidade,
            'editora' : editora,
            'autores' : au,
            'assunto' : pc,
            }

        metadados.append(d)
        au = []
        pc = []

        x += 1

    return metadados

def eliminar_titulos_similares(metadados):
    repetidos = []
    for i in range(len(metadados)-1):
        for j in range(i+1, len(metadados)):
            if lev.distance(metadados[i]['titulo'], metadados[j]['titulo']) <= 5:
                repetidos.append(metadados[j])

    m = []
    print('Foram eliminados',len(repetidos),'títulos similares')
    for i in metadados:
        if i not in repetidos:
            m.append(i)

    return m
    

def escrever_csv(metadados):
    with open('capitulo_livros.csv', 'w', newline='', encoding='utf-8') as f:
        n = ['Autores',
             'Título',
             'Livro',
             'Idioma',
             'Cidade',
             'Editora',
             'Ano',
             'Pag. Inicial',
             'Pag. Final',
             'Assunto']
        e = csv.DictWriter(f, fieldnames=n)

        e.writeheader()
        c = 0
        while c <= len(metadados)-1:
            e.writerow({'Autores' : metadados[c]['autores'],
                        'Título' : metadados[c]['titulo'],
                        'livro' : metadados[c]['livro'],
                        'Idioma' : metadados[c]['idioma'],
                        'Cidade' : metadados[c]['cidade'],
                        'Editora' : metadados[c]['editora'],
                        'Ano' : metadados[c]['ano'],
                        'Pag. Inicial' : metadados[c]['pag. inicial'],
                        'Pag. Final' : metadados[c]['pag. final'],
                        'Assunto' : metadados[c]['assunto']})
            c += 1
