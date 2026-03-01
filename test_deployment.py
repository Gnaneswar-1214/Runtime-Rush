"""
Test script to verify Railway deployment is working
Run this after deploying to Railway to check if everything is set up correctly
"""
import requests
import sys

def test_deployment(base_url):
    """Test all critical endpoints"""
    print(f"🧪 Testing deployment at: {base_url}\n")
    
    tests_passed = 0
    tests_failed = 0
    
    # Test 1: Health check
    print("1️⃣ Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            print("   ✅ Health check passed")
            tests_passed += 1
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            tests_failed += 1
    except Exception as e:
        print(f"   ❌ Health check error: {e}")
        tests_failed += 1
    
    # Test 2: Initialize database
    print("\n2️⃣ Initializing database...")
    try:
        response = requests.post(f"{base_url}/initialize-db", timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Database initialized: {data}")
            tests_passed += 1
        else:
            print(f"   ❌ Database initialization failed: {response.status_code}")
            print(f"   Response: {response.text}")
            tests_failed += 1
    except Exception as e:
        print(f"   ❌ Database initialization error: {e}")
        tests_failed += 1
    
    # Test 3: Get challenges
    print("\n3️⃣ Testing challenges endpoint...")
    try:
        response = requests.get(f"{base_url}/api/challenges", timeout=10)
        if response.status_code == 200:
            challenges = response.json()
            print(f"   ✅ Found {len(challenges)} challenges")
            for ch in challenges:
                print(f"      - Level {ch.get('level')}: {ch.get('title')}")
            tests_passed += 1
        else:
            print(f"   ❌ Challenges fetch failed: {response.status_code}")
            tests_failed += 1
    except Exception as e:
        print(f"   ❌ Challenges fetch error: {e}")
        tests_failed += 1
    
    # Test 4: Admin login
    print("\n4️⃣ Testing admin login...")
    try:
        response = requests.post(
            f"{base_url}/api/auth/login",
            json={"username": "admin", "password": "admin123"},
            timeout=10
        )
        if response.status_code == 200:
            user = response.json()
            if user.get('role') == 'admin':
                print(f"   ✅ Admin login successful: {user.get('username')}")
                tests_passed += 1
            else:
                print(f"   ❌ User is not admin: {user.get('role')}")
                tests_failed += 1
        else:
            print(f"   ❌ Admin login failed: {response.status_code}")
            print(f"   Response: {response.text}")
            tests_failed += 1
    except Exception as e:
        print(f"   ❌ Admin login error: {e}")
        tests_failed += 1
    
    # Test 5: User registration
    print("\n5️⃣ Testing user registration...")
    try:
        response = requests.post(
            f"{base_url}/api/auth/register",
            json={
                "username": f"testuser_{requests.utils.quote(str(requests.utils.default_user_agent())[:5])}",
                "email": "test@example.com",
                "password": "testpass123"
            },
            timeout=10
        )
        if response.status_code == 200:
            user = response.json()
            print(f"   ✅ User registration successful: {user.get('username')}")
            tests_passed += 1
        elif response.status_code == 400 and "already registered" in response.text:
            print(f"   ✅ User registration working (user already exists)")
            tests_passed += 1
        else:
            print(f"   ❌ User registration failed: {response.status_code}")
            print(f"   Response: {response.text}")
            tests_failed += 1
    except Exception as e:
        print(f"   ❌ User registration error: {e}")
        tests_failed += 1
    
    # Summary
    print("\n" + "="*50)
    print(f"📊 Test Results: {tests_passed} passed, {tests_failed} failed")
    print("="*50)
    
    if tests_failed == 0:
        print("🎉 All tests passed! Your deployment is working correctly.")
        print("\n📝 Admin credentials:")
        print("   Username: admin")
        print("   Password: admin123")
        return True
    else:
        print("⚠️ Some tests failed. Check the errors above.")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_deployment.py <railway-url>")
        print("Example: python test_deployment.py https://your-app.railway.app")
        sys.exit(1)
    
    base_url = sys.argv[1].rstrip('/')
    success = test_deployment(base_url)
    sys.exit(0 if success else 1)
