# PowerShell script to update Level 3 challenges

$filePath = "backend/app/main.py"
$content = Get-Content $filePath -Raw

# Replace comment
$content = $content -replace '# Level 3: Valid Parenthesis - 4 languages', '# Level 3: Reversing Array - 4 languages (5 fragments each)'

# Replace titles
$content = $content -replace '"title": "Valid Parenthesis - Python"', '"title": "Reversing Array - Python"'
$content = $content -replace '"title": "Valid Parenthesis - C"', '"title": "Reversing Array - C"'
$content = $content -replace '"title": "Valid Parenthesis - Java"', '"title": "Reversing Array - Java"'
$content = $content -replace '"title": "Valid Parenthesis - C\+\+"', '"title": "Reversing Array - C++"'

# Replace descriptions
$content = $content -replace 'Check if parentheses in a string are balanced\.', 'Implement a function to reverse an array in-place.'

# Save
$content | Set-Content $filePath -NoNewline

Write-Host "✅ Updated titles, comments, and descriptions"
Write-Host "⚠️ Note: Fragment code needs manual update - too complex for regex"
