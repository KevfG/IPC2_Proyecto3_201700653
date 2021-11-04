from flask import Flask, Response, request
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origin": "*"}})


@app.route('/events/', methods=['POST'])
def post_events():
    data = open('data.txt', 'w+')
    data.write(request.data.decode('utf-8'))
    data.close()

    prueba = request.data.decode('utf-8')
    print(prueba)

    return Response(response=request.data.decode('utf-8'),
                    mimetype='text/plain',
                    content_type='text/plain')


@app.route('/events/', methods=['GET'])
def get_events():
    data = open('data.txt', 'r+')
    return Response(response=data.read(),
                    mimetype='text/plain',
                    content_type='text/plain')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
