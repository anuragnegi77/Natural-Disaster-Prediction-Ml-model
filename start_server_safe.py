"""
Safe server startup with comprehensive error handling
Use this if app.py has issues
"""
import sys
import traceback
import os

print("\n" + "=" * 70)
print("DISASTERSCOPE - SAFE SERVER STARTUP")
print("=" * 70)

try:
    # Step 1: Validate environment
    print("\n[Step 1] Validating environment...")
    if not os.path.exists('index.html'):
        print("WARNING: index.html not found in current directory")
        print(f"   Current directory: {os.getcwd()}")
    else:
        print("   OK: index.html found")
    
    if not os.path.exists('models'):
        print("   ERROR: models/ directory not found!")
        sys.exit(1)
    else:
        print("   OK: models/ directory found")
    
    # Step 2: Import and setup
    print("\n[Step 2] Loading application...")
    import app
    from app import app as flask_app
    
    print("   OK: Application loaded")
    
    # Step 3: Start server
    print("\n[Step 3] Starting server...")
    print("=" * 70)
    print("Server starting on http://127.0.0.1:5000")
    print("Press Ctrl+C to stop")
    print("=" * 70 + "\n")
    
    flask_app.run(debug=True, port=5000, host='127.0.0.1', use_reloader=False)
    
except KeyboardInterrupt:
    print("\n\nServer stopped by user")
    sys.exit(0)
except ImportError as e:
    print(f"\nIMPORT ERROR: {e}")
    print("\nSolution: Install missing dependencies")
    print("   pip install flask flask-cors pandas scikit-learn numpy")
    traceback.print_exc()
    sys.exit(1)
except OSError as e:
    error_str = str(e)
    if "Address already in use" in error_str or "port" in error_str.lower():
        print(f"\nPORT ERROR: {error_str}")
        print("\nSolutions:")
        print("   1. Close other applications using port 5000")
        print("   2. Run: netstat -ano | findstr :5000")
        print("   3. Change port in this file (line with app.run)")
    else:
        print(f"\nSYSTEM ERROR: {error_str}")
        traceback.print_exc()
    sys.exit(1)
except Exception as e:
    print(f"\nUNEXPECTED ERROR: {type(e).__name__}")
    print(f"   Message: {str(e)}")
    print("\nFull error details:")
    traceback.print_exc()
    sys.exit(1)

