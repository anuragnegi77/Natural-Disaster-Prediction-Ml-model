from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import os
import pickle
import pandas as pd
import numpy as np
from math import radians, cos, sin, sqrt, atan2
import traceback
from datetime import datetime
import sys
import socket
try:
    from twilio.rest import Client
    _TWILIO_AVAILABLE = True
except Exception:
    _TWILIO_AVAILABLE = False

# Initialize Flask app
app = Flask(__name__, template_folder=".", static_folder=".")

# Configure Flask to handle errors better
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JSON_SORT_KEYS'] = False

# Enable CORS for all routes and origins
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Global error handler
@app.errorhandler(Exception)
def handle_exception(e):
    """Handle all unhandled exceptions"""
    app.logger.error(f"Unhandled exception: {str(e)}\n{traceback.format_exc()}")
    return jsonify({
        "error": "Internal server error",
        "message": str(e),
        "type": type(e).__name__
    }), 500

# --- Model / Data Loading ---
model_dir = "models"

try:
    earthquake_model = pickle.load(open(os.path.join(model_dir, "earthquake_model.pkl"), "rb"))
    flood_model = pickle.load(open(os.path.join(model_dir, "flood_model.pkl"), "rb"))
    wildfire_model = pickle.load(open(os.path.join(model_dir, "wildfire_model.pkl"), "rb"))
    print("All models loaded successfully")
except Exception as e:
    print(f"Error loading models: {str(e)}")
    raise

# Load CSV data for nearby counts
try:
    earthquakes_df = pd.read_csv("earthquakes.csv")
    floods_df = pd.read_csv("floods.csv")
    wildfires_df = pd.read_csv("wildfires.csv")
    
    # Keep original column names for feature extraction
    # The count_nearby function will handle both 'latitude'/'longitude' and 'lat'/'lon'
    print("CSV data loaded successfully")
    print(f"   Earthquake columns: {list(earthquakes_df.columns)}")
    print(f"   Flood columns: {list(floods_df.columns)}")
    print(f"   Wildfire columns: {list(wildfires_df.columns)}")
except Exception as e:
    print(f"Warning loading CSV data: {str(e)}")
    earthquakes_df = pd.DataFrame()
    floods_df = pd.DataFrame()
    wildfires_df = pd.DataFrame()

# --- Helper Functions ---
def haversine(lat1, lon1, lat2, lon2):
    """Calculate distance between two points on Earth in km"""
    R = 6371  # Earth radius in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

def count_nearby(df, lat, lon, radius_km=100):
    """Count nearby disasters within radius"""
    if df.empty:
        return 0
    
    # Find latitude and longitude columns
    lat_col = None
    lon_col = None
    
    for col in df.columns:
        col_lower = col.lower()
        if col_lower in ['latitude', 'lat'] and lat_col is None:
            lat_col = col
        if col_lower in ['longitude', 'lon', 'lng'] and lon_col is None:
            lon_col = col
    
    if not lat_col or not lon_col:
        return 0
    
    # Filter valid coordinates
    valid_df = df.dropna(subset=[lat_col, lon_col])
    if valid_df.empty:
        return 0
    
    try:
        # Calculate distances and count within radius
        distances = valid_df.apply(
            lambda r: haversine(lat, lon, r[lat_col], r[lon_col]), 
            axis=1
        )
        return int((distances <= radius_km).sum())
    except Exception:
        return 0

def validate_coordinates(lat, lng):
    """Validate latitude and longitude are within valid ranges"""
    if not isinstance(lat, (int, float)) or not isinstance(lng, (int, float)):
        return False, "Coordinates must be numbers"
    if not (-90 <= lat <= 90):
        return False, "Latitude must be between -90 and 90"
    if not (-180 <= lng <= 180):
        return False, "Longitude must be between -180 and 180"
    return True, None

def safe_predict_proba(model, input_df):
    """Safely get prediction probability from model"""
    try:
        # Check if model has predict_proba
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(input_df)
            # Handle different return formats
            if isinstance(proba, np.ndarray):
                if proba.shape[1] > 1:
                    return proba[0][1] * 100  # Probability of class 1
                else:
                    return proba[0][0] * 100
            elif isinstance(proba, list):
                if len(proba) > 0 and isinstance(proba[0], (list, np.ndarray)):
                    if len(proba[0]) > 1:
                        return proba[0][1] * 100
                    else:
                        return proba[0][0] * 100
                return proba[0] * 100 if isinstance(proba[0], (int, float)) else 50.0
        else:
            # If no predict_proba, use predict and convert to probability estimate
            pred = model.predict(input_df)
            if isinstance(pred, (list, np.ndarray)):
                pred_val = pred[0] if len(pred) > 0 else 0
            else:
                pred_val = pred
            # Convert binary prediction to probability estimate
            return 85.0 if pred_val == 1 else 15.0
    except Exception as e:
        raise Exception(f"Prediction error: {str(e)}")

def get_risk_level(probability):
    """Categorize risk level based on probability"""
    if probability >= 70:
        return "High", "High risk - Take immediate precautions"
    elif probability >= 40:
        return "Medium", "Moderate risk - Stay alert"
    elif probability >= 10:
        return "Low", "Low risk - Minimal concern"
    else:
        return "Very Low", "Very low risk - Safe area"

def get_location_info(lat, lng):
    """Get additional location information"""
    # This could be enhanced with reverse geocoding API
    return {
        "coordinates": f"{lat:.4f}, {lng:.4f}",
        "lat": round(lat, 4),
        "lng": round(lng, 4)
    }

def send_notification(phone_number, message_text):
    try:
        if _TWILIO_AVAILABLE:
            account_sid = os.getenv('TWILIO_ACCOUNT_SID')
            auth_token = os.getenv('TWILIO_AUTH_TOKEN')
            from_number = os.getenv('TWILIO_FROM')
            if account_sid and auth_token and from_number:
                client = Client(account_sid, auth_token)
                client.messages.create(
                    to=str(phone_number),
                    from_=from_number,
                    body=message_text
                )
                return True
    except Exception as _e:
        pass
    try:
        app.logger.info(f"Notify {phone_number}: {message_text}")
    except Exception:
        print(f"Notify {phone_number}: {message_text}")
    return False

# Build input matching model's expected features
def build_model_input(model, lat, lng):
    feat_names = getattr(model, 'feature_names_in_', None)
    # Defaults
    eq_magnitude = 5.0
    eq_depth = 10.0
    try:
        if not earthquakes_df.empty and 'magnitude' in earthquakes_df.columns:
            eq_magnitude = float(earthquakes_df['magnitude'].mean())
        if not earthquakes_df.empty and 'depth' in earthquakes_df.columns:
            eq_depth = float(earthquakes_df['depth'].mean())
    except Exception:
        pass

    flood_rainfall = 100.0
    try:
        if not floods_df.empty:
            if 'rainfall' in floods_df.columns:
                flood_rainfall = float(floods_df['rainfall'].mean())
            elif 'Rainfall' in floods_df.columns:
                flood_rainfall = float(floods_df['Rainfall'].mean())
            elif 'FloodProbability' in floods_df.columns:
                flood_rainfall = float(floods_df['FloodProbability'].mean() * 2)
    except Exception:
        pass

    avg_fires = 50000.0
    try:
        if not wildfires_df.empty:
            fires_col = None
            for c in wildfires_df.columns:
                if c.lower() == 'fires':
                    fires_col = c; break
            if fires_col:
                fires_series = pd.to_numeric(wildfires_df[fires_col].astype(str).str.replace(',', ''), errors='coerce')
                val = fires_series.mean()
                if pd.notna(val):
                    avg_fires = float(val)
    except Exception:
        pass

    # If model doesn't specify feature names, default to lat/lon
    if feat_names is None:
        return pd.DataFrame([[lat, lng]], columns=['lat', 'lon'])

    # Construct row matching expected features
    row = []
    for name in feat_names:
        n = str(name)
        n_low = n.lower()
        if n_low in ('lat', 'latitude'):
            row.append(lat)
        elif n_low in ('lon', 'lng', 'longitude'):
            row.append(lng)
        elif n_low == 'magnitude':
            row.append(eq_magnitude)
        elif n_low == 'depth':
            row.append(eq_depth)
        elif n_low == 'rainfall':
            row.append(flood_rainfall)
        elif n_low == 'fires':
            row.append(avg_fires)
        else:
            # Unknown extra feature: use 0.0
            row.append(0.0)
    try:
        return pd.DataFrame([row], columns=list(feat_names))
    except Exception:
        # Fallback to lat/lon only
        return pd.DataFrame([[lat, lng]], columns=['lat', 'lon'])

# --- Routes ---
# Handle CORS preflight requests
@app.route('/predict', methods=['OPTIONS'])
def predict_options():
    return '', 200

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    """
    Predict disaster probabilities for given coordinates.
    Supports both GET (query params lat,lng) and POST (JSON with latitude, longitude).
    """
    try:
        # Extract coordinates from request
        lat = None
        lng = None

        if request.method == "POST":
            data = request.get_json(silent=True) or {}
            lat = data.get("latitude") or data.get("lat")
            lng = data.get("longitude") or data.get("lng")
        else:
            lat = request.args.get('lat', type=float)
            lng = request.args.get('lng', type=float)

        # Validate inputs
        if lat is None or lng is None:
            return jsonify({"error": "Missing latitude or longitude"}), 400

        # Convert to float and validate ranges
        try:
            lat = float(lat)
            lng = float(lng)
        except (TypeError, ValueError):
            return jsonify({"error": "Invalid latitude/longitude format"}), 400

        # Validate coordinate ranges
        valid, error_msg = validate_coordinates(lat, lng)
        if not valid:
            return jsonify({"error": error_msg}), 400

        # Prepare model inputs dynamically to match each model's expected features
        eq_input = build_model_input(earthquake_model, lat, lng)
        flood_input = build_model_input(flood_model, lat, lng)
        wildfire_input = build_model_input(wildfire_model, lat, lng)

        # Make predictions
        try:
            earthquake_prob = safe_predict_proba(earthquake_model, eq_input)
        except Exception as e:
            app.logger.error(f"Earthquake prediction error: {str(e)}\n{traceback.format_exc()}")
            return jsonify({"error": f"Earthquake model error: {str(e)}"}), 500

        try:
            flood_prob = safe_predict_proba(flood_model, flood_input)
        except Exception as e:
            app.logger.error(f"Flood prediction error: {str(e)}\n{traceback.format_exc()}")
            return jsonify({"error": f"Flood model error: {str(e)}"}), 500

        try:
            wildfire_prob = safe_predict_proba(wildfire_model, wildfire_input)
        except Exception as e:
            app.logger.error(f"Wildfire prediction error: {str(e)}\n{traceback.format_exc()}")
            return jsonify({"error": f"Wildfire model error: {str(e)}"}), 500

        # Calculate nearby counts
        eq_count = count_nearby(earthquakes_df, lat, lng, radius_km=100)
        flood_count = count_nearby(floods_df, lat, lng, radius_km=100)
        wildfire_count = count_nearby(wildfires_df, lat, lng, radius_km=100)

        # Ensure probabilities are in valid range
        earthquake_prob = max(0.0, min(100.0, earthquake_prob))
        flood_prob = max(0.0, min(100.0, flood_prob))
        wildfire_prob = max(0.0, min(100.0, wildfire_prob))

        # Get risk levels and recommendations
        try:
            eq_level, eq_message = get_risk_level(earthquake_prob)
        except Exception as e:
            app.logger.warning(f"Error getting earthquake risk level: {e}")
            eq_level, eq_message = "Unknown", "Unable to assess risk"
        
        try:
            flood_level, flood_message = get_risk_level(flood_prob)
        except Exception as e:
            app.logger.warning(f"Error getting flood risk level: {e}")
            flood_level, flood_message = "Unknown", "Unable to assess risk"
        
        try:
            fire_level, fire_message = get_risk_level(wildfire_prob)
        except Exception as e:
            app.logger.warning(f"Error getting wildfire risk level: {e}")
            fire_level, fire_message = "Unknown", "Unable to assess risk"

        # Calculate overall risk
        try:
            max_risk = max(earthquake_prob, flood_prob, wildfire_prob)
            overall_level, overall_message = get_risk_level(max_risk)
        except Exception as e:
            app.logger.warning(f"Error calculating overall risk: {e}")
            max_risk = max(earthquake_prob, flood_prob, wildfire_prob)
            overall_level, overall_message = "Unknown", "Unable to assess overall risk"

        # Get location info
        location_info = get_location_info(lat, lng)

        # Auto-notify if high risk
        try:
            risk_values = {
                'earthquake': float(earthquake_prob),
                'flood': float(flood_prob),
                'wildfire': float(wildfire_prob)
            }
            top_risk_type = max(risk_values, key=risk_values.get)
            if max_risk >= 70:
                send_notification(
                    phone_number='1945',
                    message_text=(
                        f"ALERT: High {top_risk_type.title()} Risk at "
                        f"{lat:.4f},{lng:.4f} - {max_risk:.1f}%"
                    )
                )
        except Exception:
            pass

        # Validate all probabilities before creating response
        try:
            eq_prob_float = round(float(earthquake_prob), 2)
            flood_prob_float = round(float(flood_prob), 2)
            fire_prob_float = round(float(wildfire_prob), 2)
            max_risk_float = round(float(max_risk), 2)
        except (ValueError, TypeError) as e:
            app.logger.error(f"Error converting probabilities to float: {e}")
            return jsonify({"error": "Internal error: Invalid probability values"}), 500
        
        # Ensure all required fields exist
        if not all([eq_level, flood_level, fire_level]):
            app.logger.error(f"Missing risk levels: eq={eq_level}, flood={flood_level}, fire={fire_level}")
        
        response = {
            "earthquake": {
                "probability": eq_prob_float,
                "level": eq_level,
                "message": eq_message or "Risk assessment available"
            },
            "flood": {
                "probability": flood_prob_float,
                "level": flood_level,
                "message": flood_message or "Risk assessment available"
            },
            "wildfire": {
                "probability": fire_prob_float,
                "level": fire_level,
                "message": fire_message or "Risk assessment available"
            },
            "overall": {
                "risk_level": overall_level or "Unknown",
                "max_probability": max_risk_float,
                "message": overall_message or "Risk assessment complete"
            },
            "counts": {
                "earthquake": int(eq_count) if not pd.isna(eq_count) else 0,
                "flood": int(flood_count) if not pd.isna(flood_count) else 0,
                "wildfire": int(wildfire_count) if not pd.isna(wildfire_count) else 0
            },
            "location": location_info or {},
            "timestamp": datetime.now().isoformat()
        }

        # Log successful prediction (optional, for debugging)
        app.logger.debug(f"Prediction successful for {lat}, {lng}: EQ={eq_prob_float}%, Flood={flood_prob_float}%, Fire={fire_prob_float}%")
        
        return jsonify(response)

    except Exception as e:
        app.logger.error(f"Unexpected error in predict: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

# Route to serve the main HTML page
@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        app.logger.error(f"Error rendering template: {str(e)}\n{traceback.format_exc()}")
        # Fallback: return a simple HTML response
        return f"""
        <!DOCTYPE html>
        <html>
        <head><title>DisasterScope</title></head>
        <body>
            <h1>Error loading template</h1>
            <p>Template file not found. Please ensure index.html exists in the project root.</p>
            <p>Error: {str(e)}</p>
        </body>
        </html>
        """, 500

# Health check endpoint
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "models_loaded": True})

# Statistics endpoint
@app.route('/stats', methods=['GET'])
def stats():
    """Get dataset statistics"""
    stats_data = {
        "earthquakes": {
            "total_records": len(earthquakes_df),
            "columns": list(earthquakes_df.columns) if not earthquakes_df.empty else []
        },
        "floods": {
            "total_records": len(floods_df),
            "columns": list(floods_df.columns) if not floods_df.empty else []
        },
        "wildfires": {
            "total_records": len(wildfires_df),
            "columns": list(wildfires_df.columns) if not wildfires_df.empty else []
        }
    }
    return jsonify(stats_data)

if __name__ == '__main__':
    print("\n" + "="*50)
    print("DisasterScope API Server Starting...")
    print("="*50)
    print(f"Models directory: {model_dir}")
    print(f"Earthquake data: {len(earthquakes_df)} records")
    print(f"Flood data: {len(floods_df)} records")
    print(f"Wildfire data: {len(wildfires_df)} records")
    print("="*50)
    
    # Check if port is available
    port = 5000
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(('127.0.0.1', port))
        sock.close()
        print(f"Port {port} is available")
    except OSError:
        print(f"Port {port} is already in use!")
        print(f"Solution: Close other applications using port {port}")
        print(f"   Or change port in app.py (last line): app.run(..., port=5001)")
        print("="*50 + "\n")
        sys.exit(1)
    
    # Check if index.html exists
    if not os.path.exists('index.html'):
        print("WARNING: index.html not found in project root!")
        print("The server will start but '/' route may fail")
    
    print("="*50)
    print("Debug mode: ON (detailed error logging enabled)")
    print("Run 'python debug.py' to diagnose issues")
    print("="*50 + "\n")
    
    # Enable detailed error pages and logging
    app.config['DEBUG'] = True
    app.config['TESTING'] = False
    
    try:
        print(f"\nStarting Flask server on http://127.0.0.1:{port}")
        print("   Press Ctrl+C to stop the server\n")
        app.run(debug=True, port=port, host='127.0.0.1', use_reloader=False)
    except KeyboardInterrupt:
        print("\n\nServer stopped by user")
    except OSError as e:
        error_msg = str(e)
        if "Address already in use" in error_msg or "Only one usage" in error_msg or "address is already in use" in error_msg.lower():
            print(f"\nERROR: Port {port} is already in use!")
            print("Solutions:")
            print(f"   1. Close other applications using port {port}")
            print(f"   2. Find process: netstat -ano | findstr :{port}")
            print(f"   3. Kill process: taskkill /PID <PID> /F")
            print(f"   4. Change port: Edit app.py -> port=5001")
        else:
            print(f"\nServer error: {error_msg}")
            traceback.print_exc()
    except Exception as e:
        print(f"\nUnexpected error starting server: {type(e).__name__}: {str(e)}")
        traceback.print_exc()
        print("\nPlease share this error message for help")