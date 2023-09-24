let vehicleSpeeds = [];
let speedLimits = [];
let barChart;
let lineChart;

// Function to generate charts from the given data
function generateCharts(filteredData) {
  const sensorLabels = filteredData.map((_, index) => "Sensor " + (index + 1));

  // Destroy previous chart instances if they exist
  if (barChart) {
    barChart.destroy();
  }
  if (lineChart) {
    lineChart.destroy();
  }

  // Bar Chart
  const barCtx = document.getElementById("bar-chart").getContext("2d");
  barChart = new Chart(barCtx, {
    type: "bar",
    data: {
      labels: sensorLabels,
      datasets: [
        {
          label: "Vehicle Speed",
          data: vehicleSpeeds,
          backgroundColor: "rgba(75, 192, 192, 0.2)",
          borderColor: "rgba(75, 192, 192, 1)",
          borderWidth: 1,
        },
      ],
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
        },
      },
    },
  });

  // Line Chart
  const lineCtx = document.getElementById("line-chart").getContext("2d");
  lineChart = new Chart(lineCtx, {
    type: "line",
    data: {
      labels: sensorLabels,
      datasets: [
        {
          label: "Speed Limit",
          data: speedLimits,
          backgroundColor: "rgba(255, 99, 132, 0.2)",
          borderColor: "rgba(255, 99, 132, 1)",
          borderWidth: 1,
        },
      ],
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
        },
      },
    },
  });
}
