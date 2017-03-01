from cStringIO import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import os
import re
import string


def convert(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)
    infile = file(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    # lista = text.split('\n')
    # print lista
    # for i in range(0,len(lista)):
    #     print i, lista[i]
    return text
def getInfoClass(list):
    tempDis     = ""
    tempProf    = ""
    for l in range(0,len(list)):
        if "NOME DA TURMA:" in list[l]:
            tempDis = list[l]
        if "PROFESSOR(A):" in list[l]:
            tempProf = list[l]

    tempDis = tempDis.split(":")[1]
    tempProf = tempProf.split(":")[1]

    dis = ""
    try:
        for i in range(0, len(tempDis)):
            if tempDis[i] != " " or tempDis[i] == " " and tempDis[i-1] != " " and tempDis[i+1] != " " :
                dis += tempDis[i]
            if tempDis[i] != " " and tempDis[i + 1] == " " and tempDis[i + 2] == " ":
                break
    except:
        pass
    prof = ""
    try:
        for i in range(0, len(tempProf)):
            if tempProf[i] != " " or tempProf[i] == " " and tempProf[i - 1] != " " and tempProf[i + 1] != " ":
                prof += tempProf[i]
            if tempProf[i] != " " and tempProf[i + 1] == " " and tempProf[i + 2] == " ":
                break
    except:
        pass
    return (prof, dis)


def open(fname):
    bashCommand = "pdftotext -layout " + fname
    os.system(bashCommand)
    nname = fname.split(".")
    f = file(nname[0]+".txt","r")
    linhas = f.read().split("\n")
    # linhas = re.findall('\s*(.*?):[\n\s]?(.*)$', f.read(), re.MULTILINE)
    # linhas = re.findall('(.*?)$', f.read(), re.MULTILINE)
    lista = []
    lista_dre = []
    lista_num = []
    lista_nome = []
    info = getInfoClass(linhas)
    for linha in linhas:
        temp = re.findall('(.*)([0-9]{9})', linha, re.MULTILINE)
        if temp != []:
            dre = temp[0][1]
            ntemp = temp[0][0]
            numNome = re.findall('([0-9]{1,2})\s(\w[A-Z].*)\s*', ntemp, re.MULTILINE)
            nome = re.findall('((\w[A-Z]*\s{0,1})*)\s*', numNome[0][1], re.MULTILINE)
            # print nome[0][0]
            lista_dre.append(dre)
            lista_num.append(numNome[0][0])
            lista_nome.append(nome[0][0])
            # lista.append(temp)

    # print len(lista_num), lista_num
    # print len(lista_nome), lista_nome
    # print len(lista_dre), lista_dre
    return {'nome':lista_nome, 'numero':lista_num, 'dre':lista_dre, "size":len(lista_dre), "prof":info[0], "disciplina":info[1]}

# def parseText(text):
#     print text

# parseText(convert("webdesign.pdf"))
# convert("cg.pdf")