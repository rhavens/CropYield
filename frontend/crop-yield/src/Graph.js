import React, { useEffect } from 'react';
import Chart from 'chart.js/auto';

function Graph({ data }) {
  useEffect(() => {
    if (data) {
      const ctx = document.getElementById('myChart').getContext('2d');
      new Chart(ctx, {
        type: 'line',
        data: {
          labels: data.labels,
          datasets: [{
            label: 'Historical Yield',
            data: data.historicalYield,
            borderColor: 'blue',
            fill: false
          }, {
            label: 'Predicted Yield for Next Year',
            data: data.predictedYield,
            borderColor: 'red',
            fill: false
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false
        }
      });
    }
  }, [data]);

  return (
    <div>
      <canvas id="myChart" width="400" height="400"></canvas>
    </div>
  );
}

export default Graph;
