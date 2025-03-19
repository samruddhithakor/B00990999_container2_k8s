from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

# GKE Persistent Volume Mount Directory
STORAGE_DIR = "/samruddhi_PV_dir"

@app.route('/process', methods=['POST'])
def process_file():
    data = request.get_json()

    if not data or "file" not in data or "product" not in data:
        return jsonify({"file": None, "error": "Invalid JSON input."}), 400

    file_path = os.path.join(STORAGE_DIR, data["file"])

    if not os.path.exists(file_path):
        return jsonify({"file": data["file"], "error": "File not found."}), 404

    try:
        df = pd.read_csv(file_path)

        required_columns = {"product", "amount"}
        if not required_columns.issubset(df.columns) or not df["amount"].apply(lambda x: str(x).isdigit()).all():
            return jsonify({"file": data["file"], "error": "Input file not in CSV format."}), 400

        df["amount"] = df["amount"].astype(int)
        total_sum = df[df["product"] == data["product"]]["amount"].sum()

        return jsonify({"file": data["file"], "sum": int(total_sum)}), 200

    except (pd.errors.ParserError, pd.errors.EmptyDataError):
        return jsonify({"file": data["file"], "error": "Input file not in CSV format."}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6001)
