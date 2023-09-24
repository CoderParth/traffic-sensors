const socket = new WebSocket(ws_url);

socket.addEventListener("open", (event) => {
  console.log("WebSocket connected!");
});

let currentQuery = {}; // Object to hold the current query parameters

function sendQuery() {
  setLoading(true);
  const query = {
    location: document.getElementById("location").value,
    min_speed: document.getElementById("min-speed").value,
    max_speed: document.getElementById("max-speed").value,
    min_speed_limit: document.getElementById("min-speed-limit").value,
    max_speed_limit: document.getElementById("max-speed-limit").value,
    start_date: document.getElementById("start-date").value,
    end_date: document.getElementById("end-date").value,
  };

  console.log("query ", query);
  currentQuery = query; // Update the current query object
}

socket.addEventListener("message", (event) => {
  const sensorData = JSON.parse(event.data);
  console.log("sensor data", sensorData);

  // Filter the data based on the current query parameters
  const filteredData = sensorData.data.filter((dataItem) => {
    const speed = parseFloat(dataItem.vehicle_speed);
    const speedLimit = parseFloat(dataItem.speed_limit);
    const lat = parseFloat(dataItem.latitude);
    const lon = parseFloat(dataItem.longitude);

    // Split location only if it's defined and not empty
    const [queryLat, queryLon] = currentQuery.location
      ? currentQuery.location.split(",").map(Number)
      : [null, null];

    // Set start date and end date based on the data item's timestamp
    const itemStartDate = new Date(dataItem.timestamp);
    const itemEndDate = new Date(dataItem.timestamp);
    itemEndDate.setMonth(itemEndDate.getMonth() + 1);

    const queryStartDate = new Date(currentQuery.start_date);
    const queryEndDate = new Date(currentQuery.end_date);

    return (
      (!currentQuery.location || (lat === queryLat && lon === queryLon)) &&
      (!currentQuery.min_speed ||
        speed >= parseFloat(currentQuery.min_speed)) &&
      (!currentQuery.max_speed ||
        speed <= parseFloat(currentQuery.max_speed)) &&
      (!currentQuery.min_speed_limit ||
        speedLimit >= parseFloat(currentQuery.min_speed_limit)) &&
      (!currentQuery.start_date || itemStartDate >= queryStartDate) &&
      (!currentQuery.end_date || itemEndDate <= queryEndDate)
    );
  });

  // Clear previous markers
  map.eachLayer((layer) => {
    if (layer instanceof L.Marker) {
      map.removeLayer(layer);
    }
  });

  // Display the filtered data on the map
  for (const dataItem of filteredData) {
    const id = dataItem.id;
    const lat = parseFloat(dataItem.latitude);
    const lon = parseFloat(dataItem.longitude);
    const speed = dataItem.vehicle_speed;
    const speedLimit = dataItem.speed_limit;

    // The timestamp is the start date/time
    const startDate = new Date(dataItem.timestamp);
    // Create a new Date object for the end date/time, one month later
    const endDate = new Date(startDate);
    endDate.setMonth(endDate.getMonth() + 1);

    // Format dates for display
    const formattedStartDate = startDate.toLocaleString();
    const formattedEndDate = endDate.toLocaleString();

    // Append vehicle speed and speed limit to the arrays
    vehicleSpeeds.push(parseFloat(speed));
    speedLimits.push(parseFloat(speedLimit));

    // Create a marker and add it to the map
    const marker = L.marker([lat, lon], { icon: carIcon }).addTo(map);

    // Bind a popup to the marker displaying all the required information
    marker
      .bindPopup(
        `
        Sensor ID: ${id} <br>
        Latitude: ${lat} <br>
        Longitude: ${lon} <br>
        Start Date: ${formattedStartDate} <br>
        End Date: ${formattedEndDate} <br>
        Vehicle Speed: ${speed} km/h <br>
        Speed Limit: ${speedLimit} km/h
    `
      )
      .openPopup();
  }

  // Reupdate the charts
  generateCharts(filteredData, vehicleSpeeds, speedLimits);

  setLoading(false);
});

socket.addEventListener("close", (event) => {
  console.log("WebSocket closed:", event);
});
