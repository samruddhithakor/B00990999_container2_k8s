import csv
from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

STORAGE_DIR = "/samruddhi_PV_dir"

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    filename = data.get('file')
    product = data.get('product')

    app.logger.info("B00990999_samruddhi")

    if not filename or not product:
        return jsonify({"error": "Invalid JSON input."}), 400

    filepath = os.path.join(STORAGE_DIR, filename)
    
    if not os.path.exists(filepath):
        return jsonify({"file": filename, "error": "File not found."}), 400

    try:
        total = 0
        with open(filepath, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            
            if [col.strip() for col in header] != ['product', 'amount']:
                return jsonify({"file": filename, "error": "Input file not in CSV format."}), 400
            
            for row in reader:
                if len(row) != 2:
                    return jsonify({"file": filename, "error": "Input file not in CSV format."}), 400
                if row[0].strip() == product:
                    total += int(row[1].strip())
        return jsonify({"file": filename, "sum": total}), 200
    except Exception as e:
        return jsonify({"file": filename, "error": "Input file not in CSV format."}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6001)