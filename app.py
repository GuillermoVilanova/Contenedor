import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "¡Hola desde Docker en Railway! 🚀"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Toma el puerto de Railway
    app.run(host='0.0.0.0', port=port)