# 🔧 Server Error Fix Guide

## Quick Fix Steps

### Step 1: Check What Error You're Seeing
Run this to diagnose:
```bash
python debug.py
python test_server_error.py
```

### Step 2: Common Errors & Solutions

#### Error: "Address already in use" or "Port 5000 already in use"
**Solution:**
```bash
# Find what's using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F

# OR change the port in app.py (last line):
# app.run(debug=True, port=5001, host='127.0.0.1')
# Then update main.js line 43 to use port 5001
```

#### Error: "Template not found" or "index.html not found"
**Solution:**
- Ensure `index.html` exists in the project root directory
- Check that you're running `python app.py` from the project root
- Verify file path is correct

#### Error: "Module not found" or "Import error"
**Solution:**
```bash
pip install flask flask-cors pandas scikit-learn numpy
```

#### Error: "Model file not found"
**Solution:**
- Ensure `models/` folder exists
- Check these files exist:
  - `models/earthquake_model.pkl`
  - `models/flood_model.pkl`
  - `models/wildfire_model.pkl`

#### Error: Runtime errors during prediction
**Solution:**
- Check browser console (F12) for JavaScript errors
- Check server terminal for Python errors
- Run `python debug.py` to validate setup

### Step 3: Start Server with Better Error Handling

The improved `app.py` now:
- ✅ Checks if port is available before starting
- ✅ Validates all files exist
- ✅ Shows clear error messages
- ✅ Handles template errors gracefully

### Step 4: Verify Server is Running

```bash
# Test health endpoint
python -c "import requests; print(requests.get('http://127.0.0.1:5000/health').json())"
```

Or open in browser: `http://127.0.0.1:5000/health`

## Debugging Checklist

- [ ] Dependencies installed (`pip install -r requirements.txt` or manually)
- [ ] Models exist in `models/` folder
- [ ] CSV files exist in project root
- [ ] `index.html` exists in project root
- [ ] Port 5000 is not in use
- [ ] Running from correct directory
- [ ] Python version compatible (3.7+)

## Getting Detailed Error Information

1. **Server logs**: Watch the terminal running `python app.py`
2. **Browser console**: Press F12 → Console tab
3. **Network tab**: F12 → Network tab (check failed requests)
4. **Debug tool**: Run `python debug.py`

## Still Having Issues?

Share:
1. The exact error message
2. Output from `python debug.py`
3. Output from `python test_server_error.py`
4. Server logs from terminal

