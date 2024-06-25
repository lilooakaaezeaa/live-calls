from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)

API_URL = 'https://api.premiumy.net/v1.0'
API_KEY = 'Wdv1qTghQJ2sKzp5Q_4Tcg'

@app.route('/live_calls', methods=['GET'])
def get_live_calls():
    headers = {
        'Content-Type': 'application/json',
        'Api-Key': API_KEY
    }
    payload = {
        "id": None,
        "jsonrpc": "2.0",
        "method": "live_call:get_list_by_account_user",
        "params": {}
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    data = response.json()
    return jsonify(data['result']['live_call_list'])

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
