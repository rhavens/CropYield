import React, {useState, useEffect} from 'react';
import './App.css';
import cornImage from './cornimage.jpeg';

function App() {
    const [countyCode, setCountyCode] = useState('');
    const [stateCode, setStateCode] = useState('');
    const [predictionResult, setPredictionResult] = useState(null);
    const [error, setError] = useState(null);
    const [formSubmitted, setFormSubmitted] = useState(false);
    const [graphImage, setGraphImage] = useState(null);
    const [stateCountyCodeMap, setStateCountyCodeMap] = useState(null);


    /*
    Format of stateCountyCodeMap
    map = {
        state_name: {
            code: value
            counties: {
                county_name: value
                county_name: value
                ...
            }
        }
        ...
    }
     */
    async function createStateCountyCodeMap() {
        console.log("creating code map")
        const response = await fetch('./name_code_map.csv');
        const text = await response.text();
        // const text = fs.readFileSync('./name_code_map.csv')
        const rows = text.split('\n');
        const data = rows.map(row => row.split(','));

        const map = {}

        data.forEach(row => {
            const state_name = row[0]
            const state_code = Number(row[1])
            const county_name = row[2]
            const county_code = Number(row[3])

            if (state_name in map) {
                map[state_name]["counties"][county_name] = county_code;
            } else {
                map[state_name] = {};
                map[state_name][state_code] = state_code;
                map[state_name]["counties"] = {}
                map[state_name]["counties"][county_name] = county_code;
            }
        });
        setStateCountyCodeMap(map);
    }

    const handleCountyCodeChange = (event) => {
        setCountyCode(event.target.value);
    };

    const handleStateCodeChange = (event) => {
        setStateCode(event.target.value);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        setFormSubmitted(true);

        try {
            //Adjust to whatever the IP will be for the server
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
            console.log(data); // Check if the response data is correct

            setPredictionResult(data.nextYearPrediction); // Update prediction result state
            setGraphImage(data.graph_image);
        } catch (error) {
            console.error('Error:', error);
            setError(error.message);
        }

    };

    useEffect(() => {
        console.log('graphImage:', graphImage); // Log the graphImage state
    }, [graphImage]);

  function generateStateDropdown() {
        console.log("dropdown");
        const dropdown = document.getElementById("state_name");
        console.log(stateCountyCodeMap);
        for (let state in stateCountyCodeMap) {
            const option = document.createElement("option");
            option.value = state;
            option.text = state;
            dropdown.appendChild(option)
        }
    }

    return (
        <div className="App">
            <header className="App-header">
                <h1>Corn Crop Yield Prediction</h1>
                <img src={cornImage} alt="corn-image" style={{width: '10%', height: 'auto'}}></img>
                <p>Please select your county and state code.</p>
                <p>The model will display future predictions for your county's yield.</p>
                <form onSubmit={handleSubmit}>
                    <label>
                        State Name:
                        <select name="State Name" id="state_name" onChange={handleStateCodeChange}>State Name
                            <option> option1 </option>
                            <option> option2</option>
                            <option> option3</option>
                        </select>
                    </label>
                    <label>
                        State Code:
                        <input type="number" value={stateCode} onChange={handleStateCodeChange}/>
                    </label>
                    <label>
                        County Code:
                        <input type="number" value={countyCode} onChange={handleCountyCodeChange}/>
                    </label>
                    <button type="submit">Submit</button>
                </form>
                {formSubmitted && predictionResult !== null && (
                    <div>
                        <h2>Prediction Results</h2>
                        <p style={{fontSize: "30px"}}>Next year's predicted
                            yield: {Math.round(predictionResult)} bushels</p>

                        {graphImage && <img src={`${graphImage}?${new Date().getTime()}`} alt="Prediction Graph"/>}
                    </div>
                )}

                {/* Display error message if there is an error */}
                {error && <div>Error: {error}</div>}
            </header>
        </div>
    );
}

export default App;
