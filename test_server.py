"""
Quick test script to verify the Flask server is running and responding
"""
import requests
import json

def test_server():
    base_url = "http://127.0.0.1:5000"
    
    print("Testing Flask server connection...\n")
    
    # Test 1: Health check
    try:
        print("1. Testing /health endpoint...")
        response = requests.get(f"{base_url}/health", timeout=2)
        if response.status_code == 200:
            print(f"   ✅ Health check passed: {response.json()}")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("   ❌ Cannot connect to server!")
        print("   💡 Make sure to run: python app.py")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test 2: Predict endpoint
    try:
        print("\n2. Testing /predict endpoint...")
        test_data = {
            "latitude": 20.59,
            "longitude": 78.96
        }
        response = requests.post(
            f"{base_url}/predict",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Prediction successful!")
            print(f"   📊 Results:")
            print(f"      - Earthquake: {result.get('earthquake', 'N/A')}%")
            print(f"      - Flood: {result.get('flood', 'N/A')}%")
            print(f"      - Wildfire: {result.get('wildfire', 'N/A')}%")
            return True
        else:
            print(f"   ❌ Prediction failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("🧪 DisasterScope Server Test")
    print("=" * 50 + "\n")
    
    if test_server():
        print("\n" + "=" * 50)
        print("✅ All tests passed! Server is working correctly.")
        print("=" * 50)
    else:
        print("\n" + "=" * 50)
        print("❌ Tests failed. Please check the server.")
        print("=" * 50)

