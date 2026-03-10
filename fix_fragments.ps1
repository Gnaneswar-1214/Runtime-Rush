# PowerShell script to fix Level 3 fragment code

$file = "backend/app/main.py"
$content = Get-Content $file -Raw

# Replace Python fragments
$content = $content -replace 'def is_valid\(s\):\\n    stack = \[\]\\n    pairs = \{''\\('': ''\\)'', ''\\{'': ''\\}'', ''\\\['': ''\\\]''\}', 'def reverse_array(arr):\n    left = 0\n    right = len(arr) - 1'
$content = $content -replace '    for char in s:\\n        if char in pairs:', '    while left < right:'
$content = $content -replace '            stack\.append\(char\)\\n        elif char in pairs\.values\(\):', '        arr[left], arr[right] = arr[right], arr[left]'
$content = $content -replace '            if not stack or pairs\[stack\.pop\(\)\] != char:\\n                return False\\n    return len\(stack\) == 0', '        left += 1\n        right -= 1",\n                        "    return arr'

# Replace C fragments  
$content = $content -replace 'bool isValid\(char\* s\) \{\\n    char stack\[10000\];\\n    int top = -1;', 'void reverse_array(int arr[], int n) {\n    int left = 0, right = n - 1;'
$content = $content -replace '    for\(int i = 0; s\[i\]; i\+\+\) \{\\n        if\(s\[i\] == ''\\('' \|\| s\[i\] == ''\\{'' \|\| s\[i\] == ''\\\['' \) \{', '    while(left < right) {'
$content = $content -replace '            stack\[\+\+top\] = s\[i\];\\n        \} else \{', '        int temp = arr[left];'
$content = $content -replace '            if\(top == -1\) return false;\\n            char open = stack\[top--\];\\n            if\(\(s\[i\] == ''\\)'' && open != ''\\(''\) \|\| \(s\[i\] == ''\\}'' && open != ''\\{''\) \|\| \(s\[i\] == ''\\\]'' && open != ''\\\[''\)\) return false;\\n        \}\\n    \}\\n    return top == -1;\\n\}', '        arr[left] = arr[right];\n        arr[right] = temp;",\n                        "        left++;\n        right--;\n    }\n}'

# Replace Java fragments
$content = $content -replace 'public static boolean isValid\(String s\) \{\\n    Stack<Character> stack = new Stack<>\(\);\\n    Map<Character, Character> pairs = Map\.of\(''\\('', ''\\)'', ''\\{'', ''\\}'', ''\\\['', ''\\\]''\);', 'public static void reverseArray(int[] arr) {\n    int left = 0, right = arr.length - 1;'
$content = $content -replace '    for \(char c : s\.toCharArray\(\)\) \{\\n        if \(pairs\.containsKey\(c\)\) \{', '    while(left < right) {'
$content = $content -replace '            stack\.push\(c\);\\n        \} else if \(pairs\.containsValue\(c\)\) \{', '        int temp = arr[left];'
$content = $content -replace '            if \(stack\.isEmpty\(\) \|\| pairs\.get\(stack\.pop\(\)\) != c\) return false;\\n        \}\\n    \}\\n    return stack\.isEmpty\(\);\\n\}', '        arr[left] = arr[right];\n        arr[right] = temp;",\n                        "        left++;\n        right--;\n    }\n}'

# Replace C++ fragments
$content = $content -replace 'bool isValid\(string s\) \{\\n    stack<char> st;\\n    unordered_map<char, char> pairs = \{\{''\\('', ''\\)''\}, \{''\\{'', ''\\}''\}, \{''\\\['', ''\\\]''\}\};', 'void reverseArray(vector<int>& arr) {\n    int left = 0, right = arr.size() - 1;'
$content = $content -replace '    for\(char c : s\) \{\\n        if\(pairs\.count\(c\)\) \{', '    while(left < right) {'
$content = $content -replace '            st\.push\(c\);\\n        \} else \{', '        swap(arr[left], arr[right]);'
$content = $content -replace '            if\(st\.empty\(\) \|\| pairs\[st\.top\(\)\] != c\) return false;\\n            st\.pop\(\);\\n        \}\\n    \}\\n    return st\.empty\(\);\\n\}', '        left++;\n        right--;",\n                        "    }\n}'

# Save
$content | Set-Content $file -NoNewline

Write-Host "✅ Level 3 fragments updated!"
