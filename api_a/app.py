from flask import Flask, jsonify
import requests
import redis
import json

app = Flask(__name__)

# Configura conexão com o Redis (localhost, porta padrão)
cache = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Tempo de vida do cache (em segundos)
CACHE_TTL = 60

API_B_URL = 'http://localhost:5001/weather/'

@app.route('/recommendation/<city>', methods=['GET'])
def get_recommendation(city):
    city_key = city.lower()

    # Verifica se a cidade está no cache Redis
    cached_data = cache.get(city_key)
    if cached_data:
        return jsonify(json.loads(cached_data))

    # Consulta API B
    try:
        response = requests.get(f"{API_B_URL}{city}")
        if response.status_code != 200:
            return jsonify({"error": "Cidade não encontrada na API B"}), 404

        weather = response.json()
        temp = weather["temp"]

        # Gera a recomendação
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

        # Armazena no Redis com tempo de expiração
        cache.setex(city_key, CACHE_TTL, json.dumps(result))

        return jsonify(result)

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Erro ao acessar API B", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
