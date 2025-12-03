let map;
let marker;

function initMap() {
  map = L.map('map').setView([20.59, 78.96], 5);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
  }).addTo(map);

  map.on('click', function (e) {
    const lat = e.latlng.lat;
    const lng = e.latlng.lng;

    if (marker) map.removeLayer(marker);

    marker = L.marker([lat, lng]).addTo(map);
    
    // Show location immediately
    updateLocationInfo({
      coordinates: `${lat.toFixed(4)}, ${lng.toFixed(4)}`,
      lat: lat,
      lng: lng
    });

    fetchPrediction(lat, lng);
  });

  document.getElementById('reset-btn').addEventListener('click', () => {
    if (marker) map.removeLayer(marker);
    resetBars();
  });
}

async function fetchPrediction(lat, lng) {
  try {
    // Validate coordinates
    if (isNaN(lat) || isNaN(lng) || lat < -90 || lat > 90 || lng < -180 || lng > 180) {
      alert("Invalid coordinates. Please click on a valid location on the map.");
      return;
    }

    // Show loading state
    const bars = document.querySelectorAll(".bar-fill");
    bars.forEach(bar => {
      bar.style.backgroundColor = "#666";
      bar.style.height = "5%";
    });

    const res = await fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      headers: { 
        "Content-Type": "application/json",
        "Accept": "application/json"
      },
      body: JSON.stringify({ latitude: lat, longitude: lng }),
      mode: 'cors',
      credentials: 'omit'
    }).catch(err => {
      // Network error - server might not be running
      throw new TypeError(`Failed to fetch: ${err.message}`);
    });

    // Check if response is ok before parsing JSON
    if (!res.ok) {
      let errorData;
      try {
        errorData = await res.json();
      } catch {
        errorData = { error: `HTTP ${res.status}: ${res.statusText}` };
      }
      throw new Error(errorData.error || `Server error: ${res.status}`);
    }

    let data;
    try {
      data = await res.json();
    } catch (jsonErr) {
      console.error("Failed to parse JSON response:", jsonErr);
      throw new Error("Server returned invalid JSON response");
    }
    
    // Debug logging
    console.log("Prediction response:", data);

    // Validate response structure
    if (!data || typeof data !== 'object') {
      throw new Error("Invalid response: Expected object, got " + typeof data);
    }

    // Handle both old and new response formats
    let eqProb, floodProb, fireProb;
    try {
      if (data.earthquake && typeof data.earthquake === 'object') {
        // New format with risk levels
        eqProb = parseFloat(data.earthquake.probability);
        floodProb = parseFloat(data.flood?.probability);
        fireProb = parseFloat(data.wildfire?.probability);
        
        // Validate probabilities are numbers
        if (isNaN(eqProb) || isNaN(floodProb) || isNaN(fireProb)) {
          throw new Error("Invalid probability values in response");
        }
        
        // Update risk level displays
        updateRiskInfo("eq", data.earthquake);
        updateRiskInfo("flood", data.flood);
        updateRiskInfo("fire", data.wildfire);
        
        // Update location info
        if (data.location) {
          updateLocationInfo(data.location);
        }
        
        // Update overall risk
        if (data.overall) {
          updateOverallRisk(data.overall);
        }
      } else {
        // Old format (backward compatibility)
        eqProb = parseFloat(data.earthquake);
        floodProb = parseFloat(data.flood);
        fireProb = parseFloat(data.wildfire);
      }

      // Validate response data
      if (isNaN(eqProb) || isNaN(floodProb) || isNaN(fireProb)) {
        console.error("Invalid probabilities:", { eqProb, floodProb, fireProb });
        throw new Error("Invalid response format: Missing or invalid probability values");
      }
    } catch (parseErr) {
      console.error("Error parsing response:", parseErr, "Response data:", data);
      throw new Error("Failed to parse prediction response: " + parseErr.message);
    }

    // Update UI with predictions
    animateBar("eq", eqProb);
    animateBar("flood", floodProb);
    animateBar("fire", fireProb);
    
    // Add percentage text to bars
    updateBarPercentage("eq", eqProb);
    updateBarPercentage("flood", floodProb);
    updateBarPercentage("fire", fireProb);

    // Update counts
    document.getElementById("count-eq").textContent = `${data.counts?.earthquake || 0} nearby`;
    document.getElementById("count-flood").textContent = `${data.counts?.flood || 0} nearby`;
    document.getElementById("count-fire").textContent = `${data.counts?.wildfire || 0} nearby`;

    // Update dashboard color (using probabilities)
    updateDashboardColor({
      earthquake: eqProb,
      flood: floodProb,
      wildfire: fireProb
    });

  } catch (err) {
    console.error("Prediction error:", err);
    
    // Reset bars to indicate error
    resetBars();
    
    // Check if it's a network error
    let errorMsg = err.message || "Unknown error occurred";
    
    if (err instanceof TypeError && err.message.includes("fetch")) {
      errorMsg = "Cannot connect to server. Please ensure:\n\n" +
                 "1. Flask server is running (python app.py)\n" +
                 "2. Server is accessible at http://127.0.0.1:5000\n" +
                 "3. No firewall is blocking the connection";
    } else if (err.message.includes("Failed to fetch")) {
      errorMsg = "Failed to connect to server. Make sure Flask server is running on port 5000.";
    }
    
    alert(`⚠️ ${errorMsg}`);
  }
}

function animateBar(type, percent) {
  const fill = document.getElementById(`fill-${type}`);
  if (!fill) {
    console.error(`Bar fill not found: fill-${type}`);
    return;
  }

  // Ensure percent is a valid number between 0 and 100
  percent = Math.max(0, Math.min(100, parseFloat(percent) || 0));
  
  // Calculate height - ensure small values are still visible
  // For values > 0 but < 5%, show at least 5% so it's visible
  let displayHeight = percent;
  if (percent > 0 && percent < 5) {
    displayHeight = 5; // Minimum 5% for visibility
  }
  
  fill.style.height = `${displayHeight}%`;
  fill.style.minHeight = percent === 0 ? "0px" : "2px"; // Small minimum for > 0
  fill.style.opacity = percent === 0 ? "0.3" : "1"; // Fade out if 0

  // Set color based on risk level
  let color = "#00ff99"; // Default green
  if (percent > 70) color = "#ff4444"; // Red
  else if (percent > 40) color = "#ffa500"; // Orange
  else if (percent > 0) color = "#00ff99"; // Green
  fill.style.backgroundColor = color;

  // Add glow effect for high risk
  if (percent > 80) {
    fill.classList.add("glow");
  } else {
    fill.classList.remove("glow");
  }
  
  console.log(`Bar ${type}: ${percent}% - display height: ${displayHeight}%`);
}

function updateBarPercentage(type, percent) {
  // Ensure percent is a valid number
  percent = Math.max(0, Math.min(100, parseFloat(percent) || 0));
  
  // Update or create percentage label
  const bar = document.getElementById(`bar-${type}`);
  if (!bar) return;
  
  // Remove existing percentage if any
  const existingPct = bar.querySelector('.bar-percentage');
  if (existingPct) {
    existingPct.remove();
  }
  
  // Add percentage label above the bar fill
  const percentageLabel = document.createElement('div');
  percentageLabel.className = 'bar-percentage';
  percentageLabel.textContent = `${percent.toFixed(1)}%`;
  percentageLabel.style.cssText = `
    position: absolute;
    top: 5px;
    left: 50%;
    transform: translateX(-50%);
    font-size: 0.9rem;
    font-weight: bold;
    color: #00ff99;
    text-shadow: 0 0 5px #00ff99;
    z-index: 10;
  `;
  
  bar.appendChild(percentageLabel);
}

function updateDashboardColor(data) {
  const dashboard = document.querySelector(".dashboard");
  const maxRisk = Math.max(data.earthquake, data.flood, data.wildfire);

  if (maxRisk > 90) dashboard.style.backgroundColor = "#ff4d4d";
  else if (maxRisk > 70) dashboard.style.backgroundColor = "#ffa500";
  else if (maxRisk > 40) dashboard.style.backgroundColor = "#ffff66";
  else dashboard.style.backgroundColor = "#111";
}

function resetBars() {
  document.querySelectorAll(".bar-fill").forEach(fill => {
    fill.style.height = "0";
    fill.classList.remove("glow");
    fill.style.backgroundColor = "green";
  });

  document.querySelectorAll(".bar-count").forEach(count => {
    count.textContent = "0 nearby";
  });
  
  // Reset risk badges and messages
  document.querySelectorAll(".risk-badge").forEach(badge => {
    badge.textContent = "";
  });
  document.querySelectorAll(".risk-message").forEach(msg => {
    msg.textContent = "";
  });
  
  // Hide risk summary
  const riskSummary = document.getElementById("risk-summary");
  if (riskSummary) riskSummary.style.display = "none";
  
  // Hide location
  const locDisplay = document.getElementById('location-display');
  if (locDisplay) locDisplay.style.display = 'none';

  document.querySelector(".dashboard").style.backgroundColor = "#111";
}

// Check server status on page load
async function checkServerStatus() {
  try {
    const res = await fetch("http://127.0.0.1:5000/health", {
      method: "GET",
      mode: 'cors',
      credentials: 'omit'
    });
    if (res.ok) {
      const statusDiv = document.getElementById("server-status");
      if (statusDiv) {
        statusDiv.style.display = "none";
      }
      return true;
    }
  } catch (err) {
    const statusDiv = document.getElementById("server-status");
    if (statusDiv) {
      statusDiv.style.display = "block";
      statusDiv.innerHTML = "⚠️ Server not running!<br>Please run: <code>python app.py</code>";
      statusDiv.style.background = "#ff4444";
    }
    console.log("Server check failed:", err);
    return false;
  }
}

function updateRiskInfo(type, riskData) {
  // Safety check
  if (!riskData || typeof riskData !== 'object') {
    console.warn(`Invalid risk data for ${type}:`, riskData);
    return;
  }
  
  // Update risk level badge if element exists
  const riskBadge = document.getElementById(`risk-${type}`);
  if (riskBadge && riskData.level) {
    try {
      riskBadge.textContent = riskData.level;
      const levelClass = riskData.level.toLowerCase().replace(/\s+/g, '-');
      riskBadge.className = `risk-badge risk-${levelClass}`;
    } catch (e) {
      console.error(`Error updating risk badge for ${type}:`, e);
    }
  }
  
  // Update risk message
  const riskMessage = document.getElementById(`message-${type}`);
  if (riskMessage && riskData.message) {
    try {
      riskMessage.textContent = riskData.message;
    } catch (e) {
      console.error(`Error updating risk message for ${type}:`, e);
    }
  }
}

function updateLocationInfo(location) {
  if (!location || typeof location !== 'object') {
    console.warn("Invalid location data:", location);
    return;
  }
  
  const locDisplay = document.getElementById('location-display');
  if (locDisplay) {
    try {
      const coords = location.coordinates || `${location.lat?.toFixed(4) || 'N/A'}, ${location.lng?.toFixed(4) || 'N/A'}`;
      locDisplay.textContent = `📍 ${coords}`;
      locDisplay.style.display = 'block';
    } catch (e) {
      console.error("Error updating location info:", e);
    }
  }
}

function updateOverallRisk(overall) {
  if (!overall || typeof overall !== 'object') {
    console.warn("Invalid overall risk data:", overall);
    return;
  }
  
  const riskSummary = document.getElementById('risk-summary');
  if (riskSummary) {
    try {
      riskSummary.style.display = 'block';
    } catch (e) {
      console.error("Error showing risk summary:", e);
    }
  }
  
  const overallRisk = document.getElementById('overall-risk');
  if (overallRisk && overall.risk_level) {
    try {
      const probText = overall.max_probability !== undefined ? ` (${overall.max_probability}%)` : '';
      overallRisk.textContent = `Overall Risk: ${overall.risk_level}${probText}`;
      const levelClass = overall.risk_level.toLowerCase().replace(/\s+/g, '-');
      overallRisk.className = `overall-risk risk-${levelClass}`;
    } catch (e) {
      console.error("Error updating overall risk:", e);
    }
  }
  
  const overallMessage = document.getElementById('overall-message');
  if (overallMessage && overall.message) {
    try {
      overallMessage.textContent = overall.message;
    } catch (e) {
      console.error("Error updating overall message:", e);
    }
  }
}

document.addEventListener("DOMContentLoaded", function() {
  checkServerStatus();
  initMap();
  
  // Check server status every 10 seconds
  setInterval(checkServerStatus, 10000);
});
