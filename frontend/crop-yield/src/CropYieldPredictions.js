import React from 'react';

function CropYieldPrediction({ predictionResult }) {
  return (
    <div>
      <h1>Crop Yield Prediction</h1>
      {predictionResult ? (
        <div>
          <p>Predicted yield: {predictionResult.predictions}</p>
          <p>MSE: {predictionResult.mse}</p>
        </div>
      ) : (
        <p>No prediction results yet.</p>
      )}
    </div>
  );
}

export default CropYieldPrediction;
