from flask import Flask, jsonify
import requests
import time

app = Flask(__name__)

# Cache simples: { city_name: (response_data, timestamp) }
cache = {}
CACHE_TTL = 60  # segundos

API_B_URL = 'http://localhost:5001/weather/'

@app.route('/recommendation/<city>', methods=['GET'])
def get_recommendation(city):
    now = time.time()
    
    # Verifica cache
    if city in cache:
        data, timestamp = cache[city]
        if now - timestamp < CACHE_TTL:
            return jsonify(data)
    
    # Consulta API B
    try:
        response = requests.get(f"{API_B_URL}{city}")
        if response.status_code != 200:
            return jsonify({"error": "Cidade não encontrada na API B"}), 404
        
        weather = response.json()
        temp = weather["temp"]

        # Lógica de recomendação
        if temp > 30:
            recommendation = "Está muito quente! Hidrate-se e use protetor solar."
        elif 15 < temp <= 30:
            recommendation = "O clima está agradável. Aproveite o dia!"
        else:
            recommendation = "Está frio! Vista um casaco."

        result = {
            "city": weather["city"],
            "temp": temp,
            "unit": weather["unit"],
            "recommendation": recommendation
        }

        # Atualiza cache
        cache[city] = (result, now)

        return jsonify(result)

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Erro ao acessar API B", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
