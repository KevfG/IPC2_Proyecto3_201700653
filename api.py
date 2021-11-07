from flask import Flask, Response, request
from flask_cors import CORS
import readXml as xml
import os
from datetime import datetime
from fpdf import FPDF

now = datetime.now()
historialMovimientos = []
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origin": "*"}})

#encender django
#cd frontend
#python manage.py runserver 8000

@app.route('/events/all/', methods=['GET'])
def get_filterRange():
    xml.filterRangeDate()
    data = open('filtroFechaRango.txt', 'r+')
    historialMovimientos.append(now.strftime("%m/%d/%Y, %H:%M:%S") + ' Se filtaron las fechas por rango')
    return Response(response=data.read(),
                    mimetype='text/plain',
                    content_type='text/plain')

#--------------------------------------------------------------------------

@app.route('/events/ff/', methods=['POST'])
def post_filter():
    xml.filterDate(request.data.decode('utf-8'))
    historialMovimientos.append(now.strftime("%m/%d/%Y, %H:%M:%S") + ' Se filtaron las fechas')
    return Response(response="ok")

@app.route('/events/ff/', methods=['GET'])
def get_filter():
    data = open('filtroFecha.txt', 'r+')
    historialMovimientos.append(now.strftime("%m/%d/%Y, %H:%M:%S") + ' Se filtaron las fechas')
    return Response(response=data.read(),
                    mimetype='text/plain',
                    content_type='text/plain')

@app.route('/events/', methods=['POST'])
def post_events():
    data = open('data.xml', 'w+')
    data.write(request.data.decode('utf-8'))
    data.close()
    xml.processXml('data.xml')
    historialMovimientos.append(now.strftime("%m/%d/%Y, %H:%M:%S") + ' Se enviaron los datos')
    return Response(response=request.data.decode('utf-8'),
                    mimetype='text/plain',
                    content_type='text/plain')


@app.route('/events/', methods=['GET'])
def get_events():
    data = open('autorizaciones.xml', 'r+')
    historialMovimientos.append(now.strftime("%m/%d/%Y, %H:%M:%S") + ' Se recibieron los datos')
    return Response(response=data.read(),
                    mimetype='text/plain',
                    content_type='text/plain')

@app.route('/events/history/', methods=['GET'])
def get_history():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=24)

    a = 1

    for i in historialMovimientos:
        pdf.cell(200, 10, txt=str(i), ln=a, align="C")
        a =+ 1

    pdf.output("ejemplo.pdf")
    os.system("ejemplo.pdf")
    return Response(response="ok",
                    mimetype='text/plain',
                    content_type='text/plain')

@app.route('/events/remove/', methods=['GET'])
def get_remove():
    if os.path.isfile("autorizaciones.xml"):
        os.remove("autorizaciones.xml")
    if os.path.isfile("data.xml"):
        os.remove("data.xml")
    if os.path.isfile("ejemplo.pdf"):
        os.remove("ejemplo.pdf")
    if os.path.isfile("filtroFecha.txt"):
        os.remove("filtroFecha.txt")
    if os.path.isfile("filtroFechaRango.txt"):
        os.remove("filtroFechaRango.txt")
    return Response(response="ok",
                    mimetype='text/plain',
                    content_type='text/plain')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
