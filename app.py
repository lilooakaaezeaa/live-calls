from flask import Flask, jsonify, render_template, request
import requests
import csv
from io import StringIO

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

@app.route('/cdr_cost', methods=['POST'])
def get_cdr_cost():
    headers = {
        'Content-Type': 'application/json',
        'Api-Key': API_KEY
    }
    filter_data = request.json
    payload = {
        "id": None,
        "jsonrpc": "2.0",
        "method": "cdr_full:group_get_list",
        "params": {
            "filter": filter_data,
            "group": "range/a_number/b_number",
            "page": 1,
            "per_page": 15
        }
    }
    response = requests.post(f"{API_URL}/csv", headers=headers, json=payload)
    try:
        response.raise_for_status()  # Raise an HTTPError for bad responses
        csv_data = response.text
        #print(f"CSV response: {csv_data}")  # Log the CSV response for debugging

        # Parse the CSV data
        total_cost = 0.0
        f = StringIO(csv_data)
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            print(f"CSV row: {row}")  # Log each row for debugging
            if row and len(row) > 5:
                try:
                    cost = float(row[5])
                    total_cost += cost
                except ValueError as ve:
                    print(f"ValueError parsing cost: {ve}")
        return jsonify({'cost': "{:.4f}".format(total_cost)})
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Log HTTP errors
        return jsonify({'error': 'HTTP error occurred'}), 500
    except Exception as e:
        print(f"Error parsing CSV response: {e}")  # Log any parsing errors
        return jsonify({'error': 'Error parsing CSV response'}), 500

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
