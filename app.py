from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import colorama
from colorama import Fore, Style

colorama.init()

app = Flask(__name__)
CORS(app)

# VirusTotal API key and URL
API_KEY = "498b80ef6e0b2a65de622ef05cb61ec72b5e74f1df1c4d6b0d6d3efbb59c13f7"
API_URL = "https://www.virustotal.com/vtapi/v2/url/report"

# Metrics
metrics = {
    "TP": 0,
    "FP": 0,
    "TN": 0,
    "FN": 0,
}

@app.route('/check_link', methods=['GET'])
def check_link():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    # Query VirusTotal API
    try:
        params = {'apikey': API_KEY, 'resource': url}
        response = requests.get(API_URL, params=params)
        data = response.json()

        # Extract detection results
        if 'positives' in data and 'total' in data:
            positives = data['positives']
            total = data['total']
            is_phishing = positives > 0  # Flag as phishing if positives > 0

            # Update metrics
            if is_phishing:
                metrics["TP"] += 1
                print(Fore.RED + f"[WARNING] Phishing URL detected: {url}" + Style.RESET_ALL)
            else:
                metrics["TN"] += 1
                print(Fore.GREEN + f"[INFO] Safe URL: {url}" + Style.RESET_ALL)

            # Calculate and display efficiency
            efficiency = calculate_efficiency()
            print(Fore.BLUE + f"Efficiency Metrics: {efficiency}" + Style.RESET_ALL)

            return jsonify({'result': 'phishing' if is_phishing else 'safe'})
        else:
            metrics["FN"] += 1
            print(Fore.YELLOW + f"[INFO] Unable to determine: {url}" + Style.RESET_ALL)
            return jsonify({'result': 'unknown'})

    except Exception as e:
        metrics["FP"] += 1
        print(Fore.YELLOW + f"[ERROR] Error checking link: {url} - {e}" + Style.RESET_ALL)
        return jsonify({'error': 'Error checking the link'}), 500


def calculate_efficiency():
    TP, FP, TN, FN = metrics["TP"], metrics["FP"], metrics["TN"], metrics["FN"]
    total = TP + FP + TN + FN

    accuracy = (TP + TN) / total if total > 0 else 0
    recall = TP / (TP + FN) if (TP + FN) > 0 else 0
    fpr = FP / (FP + TN) if (FP + TN) > 0 else 0

    return {
        "Accuracy": round(accuracy * 100, 2),
        "Detection Rate (Recall)": round(recall * 100, 2),
        "False Positive Rate": round(fpr * 100, 2),
    }


if __name__ == '__main__':
    app.run(debug=True)
