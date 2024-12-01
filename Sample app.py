from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

def calculate_probability(data):
    # Example probability calculation logic
    return data['Close'].mean() / 100

@app.route('/generate_signal', methods=['POST'])
def generate_signal():
    data = pd.DataFrame(request.json)
    probability = calculate_probability(data)
    signal = 'BUY' if probability > 0.6 else 'SELL'
    return jsonify({'probability': probability, 'signal': signal})

if __name__ == '__main__':
    app.run(debug=True)
