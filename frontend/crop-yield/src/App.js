import React, { useState } from 'react';
import './App.css';
import cornImage from './cornimage.jpeg';
import CropYieldPrediction from './CropYieldPredictions'; // Import the CropYieldPrediction component


function App() {
  const [countyCode, setCountyCode] = useState('');
  const [stateCode, setStateCode] = useState('');
  const [pesticideUse, setPesticideUse] = useState('');
  const [predictionResult, setPredictionResult] = useState(null);
  const [error, setError] = useState(null);
  const [formSubmitted, setFormSubmitted] = useState(false);


  const handleCountyCodeChange = (event) => {
    setCountyCode(event.target.value);
  };

  const handleStateCodeChange = (event) => {
    setStateCode(event.target.value);
  };

  const handlePesticideUseChange = (event) => {
    setPesticideUse(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setFormSubmitted(true);
    
    try {
      const response = await fetch("http://127.0.0.1:5000/predict"
      , {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          COUNTY_CODE: parseInt(countyCode),
          STATE_CODE: parseInt(stateCode),
          PESTICIDE_USE: pesticideUse
        })
      });
      
      const data = await response.json();
      setPredictionResult(data); // Update prediction result state
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Corn Crop Yield Prediction</h1>
        <img src={cornImage} alt="corn-image" style={{ width: '10%', height: 'auto'}}></img>
        <p>Please select your county and state code. Then if you are using pesticides.</p> 
        <p>The model will display future predictions for your county's yield.</p>
        <form onSubmit={handleSubmit}>
        <label>
            State Code:
            <input type="number" value={stateCode} onChange={handleStateCodeChange} />
          </label>
          <label>
            County Code:
            <input type="number" value={countyCode} onChange={handleCountyCodeChange} />
          </label>
          <label>
            Pesticide Use:
            <select value={pesticideUse} onChange={handlePesticideUseChange}>
              <option value="">Select</option>
              <option value="yes">Yes</option>
              <option value="no">No</option>
            </select>
          </label>
          <button type="submit">Submit</button>
        </form>
        {formSubmitted && <CropYieldPrediction predictionResult={predictionResult} />}

        {/* Display error message if there is an error */}
        {error && <div>Error: {error}</div>}
      </header>
    </div>
  );
}

export default App;
