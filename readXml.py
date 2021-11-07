import xml.etree.ElementTree as ET
from yattag import Doc, indent
import re
import os
datosLista = []

class datos:
    def __init__(self, fecha, referencia, nit_emisor, nit_receptor, valor, iva, total, errorIva, errorTotal):
        self.fecha = fecha
        self.referencia = referencia
        self.nit_emisor = nit_emisor
        self.nit_receptor = nit_receptor
        self.valor = valor
        self.iva = iva
        self.total = total
        self.errorIva = errorIva
        self.errorTotal = errorTotal

def processXml(file):

    xmlDocument = ET.parse(file)
    root = xmlDocument.getroot()

    for i in root:  # elemento.tag = obtener nombre del tag
        tiempo = ""
        referencia = ""
        nit_emisor = ""
        nit_receptor = ""
        valor = 0
        iva = 0
        total = 0
        errorIva = 0
        errorTotal = 0
        for j in i:
            if j.tag == "TIEMPO":
                lista = j.text.split('\n')
                tiempo = validDate(lista)
            if j.tag == "REFERENCIA":
                lista = j.text
                referencia = validReference(lista)
            if j.tag == "NIT_EMISOR":
                lista = j.text
                nit_emisor = validNit(lista)
            if j.tag == "NIT_RECEPTOR":
                lista = j.text
                nit_receptor = validNit(lista)
            if j.tag == "VALOR":
                valor = float(j.text)
            if j.tag == "IVA":
                iva = float(j.text)
            if j.tag == "TOTAL":
                total = float(j.text)

            if validIva(iva, valor) == True:
                errorIva = 0
            else:
                errorIva = 1

            if validTotal(iva, valor, total) == True:
                errorTotal = 0
            else:
                errorTotal = 1
        datosLista.append(datos(tiempo, referencia, nit_emisor,
                          nit_receptor, valor, iva, total, errorIva, errorTotal))
    crearXml()
    #os.remove("autorizaciones.xml")

def validDate(date):
    for i in date:
        if re.search(r"([0-2][0-9]|3[0-1])(\/|-)(0[1-9]|1[0-2])\2(\d{4})", i) != None:
            sub_cadena = re.search(
                r"([0-2][0-9]|3[0-1])(\/|-)(0[1-9]|1[0-2])\2(\d{4})", i.strip())
            fecha = sub_cadena.group()
            return fecha


def validReference(ref):
    if re.search(r"([0-9]){1,40}$", ref) != None:
        sub_cadena = re.search(r"([0-9]){1,40}$", ref)
        fecha = sub_cadena.group()
        return fecha


def validNit(nit):
    if re.search(r"([0-9]){1,20}$", nit) != None:
        sub_cadena = re.search(r"([0-9]){1,20}$", nit)
        fecha = sub_cadena.group()
        return fecha


def validIva(iva, valor):
    a = round(valor * 0.12, 2)
    b = iva
    if b == a:
        return True
    else:
        return False


def validTotal(iva, valor, total):
    if (iva + valor) == total:
        return True
    else:
        return False


def crearXml():
    contadorErrorIva = 0
    facturas = []
    for j in datosLista:
        facturas.append(j.fecha)
    
    print(facturas)

    doc, tag, text = Doc().tagtext()
    with tag('LISTAAUTORIZACIONES'):
        with tag('AUTORIZACION'):
            for i in datosLista:
                if(len(facturas) == 1):
                    facturas.pop()
                if i.fecha in facturas:
                    with tag("FECHA"):
                        text(i.fecha)
                    if len(facturas) != 0:
                        with tag("FACTURAS_RECIBIDAS"):
                            text(facturas.count(i.fecha))
                            print(facturas.count(i.fecha))
                            k = 0
                            while(k < len(facturas)):
                                facturas.remove(i.fecha)
                                k += 1
                            print(facturas)
                        
            with tag("ERRORES"):
                with tag("ERROR_IVA"):
                    for i in datosLista:
                        if i.errorIva == 1:
                            contadorErrorIva += 1
                    text(contadorErrorIva)
                    contadorErrorIva = 0
        with tag("LISTADO_AUTORIZACIONES"):
            for i in datosLista:
                if i.errorTotal == 0:
                    with tag("NIT_EMISOR", ref = i.referencia):
                        text(i.nit_emisor)
                    with tag("NIT_RECEPTOR", ref = i.referencia):
                        text(i.nit_receptor)

    result = indent( 
        doc.getvalue(), 
        indentation = ' '*4, 
        newline = '\r' 
    ) 

    mydata = result
    myfile = open("autorizaciones.xml", "w")
    myfile.write(str(mydata))

#----------------------------------------------------------------------------------------------------------
def filterDate(date):
    textPlain = open('filtroFecha.txt', 'w+')
    textPlain.write("Resumen\n")

    file = open("autorizaciones.xml", 'r')
    xmlDocument = ET.parse(file)
    root = xmlDocument.getroot()

    cont = 0
    for j in root:
        for i in j:
            if i.text == str(date):
                print(i.text)
                textPlain.write(i.text + "\n")
                cont += 1
            if cont == 1:    
                if i.tag == "FACTURAS_RECIBIDAS":
                    textPlain.write(i.text + "\n")
                    print(i.text)
                    break
    
    textPlain.close()

def filterRangeDate():

    textPlain = open('filtroFechaRango.txt', 'w+')
    textPlain.write("Resumen fechas\n")

    file = open("autorizaciones.xml", 'r')
    xmlDocument = ET.parse(file)
    root = xmlDocument.getroot()

    for j in root:
        if j.tag == "AUTORIZACION":
            for i in j:
                textPlain.write(i.text + "\n")
                print(i.text)
        break

    textPlain.close()
