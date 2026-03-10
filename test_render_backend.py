import requests
import json

# Render backend URL
BASE_URL = "https://runtime-rush-backend2.onrender.com"

def test_health():
    """Test health check endpoint"""
    print("\n🔍 Testing Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_challenges():
    """Test challenges endpoint"""
    print("\n🔍 Testing Challenges Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/challenges", timeout=10)
        print(f"   Status: {response.status_code}")
        data = response.json()
        print(f"   Total Challenges: {len(data)}")
        
        if len(data) > 0:
            print(f"   Sample Challenge: {data[0]['title']}")
            
            # Count by level
            level1 = len([c for c in data if c.get('level') == 1])
            level2 = len([c for c in data if c.get('level') == 2])
            level3 = len([c for c in data if c.get('level') == 3])
            print(f"   Level 1: {level1} challenges")
            print(f"   Level 2: {level2} challenges")
            print(f"   Level 3: {level3} challenges")
            
            # Count by language
            languages = {}
            for c in data:
                lang = c.get('language', 'unknown')
                languages[lang] = languages.get(lang, 0) + 1
            print(f"   Languages: {languages}")
        
        return response.status_code == 200 and len(data) > 0
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_admin_login():
    """Test admin login"""
    print("\n🔍 Testing Admin Login...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={"username": "mouniadmin", "password": "1214@"},
            timeout=10
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Admin ID: {data.get('id')}")
            print(f"   Username: {data.get('username')}")
            print(f"   Role: {data.get('role')}")
            return True, data.get('id')
        else:
            print(f"   Response: {response.text}")
            return False, None
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False, None

def test_admin_stats(admin_id):
    """Test admin stats endpoint"""
    print("\n🔍 Testing Admin Stats...")
    try:
        response = requests.get(
            f"{BASE_URL}/api/admin/stats?admin_id={admin_id}",
            timeout=10
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Total Users: {data.get('total_users')}")
            print(f"   Total Challenges: {data.get('total_challenges')}")
            print(f"   Challenges by Level: {data.get('challenges_by_level')}")
            return True
        else:
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_leaderboard():
    """Test leaderboard endpoint"""
    print("\n🔍 Testing Leaderboard...")
    try:
        response = requests.get(f"{BASE_URL}/api/auth/leaderboard", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Total Users on Leaderboard: {len(data)}")
            return True
        else:
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    print("=" * 60)
    print("🚀 TESTING RENDER BACKEND")
    print(f"   URL: {BASE_URL}")
    print("=" * 60)
    
    results = {}
    
    # Test 1: Health Check
    results['health'] = test_health()
    
    # Test 2: Challenges
    results['challenges'] = test_challenges()
    
    # Test 3: Admin Login
    login_success, admin_id = test_admin_login()
    results['admin_login'] = login_success
    
    # Test 4: Admin Stats (if login succeeded)
    if login_success and admin_id:
        results['admin_stats'] = test_admin_stats(admin_id)
    else:
        results['admin_stats'] = False
    
    # Test 5: Leaderboard
    results['leaderboard'] = test_leaderboard()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"   {test_name.upper()}: {status}")
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    
    print("\n" + "=" * 60)
    print(f"   TOTAL: {passed_tests}/{total_tests} tests passed")
    print("=" * 60)
    
    if passed_tests == total_tests:
        print("\n🎉 ALL TESTS PASSED! Backend is working perfectly!")
    else:
        print(f"\n⚠️ {total_tests - passed_tests} test(s) failed. Check the errors above.")

if __name__ == "__main__":
    main()
