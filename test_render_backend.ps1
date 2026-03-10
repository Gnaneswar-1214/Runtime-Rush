# Test Render Backend
$BASE_URL = "https://runtime-rush-backend2.onrender.com"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "🚀 TESTING RENDER BACKEND" -ForegroundColor Cyan
Write-Host "   URL: $BASE_URL" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

$results = @{}

# Test 1: Health Check
Write-Host "`n🔍 Testing Health Check..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$BASE_URL/health" -Method Get -TimeoutSec 10
    Write-Host "   Status: SUCCESS" -ForegroundColor Green
    Write-Host "   Response: $($response | ConvertTo-Json -Compress)" -ForegroundColor White
    $results['health'] = $true
} catch {
    Write-Host "   ❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    $results['health'] = $false
}

# Test 2: Challenges
Write-Host "`n🔍 Testing Challenges Endpoint..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$BASE_URL/api/challenges" -Method Get -TimeoutSec 10
    Write-Host "   Status: SUCCESS" -ForegroundColor Green
    Write-Host "   Total Challenges: $($response.Count)" -ForegroundColor White
    
    if ($response.Count -gt 0) {
        Write-Host "   Sample Challenge: $($response[0].title)" -ForegroundColor White
        
        # Count by level
        $level1 = ($response | Where-Object { $_.level -eq 1 }).Count
        $level2 = ($response | Where-Object { $_.level -eq 2 }).Count
        $level3 = ($response | Where-Object { $_.level -eq 3 }).Count
        Write-Host "   Level 1: $level1 challenges" -ForegroundColor White
        Write-Host "   Level 2: $level2 challenges" -ForegroundColor White
        Write-Host "   Level 3: $level3 challenges" -ForegroundColor White
        
        # Count by language
        $languages = $response | Group-Object -Property language | Select-Object Name, Count
        Write-Host "   Languages:" -ForegroundColor White
        foreach ($lang in $languages) {
            Write-Host "      - $($lang.Name): $($lang.Count)" -ForegroundColor White
        }
    }
    
    $results['challenges'] = ($response.Count -gt 0)
} catch {
    Write-Host "   ❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    $results['challenges'] = $false
}

# Test 3: Admin Login
Write-Host "`n🔍 Testing Admin Login..." -ForegroundColor Yellow
try {
    $body = @{
        username = "mouniadmin"
        password = "1214@"
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod -Uri "$BASE_URL/api/auth/login" -Method Post -Body $body -ContentType "application/json" -TimeoutSec 10
    Write-Host "   Status: SUCCESS" -ForegroundColor Green
    Write-Host "   Admin ID: $($response.id)" -ForegroundColor White
    Write-Host "   Username: $($response.username)" -ForegroundColor White
    Write-Host "   Role: $($response.role)" -ForegroundColor White
    $adminId = $response.id
    $results['admin_login'] = $true
} catch {
    Write-Host "   ❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    $results['admin_login'] = $false
    $adminId = $null
}

# Test 4: Admin Stats
if ($adminId) {
    Write-Host "`n🔍 Testing Admin Stats..." -ForegroundColor Yellow
    try {
        $response = Invoke-RestMethod -Uri "$BASE_URL/api/admin/stats?admin_id=$adminId" -Method Get -TimeoutSec 10
        Write-Host "   Status: SUCCESS" -ForegroundColor Green
        Write-Host "   Total Users: $($response.total_users)" -ForegroundColor White
        Write-Host "   Total Challenges: $($response.total_challenges)" -ForegroundColor White
        Write-Host "   Challenges by Level: $($response.challenges_by_level | ConvertTo-Json -Compress)" -ForegroundColor White
        $results['admin_stats'] = $true
    } catch {
        Write-Host "   ❌ Error: $($_.Exception.Message)" -ForegroundColor Red
        $results['admin_stats'] = $false
    }
}
else {
    $results['admin_stats'] = $false
}

# Test 5: Leaderboard
Write-Host "`n🔍 Testing Leaderboard..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$BASE_URL/api/auth/leaderboard" -Method Get -TimeoutSec 10
    Write-Host "   Status: SUCCESS" -ForegroundColor Green
    Write-Host "   Total Users on Leaderboard: $($response.Count)" -ForegroundColor White
    $results['leaderboard'] = $true
} catch {
    Write-Host "   ❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    $results['leaderboard'] = $false
}

# Summary
Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "📊 TEST SUMMARY" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

foreach ($test in $results.GetEnumerator()) {
    $status = if ($test.Value) { "✅ PASSED" } else { "❌ FAILED" }
    $color = if ($test.Value) { "Green" } else { "Red" }
    Write-Host "   $($test.Key.ToUpper()): $status" -ForegroundColor $color
}

$totalTests = $results.Count
$passedTests = ($results.Values | Where-Object { $_ -eq $true }).Count

Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "   TOTAL: $passedTests/$totalTests tests passed" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

if ($passedTests -eq $totalTests) {
    Write-Host "`n🎉 ALL TESTS PASSED! Backend is working perfectly!" -ForegroundColor Green
}
else {
    Write-Host "`n⚠️ $($totalTests - $passedTests) test(s) failed. Check the errors above." -ForegroundColor Yellow
}
