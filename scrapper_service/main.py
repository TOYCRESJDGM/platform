import os
from dotenv import load_dotenv
from processing import process_cufe
from flask import Flask, request, jsonify

app = Flask(__name__)

# Cargar las variables de entorno desde el archivo .env
load_dotenv()


@app.route("/", methods=['POST'])
def process_cufe_route():
    # Obtener el CUF del cuerpo de la solicitud
    cufe = request.json.get('cufe')  # Suponiendo que se envía como JSON

    if not cufe:
        return jsonify({"error": "El CUF no fue proporcionado en el cuerpo de la solicitud"}), 400
    
    process_cufe(cufe)
        
    return jsonify({"message": 'procesando cufe...'}), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 6000)))

