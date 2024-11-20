from flask import Flask, request, jsonify
from app.services import Switch

app = Flask(__name__)

@app.route('/')
def index():
    return "¡Bienvenido al generador de imagenes!"


@app.route('/crearImagen', methods=['POST'])
def crear_pdf():
    data = request.json
    respuesta = Switch.verificar_tipo_doc(data)
    return jsonify(respuesta)


