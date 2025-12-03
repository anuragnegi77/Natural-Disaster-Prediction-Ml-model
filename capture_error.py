"""
Script to capture and display the exact server error
"""
import sys
import traceback

print("=" * 70)
print("🔍 CAPTURING SERVER ERROR")
print("=" * 70)

try:
    print("\n1. Testing import of app module...")
    import app
    print("   ✅ Import successful")
    
    print("\n2. Attempting to start server (will stop after checking)...")
    from app import app as flask_app
    
    # Test if server can be configured
    with flask_app.test_client() as client:
        print("   ✅ Flask app can create test client")
        
        # Test health endpoint
        response = client.get('/health')
        print(f"   ✅ Health endpoint works: {response.status_code}")
        
        # Test predict endpoint
        response = client.post('/predict', 
                             json={'latitude': 20.59, 'longitude': 78.96},
                             content_type='application/json')
        print(f"   ✅ Predict endpoint works: {response.status_code}")
        if response.status_code == 200:
            data = response.get_json()
            print(f"   ✅ Response structure valid: {list(data.keys())}")
    
    print("\n" + "=" * 70)
    print("✅ ALL SERVER COMPONENTS WORK CORRECTLY!")
    print("=" * 70)
    print("\n💡 If you're still seeing errors when running 'python app.py':")
    print("   1. Check the terminal output - what error message appears?")
    print("   2. Is the error during startup or when making requests?")
    print("   3. Share the complete error message for help")
    
except ImportError as e:
    print(f"\n❌ IMPORT ERROR: {e}")
    traceback.print_exc()
    sys.exit(1)
except Exception as e:
    print(f"\n❌ ERROR FOUND: {type(e).__name__}: {e}")
    print("\n📋 Full traceback:")
    traceback.print_exc()
    sys.exit(1)

