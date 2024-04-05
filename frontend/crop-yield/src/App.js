import React, {useState, useEffect} from 'react';
import './App.css';
import cornImage from './cornimage.jpeg';
import Chart from 'chart.js/auto'; // Import Chart.js

function App() {
  const [countyCode, setCountyCode] = useState('');
  const [stateCode, setStateCode] = useState('');
  const [predictionResult, setPredictionResult] = useState(null);
  const [cleanedData, setCleanedData] = useState(null); // State to hold cleaned data
  const [error, setError] = useState(null);
  const [formSubmitted, setFormSubmitted] = useState(false);

    const handleCountyCodeChange = (event) => {
        setCountyCode(event.target.value);
    };

    const handleStateCodeChange = (event) => {
        setStateCode(event.target.value);
    };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setFormSubmitted(true);
    setPredictionResult(null); // Clear prediction result
    setCleanedData(null);
    
    try {
      const response = await fetch("http://127.0.0.1:5000/predict", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          COUNTY_CODE: parseInt(countyCode),
          STATE_CODE: parseInt(stateCode)
        })
      });
      
      const data = await response.json();
      console.log(data);
      
      setPredictionResult(data.nextYearPrediction);
      setCleanedData(data.cleaned_csv_data);
    } catch (error) {
      console.error('Error:', error);
      setError(error.message);
    }
  };

  const prediction = predictionResult && predictionResult.length > 0 ? predictionResult[0] : null;

  // Draw the scatter plot when cleaned data and prediction result are available
  useEffect(() => {
    if (cleanedData && prediction !== null) {
      const ctx = document.getElementById('scatterChart').getContext('2d');
      
      // Extract x and y data from cleanedData
      const xData = cleanedData.map(entry => entry.YEAR);
      const yData = cleanedData.map(entry => entry.VALUE);

      const nextYear = new Date().getFullYear() + 1;

      const scatterChartData = {
        datasets: [{
          label: 'Crop Yield Over Years',
          data: xData.map((x, i) => ({ x, y: yData[i] })),
          backgroundColor: 'blue',
          pointRadius: 5,
          pointHoverRadius: 8,
        },
        {
          label: 'Next Year Prediction',
          data: [{ x: nextYear, y: prediction }],
          backgroundColor: 'red',
          pointRadius: 8,
          pointHoverRadius: 10,
        }]
      };

      new Chart(ctx, {
        type: 'scatter',
        data: scatterChartData,
        options: {
          scales: {
            x: {
              type: 'linear',
              position: 'bottom',
              title: {
                display: true,
                text: 'Year'
              }
            },
            y: {
              title: {
                display: true,
                text: 'Yield'
              }
            }
          }
        }
      });
    }
  }, [cleanedData, prediction]);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Corn Crop Yield Prediction</h1>
        <img src={cornImage} alt="corn-image" style={{ width: '10%', height: 'auto'}}></img>
        <p>Please select your county and state code.</p> 
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
          <button type="submit">Submit</button>
        </form>
        {formSubmitted && cleanedData && predictionResult !== null && (
          <div>
            <h2>Prediction Results</h2>
            <p style={{fontSize:"30px"}}>Next year's predicted yield: {Math.round(predictionResult)} bushels</p>
            <canvas id="scatterChart" width="400" height="400"></canvas> {/* Chart container */}
          </div>
        )}

                {/* Display error message if there is an error */}
                {error && <div>Error: {error}</div>}
            </header>
        </div>
    );
}

export default App;
