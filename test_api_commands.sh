#!/bin/bash
# Quick API test commands for Railway deployment
# Replace YOUR_RAILWAY_URL with your actual Railway URL

RAILWAY_URL="https://your-app.railway.app"

echo "🧪 Testing Runtime Rush API on Railway"
echo "========================================"
echo ""

# Test 1: Health Check
echo "1️⃣ Health Check"
curl -X GET "$RAILWAY_URL/health"
echo -e "\n"

# Test 2: Initialize Database
echo "2️⃣ Initialize Database (creates admin + challenges)"
curl -X POST "$RAILWAY_URL/initialize-db"
echo -e "\n"

# Test 3: Get All Challenges
echo "3️⃣ Get All Challenges"
curl -X GET "$RAILWAY_URL/api/challenges"
echo -e "\n"

# Test 4: Admin Login
echo "4️⃣ Admin Login"
curl -X POST "$RAILWAY_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
echo -e "\n"

# Test 5: Register Test User
echo "5️⃣ Register Test User"
curl -X POST "$RAILWAY_URL/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"test123"}'
echo -e "\n"

echo "========================================"
echo "✅ Tests complete!"
echo ""
echo "If all tests passed, your deployment is working!"
echo "Admin credentials: admin / admin123"
