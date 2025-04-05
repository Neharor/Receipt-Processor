"""
The module defines Flask routes for processing receipt data and 
calculating points based on receipt details.
"""
from flask import Flask, request, jsonify 
from flask_cors import CORS
from receipt_processor import process_receipt, receipts, calculate_points

# Create an instance of flask class 
app = Flask(__name__)

CORS(app)

# Create route to handle receipt data 
@app.route('/process-receipt', methods = ['POST'])
def process_receipt_endpoint(): 
    """
    Takes in the receipt data, creates a unique id for it,
    and saves it in memory. Then, it sends back the receipt ID in the response.
    """
    data = request.get_json()
    receipt_id = process_receipt(data)
    return jsonify({"id": receipt_id})

# Create route to calculate points  for a specific receipt 
@app.route('/receipts/<receipt_id>/points', methods = ['GET'])
def get_points(receipt_id): 
    """
    Checks if the given receipt id exists in memory. If found,
    it calculates and returns the points for that receipt. If not,
    it returns an error message indicating the receipt was not found.
    """
    if receipt_id not in receipts: 
        return jsonify({"error": "Receipt not found"}), 404 
    receipt = receipts[receipt_id]
    points = calculate_points(receipt)
    return jsonify({"points": points})

if __name__ == '__main__':
    app.run(debug= True)