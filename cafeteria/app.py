# app.py
from flask import Flask, jsonify, render_template
from flask_cors import CORS
from routes.auth import auth_bp
from routes.stats import stats_bp
from routes.orders import orders_bp

app = Flask(__name__)
CORS(app)

# Registramos las rutas de la API
app.register_blueprint(auth_bp)
app.register_blueprint(stats_bp)
app.register_blueprint(orders_bp)

# Esta es la ruta que va a abrir tu Dashboard Web con las gráficas
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)