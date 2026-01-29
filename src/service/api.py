import logging
from flask import Flask, jsonify
from src.service.ingress_runner import execute_ingress

# Initialize Flask app
app = Flask(__name__)

# Simple logging configuration
logging.basicConfig(level=logging.INFO)

@app.route('/status', methods=['GET'])
def status():
    # Log the incoming request
    logging.info("Received status request")

    # Example usage of the ingress runner
    raw_input = {"tenant_id": "tenant_test_001"}
    result = execute_ingress(raw_input, user_id="u1", role="viewer", fn=lambda: {"status": "OK"})

    response = {
        "tenant_id": result.tenant_id,
        "envelope_id": result.envelope_id,
        **result.result,
    }
    status_code = 200 if response.get("ok") else 400
    return jsonify(response), status_code

if __name__ == '__main__':
    app.run(debug=True)
