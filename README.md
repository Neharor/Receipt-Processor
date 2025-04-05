# Receipt Processor

This project is a Receipt Processor built with Flask (Python) for the backend and React for the frontend. Users can upload their receipts, and the system calculates points based on specific rules. The frontend lets users interact with the API, submit receipts, and view their points.

**Backend (Flask)**
Install dependencies:  pip3 install flask flask-cors
Run the server: python3 app.py

**Frontend(React)**
cd receipt-processor
install dependecies : npm install
run the app : npm start

Upload a **JSON receipt** to get a  **Receipt ID** .
Enter **Receipt ID** to fetch the points.


If you prefer not to run the React app, you can still test the backend APIs using Postman.

POST : http://localhost:5000/process-receipt
GET : http://localhost:5000/receipts/<receipt_id>/points
