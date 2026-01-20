import logging
from flask import Flask, jsonify

# Initialize Flask app
app = Flask(__name__)

# Simple logging configuration
logging.basicConfig(level=logging.INFO)

@app.route('/status', methods=['GET'])
def status():
    # Log the incoming request
    logging.info("Received status request")
    
    # Return an empty, valid response
    return jsonify({"status": "OK"}), 200

if __name__ == '__main__':
    app.run(debug=True)
