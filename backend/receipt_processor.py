"""
The module contains functions to process and validate receipt data, 
calculate points based on rules and manage receipts.
"""
import re
from datetime import datetime
import  uuid 
from math import ceil

# Create a dictionary to store receipts
receipts = {}

def validate_receipt(data):
    """Validates the receipt data to ensure it contains the required fields and follows the correct format."""
    # check if receipt is valid or not
    receipt_fields = ['retailer', 'purchaseDate', 'purchaseTime', 'items', 'total']
    for field in receipt_fields:
        if field not in data:
            return False

    # check retailer names contain alphanumeric characters and spaces
    if not re.match("^[\w\s\-\&]+$", data['retailer']):
        return False

    # check purchase date format(YYYY-MM-DD)
    try:
        datetime.strptime(data['purchaseDate'], '%Y-%m-%d')
    except ValueError:
        return False

    # check purchase time format(hh:mm)
    try:
        datetime.strptime(data['purchaseTime'], '%H:%M')
    except ValueError:
        return False

    # check if items is a valid list
    if not isinstance(data['items'], list) or len(data['items']) == 0:
        return False

    return True

def process_receipt(data):
    """Validates receipt data, generates a unique ID, stores it, and returns the ID."""
    # validate data
    if not validate_receipt(data):
        raise ValueError("Invalid receipt")

    # get a unique receipt id for each receipt
    receipt_id = str(uuid.uuid4())
    # store data corresponding to receipt id
    receipts[receipt_id] = data
    return receipt_id

def calculate_points(receipt): 
    """Calculates points based on rules from the receipt data. """
    points = 0 
    # Rule1: One point for every alphanumeric character in the retailer name.
    retailer_name = receipt['retailer']
    for char in retailer_name:
        if char.isalnum():
            points += 1

    # Rule2: 50 points if the total is a round dollar amount with no cents.
    if float(receipt['total']) % 1 == 0:
        points += 50
    
    # Rule3: 25 points if the total is a multiple of 0.25.
    if float(receipt['total']) % 0.25 == 0:
        points += 25

    # Rule4: 5 points for every two items on the receipt.
    num_items = len(receipt['items'])
    points += (num_items // 2) * 5

    # Rule5: If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 and round up to the nearest integer. The result is the number of points earned.
    for item in receipt['items']:
        description = item.get('shortDescription', '').strip()
        if len(description) % 3 == 0:
            try:
                price = float(item['price'])
                points += ceil(price * 0.2)
            except ValueError:
                continue  
    
    # Rule6:  points if the day in the purchase date is odd.
    try:
        purchase_date = datetime.strptime(receipt['purchaseDate'], '%Y-%m-%d')
        if purchase_date.day % 2 == 1:
            points += 6
    except ValueError:
        pass

    # Rule7: 10 points if the time of purchase is after 2:00pm and before 4:00pm.
    try:
        purchase_time = datetime.strptime(receipt['purchaseTime'], '%H:%M')
        if 14 <= purchase_time.hour < 16:
            points += 10
    except ValueError:
        pass

    return points

