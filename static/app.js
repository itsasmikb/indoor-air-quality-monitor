const $ = (id) => document.getElementById(id);
const number = (value, digits = 1) => Number(value).toLocaleString(undefined, { maximumFractionDigits: digits });
const setMeter = (id, value, max) => { $(id).style.width = `${Math.max(0, Math.min(100, Number(value) / max * 100))}%`; };

function renderChart(rows) {
  const host = $("chart");
  $("history-count").textContent = `${rows.length} saved reading${rows.length === 1 ? "" : "s"}`;
  if (rows.length < 2) {
    host.className = "chart-empty";
    host.textContent = rows.length ? "One saved reading. Submit more sensor readings to see a trend." : "Saved readings will appear here after sensor data is submitted.";
    return;
  }
  const width = 680, height = 215, pad = { l: 35, r: 12, t: 14, b: 24 };
  const plotW = width - pad.l - pad.r, plotH = height - pad.t - pad.b;
  const x = (i) => pad.l + i / (rows.length - 1) * plotW;
  const y = (v, max) => pad.t + plotH - Math.max(0, Math.min(max, Number(v))) / max * plotH;
  const path = (key, max) => rows.map((row, i) => `${i ? "L" : "M"} ${x(i).toFixed(1)} ${y(row[key], max).toFixed(1)}`).join(" ");
  const grid = [0, 1, 2, 3].map(i => {
    const gy = pad.t + i * plotH / 3;
    return `<line x1="${pad.l}" y1="${gy}" x2="${width-pad.r}" y2="${gy}" stroke="#29404e" stroke-dasharray="3 5"/>`;
  }).join("");
  host.className = "";
  host.innerHTML = `<svg class="chart" viewBox="0 0 ${width} ${height}" role="img" aria-label="Trend of saved AQI and PM2.5 readings">${grid}<path d="${path("AQI", 300)}" fill="none" stroke="#9fe2ca" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/><path d="${path("PM2.5", 150)}" fill="none" stroke="#7fc7e8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><text x="3" y="18" fill="#94a8b4" font-size="10">300</text><text x="3" y="${height-28}" fill="#94a8b4" font-size="10">0</text><text x="${pad.l}" y="${height-5}" fill="#94a8b4" font-size="10">Oldest</text><text x="${width-pad.r}" y="${height-5}" fill="#94a8b4" font-size="10" text-anchor="end">Latest</text></svg>`;
}

async function loadHistory() {
  try {
    const response = await fetch("/api/historical_data?limit=30");
    if (!response.ok) throw new Error("Could not load saved history.");
    renderChart(await response.json());
  } catch {
    $("chart").className = "chart-empty";
    $("chart").textContent = "History is temporarily unavailable.";
  }
}

function updateReading(data) {
  const readings = data.sensor_data;
  $("pm25").textContent = number(readings["PM2.5"]);
  $("pm10").textContent = number(readings.PM10);
  $("co2").textContent = number(readings.CO2, 0);
  $("aqi").textContent = data.aqi;
  $("category").textContent = data.aqi_category;
  $("timestamp").textContent = `Last updated ${new Date(data.timestamp).toLocaleString()}`;
  $("guidance").replaceChildren(...data.recommendations.map(text => {
    const li = document.createElement("li"); li.textContent = text; return li;
  }));
  const color = data.aqi <= 50 ? "#9fe2ca" : data.aqi <= 100 ? "#efbd79" : "#f08b83";
  $("aqi").style.color = color; $("category").style.color = color;
  $("aqi-meter").style.background = color;
  setMeter("pm25-meter", readings["PM2.5"], 150);
  setMeter("pm10-meter", readings.PM10, 300);
  setMeter("co2-meter", readings.CO2, 2000);
  setMeter("aqi-meter", data.aqi, 300);
  $("notice").className = "notice";
  $("notice").textContent = data.is_simulated
    ? "Demo readings · generated locally, not from a physical sensor."
    : "Sensor reading received and saved.";
}

async function refreshReading() {
  $("refresh").disabled = true;
  $("notice").className = "notice";
  $("notice").textContent = "Fetching a new reading…";
  try {
    const response = await fetch("/api/sensor_data");
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Unable to fetch reading.");
    updateReading(data);
    await loadHistory();
  } catch (error) {
    $("notice").className = "notice error";
    $("notice").textContent = error.message || "Unable to fetch reading.";
  } finally {
    $("refresh").disabled = false;
  }
}
$("refresh").addEventListener("click", refreshReading);
refreshReading();
