from flask import Flask, jsonify

app = Flask(__name__)

# Dados mockados de temperatura por cidade
mocked_weather_data = {
    "SãoPaulo": {"temp": 25, "unit": "Celsius"},
    "RioDeJaneiro": {"temp": 34, "unit": "Celsius"},
    "Curitiba": {"temp": 12, "unit": "Celsius"},
    "Fortaleza": {"temp": 30, "unit": "Celsius"}
}

@app.route('/weather/<city>', methods=['GET'])
def get_weather(city):
    city_data = mocked_weather_data.get(city)
    if city_data:
        return jsonify({
            "city": city.replace("_", " "),
            "temp": city_data["temp"],
            "unit": city_data["unit"]
        })
    else:
        return jsonify({"error": "Cidade não encontrada"}), 404

if __name__ == '__main__':
    app.run(port=5001)  # Porta diferente para API B
