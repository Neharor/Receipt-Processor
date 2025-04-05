import React, { useState } from 'react';

function App() {
  const [file, setFile] = useState(null);
  const [receiptId, setReceiptId] = useState('');
  const [error, setError] = useState('');
  const [points, setPoints] = useState(null);
  const [inputReceiptId, setInputReceiptId] = useState('');

  const handleFileChange = (e) => {
    // Get the first selected file
    const selectedFile = e.target.files[0];
    // Store the file in the state
    setFile(selectedFile);
    // Reset any previous receipt id
    setReceiptId('');
    // Reset any previous errors
    setError('');
    // Reset points
    setPoints(null); 
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please upload a JSON file');
      setPoints(null); 
      return;
    }

    try {
      const fileContent = await file.text();
      // Convert the text to JSON object
      const jsonData = JSON.parse(fileContent);

     // Send the receipt data to the backend for processing and get a receipt Id.
      const response = await fetch('http://localhost:5000/process-receipt', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(jsonData),
      });

      if (!response.ok) {
        const errText = await response.text();
        throw new Error(errText || 'Failed to process');
      }

      const result = await response.json();
      setReceiptId(result.id);
      setError(''); 
      setPoints(null);
    } catch (err) {
      setError(`Error: ${err.message}`);
      setReceiptId('')
      setPoints(null);
    }
  };

  const handleFetchPoints = async () => {
    if (!inputReceiptId) {
      setError('Please enter a receipt ID');
      return;
    }
    // Fetch the points for the given receipt id from the backend
    try {
      const response = await fetch(`http://localhost:5000/receipts/${inputReceiptId}/points`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        // Parse the error response as JSON
        const errText = await response.json(); 
        // Display the error message from the backend
        if (errText.error) {
            setError(errText.error); 
        } else {
            setError('Couldn’t fetch points. Please try again.');
        }
        setPoints(null);
        setReceiptId('');
        return;
      }

      const result = await response.json();
      // Update points state with the fetched result
      setPoints(result.points); 
      setError('');
    } catch (err) {
      setError('Something went wrong. Please try again.');
      setPoints(null);
    }
  };

  return (
    <div style={{ padding: '4rem', fontFamily: 'Arial, sans-serif', textAlign: 'center' }}>
      <h1>Receipt Processor</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" accept=".json" onChange={handleFileChange} />
        <br /> <br />
        <button type="submit">Submit Receipt</button>
      </form>

      {receiptId && (
        <p style={{ color: 'green' }}>
          Receipt ID: <strong>{receiptId}</strong>
        </p>
      )}

      {error && <p style={{ color: 'red' }}>{error}</p>}

      <div>
        <h2>Get Points by Receipt ID</h2>
        <input
          type="text"
          placeholder="Enter Receipt ID"
          value={inputReceiptId}
          onChange={(e) => setInputReceiptId(e.target.value)}
        />
        <br />
        <button onClick={handleFetchPoints}>Get Points</button>
        {points !== null && <p>Points: {points}</p>}
      </div>
    </div>
  );
}

export default App;
