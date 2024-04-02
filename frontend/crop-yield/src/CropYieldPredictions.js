// CropYieldPredictions.js
import React from 'react';

const CropYieldPrediction = ({ predictionResult }) => {
  if (!predictionResult) {
    return null;
  }

  return (
    <div>
      <h2>Prediction Results</h2>
      <p>Next year's predicted yield:</p>
      <img src={predictionResult.graph_image} alt="Prediction Graph" />
    </div>
  );
};

export default CropYieldPrediction;
