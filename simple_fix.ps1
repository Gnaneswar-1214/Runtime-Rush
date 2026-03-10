# Simple replacements for Level 3 fragments

$file = "backend/app/main.py"
$content = Get-Content $file -Raw

# Python - replace function signature
$content = $content -replace '"def is_valid\(s\):', '"def reverse_array(arr):'
$content = $content -replace 'stack = \[\]', 'left = 0'
$content = $content -replace 'pairs = \{', 'right = len(arr) - 1",\n                        "    while left < right:",\n                        "        arr[left], arr[right] = arr[right], arr[left]",\n                        "        left += 1\n        right -= 1",\n                        "    return arr'

# Save
$content | Set-Content $file -NoNewline

Write-Host "✅ Partial fix applied - manual editing still needed"
