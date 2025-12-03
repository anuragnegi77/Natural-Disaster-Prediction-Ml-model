# 🌍 DisasterScope - Natural Disaster Predictor

## 🚀 Quick Start

### Step 1: Start the Flask Server

**Option A: Double-click to start**
- Windows: Double-click `start_server.bat`
- Or run: `python app.py`

**Option B: Command line**
```bash
python app.py
```

You should see:
```
==================================================
🌍 DisasterScope API Server Starting...
==================================================
 * Running on http://127.0.0.1:5000
```

**⚠️ IMPORTANT:** Keep this terminal window open while using the app!

### Step 2: Open the Web Application

1. Open your web browser
2. Go to: **http://127.0.0.1:5000**
3. Click anywhere on the map to get predictions

## 📋 Requirements

Install dependencies:
```bash
pip install flask flask-cors pandas scikit-learn numpy
```

## 🐛 Troubleshooting

### Error: "Cannot connect to server"

**Solution:** Start the Flask server first!

1. Open a terminal/command prompt
2. Navigate to this folder
3. Run: `python app.py`
4. Keep that terminal window open
5. Then open: http://127.0.0.1:5000 in your browser

### Port 5000 already in use?

Change the port in `app.py` (last line):
```python
app.run(debug=True, port=5001, host='127.0.0.1')  # Change to 5001
```

And update `main.js` line 43:
```javascript
const res = await fetch("http://127.0.0.1:5001/predict", {  // Change port
```

### Models not found?

Make sure these files exist:
- `models/earthquake_model.pkl`
- `models/flood_model.pkl`
- `models/wildfire_model.pkl`

## 📁 Project Structure

```
Anurag-Negi/
├── app.py              # Flask server (START THIS FIRST!)
├── index.html          # Web interface
├── main.js             # Frontend JavaScript
├── style.css           # Styling
├── models/             # ML models
│   ├── earthquake_model.pkl
│   ├── flood_model.pkl
│   └── wildfire_model.pkl
├── earthquakes.csv     # Data files
├── floods.csv
└── wildfires.csv
```

## 🎯 How to Use

1. **Start server:** `python app.py`
2. **Open browser:** http://127.0.0.1:5000
3. **Click on map:** Click anywhere to see disaster risk predictions
4. **View results:** See earthquake, flood, and wildfire risk percentages

## ✅ Testing

Test if server is working:
```bash
python test_server.py
```

Or visit: http://127.0.0.1:5000/health

---

**Need help?** Make sure the Flask server is running before opening the web app!

