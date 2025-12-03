# 🐛 Debugging Guide for DisasterScope

## Quick Debugging Steps

### 1. Run the Debug Tool
```bash
python debug.py
```

This will check:
- ✅ All dependencies are installed
- ✅ CSV files exist and are readable
- ✅ Models can be loaded
- ✅ Predictions work correctly

### 2. Check Browser Console
Open your browser's Developer Tools (F12) and check:
- **Console tab**: Look for JavaScript errors
- **Network tab**: Check if API requests are successful (status 200)
- **Response tab**: View the actual API response data

### 3. Check Flask Server Logs
When running `python app.py`, watch the terminal for:
- Error messages
- Warning messages
- Debug information

## Common Issues & Solutions

### Issue: "Failed to fetch"
**Possible causes:**
1. Flask server not running
   - **Solution**: Run `python app.py` in a terminal
2. Wrong port
   - **Solution**: Make sure server is on port 5000
3. CORS errors
   - **Solution**: CORS is enabled, but check browser console

**Debug steps:**
```bash
# Test if server is running
python -c "import requests; print(requests.get('http://127.0.0.1:5000/health').json())"
```

### Issue: "Invalid response format"
**Possible causes:**
1. Response structure changed
2. Server returned error instead of data
3. JSON parsing failed

**Debug steps:**
- Check browser Network tab for the actual response
- Check server logs for errors
- Verify response format matches expected structure

### Issue: "Model error"
**Possible causes:**
1. Model files corrupted
2. Wrong feature names
3. Missing data

**Debug steps:**
```bash
# Run diagnostic
python debug.py

# Test specific model
python check_models.py
```

### Issue: Predictions always show 0%
**Possible causes:**
1. Models not loading correctly
2. Input features don't match model expectations
3. Probability calculation issue

**Debug steps:**
- Check server logs for model loading errors
- Verify feature names match what models expect
- Test predictions with `debug.py`

## Debugging Features

### 1. Enhanced Error Messages
All errors now include:
- Specific error type
- Location in code
- Suggested solutions

### 2. Console Logging
Frontend logs:
- API requests and responses
- Parsing errors
- UI update errors

Backend logs:
- Model prediction errors
- Data validation errors
- Request processing errors

### 3. Validation Checks
- Response format validation
- Data type checking
- Null/undefined handling
- Probability range validation

## Debug Endpoints

### Health Check
```
GET http://127.0.0.1:5000/health
```
Returns server status

### Statistics
```
GET http://127.0.0.1:5000/stats
```
Returns dataset information

## Debug Mode

The app runs in debug mode by default, which provides:
- Detailed error messages
- Stack traces
- Request logging
- Development-friendly error pages

## Getting Help

If you still encounter issues:

1. **Run debug tool**: `python debug.py`
2. **Check browser console**: F12 → Console tab
3. **Check server logs**: Terminal running `python app.py`
4. **Test manually**:
   ```bash
   python -c "
   import requests
   r = requests.post('http://127.0.0.1:5000/predict', 
                     json={'latitude': 20.59, 'longitude': 78.96})
   print(r.status_code)
   print(r.json())
   "
   ```

## Log Files

Currently logs go to:
- **Browser console**: Frontend errors
- **Terminal output**: Backend errors

For production, consider adding file logging in `app.py`.

