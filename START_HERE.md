# 🌍 DisasterScope - Quick Start Guide

## ⚠️ Important: "Failed to fetch" Error Fix

If you're seeing "Failed to fetch" errors, follow these steps:

### Step 1: Start the Flask Server

**Open a terminal/command prompt and run:**

```bash
python app.py
```

You should see:
```
==================================================
🌍 DisasterScope API Server Starting...
==================================================
📁 Models directory: models
🗺️  Earthquake data: XXX records
🌊 Flood data: XXX records
🔥 Wildfire data: XXX records
==================================================

 * Running on http://127.0.0.1:5000
```

### Step 2: Open the Web Application

**IMPORTANT:** You have TWO options:

#### Option A: Open through Flask Server (RECOMMENDED)
1. Open your web browser
2. Go to: `http://127.0.0.1:5000` or `http://localhost:5000`
3. This ensures all requests work correctly

#### Option B: If using file:// protocol
1. Open `index.html` directly in your browser
2. Make sure Flask server is running (Step 1)
3. If you still get "Failed to fetch", the server might not be accessible

### Step 3: Test the Server

Run the test script to verify everything works:

```bash
python test_server.py
```

This will check:
- ✅ Server is running
- ✅ /predict endpoint works
- ✅ Models are responding correctly

## 🔧 Troubleshooting

### Error: "Failed to fetch"
- ✅ Make sure Flask server is running (`python app.py`)
- ✅ Check that port 5000 is not blocked by firewall
- ✅ Try accessing `http://127.0.0.1:5000/health` in your browser
- ✅ Open the app through `http://127.0.0.1:5000` instead of `file://`

### Error: "Cannot connect to server"
- ✅ Check if another application is using port 5000
- ✅ Try changing the port in `app.py` (last line)
- ✅ Make sure Python and Flask are installed

### Error: "Model not found"
- ✅ Ensure `models/` folder exists
- ✅ Verify these files exist:
  - `models/earthquake_model.pkl`
  - `models/flood_model.pkl`
  - `models/wildfire_model.pkl`

## 📝 Usage

1. Start the server: `python app.py`
2. Open browser: `http://127.0.0.1:5000`
3. Click anywhere on the map
4. See disaster risk predictions!

## 🛠️ Dependencies

Make sure you have installed:
```bash
pip install flask flask-cors pandas scikit-learn numpy
```

---

**Happy Predicting! 🌍**

