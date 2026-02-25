from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = 'productos.json'

# Crear el archivo JSON si no existe
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/productos', methods=['GET'])
def get_productos():
    with open(DATA_FILE, 'r') as f:
        productos = json.load(f)
    return jsonify(productos)

@app.route('/api/productos', methods=['POST'])
def save_producto():
    nuevo_producto = request.json
    # Asignar un ID único basado en el timestamp
    nuevo_producto['__backendId'] = str(int(os.times().elapsed * 1000))
    
    with open(DATA_FILE, 'r+') as f:
        productos = json.load(f)
        productos.append(nuevo_producto)
        f.seek(0)
        json.dump(productos, f, indent=4)
        f.truncate()
        
    return jsonify({"isOk": True, "message": "Producto guardado"})

@app.route('/api/productos/<id>', methods=['DELETE'])
def delete_producto(id):
    with open(DATA_FILE, 'r+') as f:
        productos = json.load(f)
        productos = [p for p in productos if p.get('__backendId') != id]
        f.seek(0)
        json.dump(productos, f, indent=4)
        f.truncate()
    return jsonify({"isOk": True})

if __name__ == '__main__':
    app.run(debug=True, port=5000)