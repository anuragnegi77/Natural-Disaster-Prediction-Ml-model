# 🛠️ Server Error - Complete Fix Guide

## If Server Errors Are Still Occurring

### Step 1: Get the Exact Error
**Run this command and copy the FULL error message:**
```bash
python app.py
```

**OR run diagnostics:**
```bash
python debug.py
python check_server_error.py
```

### Step 2: Common Server Errors & Fixes

#### ❌ Error: "Port 5000 already in use"
**Quick Fix:**
```bash
# Option 1: Find and kill the process
netstat -ano | findstr :5000
# Note the PID number, then:
taskkill /PID <PID_NUMBER> /F

# Option 2: Change port
# Edit app.py, change line 433:
app.run(debug=True, port=5001, host='127.0.0.1')
# Then update main.js line 43 to use port 5001
```

#### ❌ Error: "Template not found" or "index.html not found"
**Quick Fix:**
- Make sure `index.html` is in the project root (same folder as `app.py`)
- Verify you're running `python app.py` from the correct directory
- Check: `ls index.html` or `dir index.html`

#### ❌ Error: "Module not found" or Import errors
**Quick Fix:**
```bash
pip install flask flask-cors pandas scikit-learn numpy
```

#### ❌ Error: "Model file not found"
**Quick Fix:**
- Check `models/` folder exists
- Verify these files:
  - `models/earthquake_model.pkl`
  - `models/flood_model.pkl`  
  - `models/wildfire_model.pkl`

#### ❌ Error: Runtime errors during prediction
**Check:**
1. Browser console (F12 → Console tab)
2. Server terminal output (where you ran `python app.py`)
3. Network tab (F12 → Network tab) - check `/predict` request

### Step 3: Enhanced Error Logging

The server now has:
- ✅ Global error handler (catches all unhandled errors)
- ✅ Detailed error messages
- ✅ Stack traces for debugging
- ✅ Port availability check
- ✅ File existence validation

### Step 4: Manual Testing

**Test server startup:**
```bash
python app.py
# Watch for any error messages
# Server should show "Running on http://127.0.0.1:5000"
```

**Test API endpoint:**
```bash
python -c "
import requests
r = requests.post('http://127.0.0.1:5000/predict',
                  json={'latitude': 20.59, 'longitude': 78.96})
print('Status:', r.status_code)
print('Response:', r.json())
"
```

### Step 5: Share Error Details

If errors persist, please share:
1. **Full error message** from terminal (copy/paste)
2. **Output of:** `python debug.py`
3. **Browser console errors** (F12 → Console)
4. **What you were doing** when error occurred

## Quick Checklist

- [ ] Python installed (python --version)
- [ ] All dependencies installed (pip install flask flask-cors pandas scikit-learn numpy)
- [ ] Models exist (models/*.pkl files)
- [ ] CSV files exist (earthquakes.csv, floods.csv, wildfires.csv)
- [ ] index.html exists in project root
- [ ] Port 5000 not in use (or changed port)
- [ ] Running from project root directory
- [ ] No firewall blocking port 5000

## Alternative: Run with Verbose Logging

Add this at the top of app.py for more details:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Still Not Working?

1. **Run all diagnostics:**
   ```bash
   python debug.py
   python test_server_error.py
   python check_server_error.py
   ```

2. **Check Python version:**
   ```bash
   python --version
   # Should be 3.7 or higher
   ```

3. **Reinstall dependencies:**
   ```bash
   pip install --upgrade flask flask-cors pandas scikit-learn numpy
   ```

4. **Clear Python cache:**
   ```bash
   # Delete __pycache__ folders
   # Windows PowerShell:
   Get-ChildItem -Path . -Filter __pycache__ -Recurse | Remove-Item -Recurse -Force
   ```

