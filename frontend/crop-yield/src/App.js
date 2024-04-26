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
    const [stateCountyCodeMap, setStateCountyCodeMap] = useState(null);

    /*
    Format of stateCountyCodeMap
    map = {
        state_name: {
            state_code: value
            counties: {
                county_name: value
                county_name: value
                ...
            }
        }
        ...
    }
     */
    if (stateCountyCodeMap == null) {
        fetch('./name_code_map.csv')
            .then(response => response.text())
            .then(text => {
                const rows = text.split('\n');
                const data = rows.map(row => row.split(','));

                const map = {};

                data.forEach(row => {
                    const state_name = row[0];
                    const state_code = Number(row[1]);
                    const county_name = row[2];
                    const county_code = Number(row[3]);

                    if (state_name in map) {
                        map[state_name]["counties"][county_name] = county_code;
                    } else {
                        map[state_name] = {};
                        map[state_name]["state_code"] = state_code;
                        map[state_name]["counties"] = {};
                        map[state_name]["counties"][county_name] = county_code;
                    }
                });
                setStateCountyCodeMap(map);
            })
            .catch(error => {
                console.error('Error fetching the CSV file:', error);
            });
    } else {
        console.log(stateCountyCodeMap);
    }
    const handleStateCodeChange = (event) => {
        let selected_state_name = event.target.value;
        let selected_state_code = stateCountyCodeMap[selected_state_name]["state_code"];

        setStateCode(selected_state_code);

        updateCountyDropdown(selected_state_name);
    };

    function updateCountyDropdown(state_name) {
        // console.log("county dropdown init");
        const dropdown = document.getElementById("county_name");
        dropdown.innerHTML = '';
        if (stateCountyCodeMap != null) {
            // console.log("adding county options");
            let counties = Array.from(Object.keys(stateCountyCodeMap[state_name]["counties"]));
            counties.sort();
            counties.forEach(county => {
                const option = document.createElement("option");
                option.text = county;
                option.value = stateCountyCodeMap[state_name]["counties"][county];
                dropdown.appendChild(option)
            })
            setCountyCode(stateCountyCodeMap[state_name]["counties"][counties[0]]);
        }
    }

    const handleCountyCodeChange = (event) => {
        let selected_county_code = event.target.value;
        setCountyCode(selected_county_code);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        setFormSubmitted(true);
        setPredictionResult(null); // Clear prediction result
        setCleanedData(null);

        try {
            //If doesnt work, update back to 127.0.0.1
            const response = await fetch("http://127.0.0.1:5000", // Directly specifying the local address 
            {    
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
                    data: xData.map((x, i) => ({x, y: yData[i]})),
                    backgroundColor: 'blue',
                    pointRadius: 5,
                    pointHoverRadius: 8,
                },
                    {
                        label: 'Next Year Prediction',
                        data: [{x: nextYear, y: prediction}],
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
                            },
                            ticks: {
                                // Added callback function to format tick labels
                                callback: function (value, index, values) {
                                    // The callback function takes the tick value (year) and formats it using regex to insert commas for every three digits
                                    return value.toString().replace(",", ""); //replaced the comma with nothing...
                                }

                            }
                        },

                        y: {
                            title: {
                                display: true,
                                text: 'Corn Yield in Bushels'
                            }
                        }
                    }
                }
            });
        }
    }, [cleanedData, prediction]);

    useEffect(() => {
        console.log("state dropdown init");
        const dropdown = document.getElementById("state_name");
        dropdown.innerHTML = '';
        // console.log(dropdown.children);
        if (stateCountyCodeMap != null) {
            console.log("adding elements");
            let states = Array.from(Object.keys(stateCountyCodeMap));
            states.sort();
            states.forEach(state => {
                const option = document.createElement("option");
                // option.value = stateCountyCodeMap[state]["state_code"];
                option.value = state;
                option.text = state;
                // console.log(option);
                dropdown.appendChild(option)
            })
            let default_state = states[0]
            setStateCode(stateCountyCodeMap[default_state]["state_code"]);
            updateCountyDropdown(default_state);
        }

    }, [stateCountyCodeMap]);

    return (
        <div className="App">
            <header className="App-header">
                <h1>Corn Crop Yield Prediction</h1>
                <img src={cornImage} alt="corn-image" style={{width: '10%', height: 'auto'}}></img>
                <p>The model will display future predictions for your county's yield.</p>
                
                <p>Please select your state and county:</p>
                
                <form onSubmit={handleSubmit}>
                    <label>
                        State Name:
                        <select name="State Name" id="state_name" onChange={handleStateCodeChange}>State Name
                        </select>
                    </label>
                    <label>
                        County Name:
                        <select name="County Name" id="county_name" onChange={handleCountyCodeChange}>County Name
                        </select>
                    </label>
                    {/*<label>*/}
                    {/*    State Code:*/}
                    {/*    <input type="number" value={stateCode} onChange={handleStateCodeChange}/>*/}
                    {/*</label>*/}
                    {/*<label>*/}
                    {/*    County Code:*/}
                    {/*    <input type="number" value={countyCode} onChange={handleCountyCodeChange}/>*/}
                    {/*</label>*/}
                    <button type="submit">Submit</button>
                </form>
                {formSubmitted && cleanedData && predictionResult !== null && (
                    <div>
                        <h2>Prediction Results</h2>
                        <p style={{fontSize: "30px"}}>Next Year's Predicted
                            Yield: {Math.round(predictionResult)} Bushels</p>
                        <canvas id="scatterChart" className="chartCanvas"></canvas>
                        {/* Chart container */}
                    </div>
                )}

                {/* Display error message if there is an error */}
                {error && <div>Error: {error}</div>}
            </header>
        </div>
    );
}

export default App;