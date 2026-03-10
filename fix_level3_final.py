#!/usr/bin/env python3
"""Final fix for Level 3 challenges - Replace fragment code"""

import re

# Read the file
with open('backend/app/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Define the pattern to find Level 3 Python challenge
old_python = r'"title": "Reversing Array - Python",\s*"description": "Implement a function to reverse an array in-place\. Arrange the code fragments in the correct order\.",\s*"language": "python",\s*"level": 3,\s*"fragments": \[\s*"def is_valid\(s\):\\n    stack = \[\]\\n    pairs = \{\'\\(\': \'\\)\', \'\{\':\s*\'\}\', \'\[\':\s*\'\]\'\}",\s*"    for char in s:\\n        if char in pairs:",\s*"            stack\.append\(char\)\\n        elif char in pairs\.values\(\):",\s*"            if not stack or pairs\[stack\.pop\(\)\] != char:\\n                return False\\n    return len\(stack\) == 0"\s*\]'

new_python = '''"title": "Reversing Array - Python",
                    "description": "Implement a function to reverse an array in-place. Arrange the code fragments in the correct order.",
                    "language": "python",
                    "level": 3,
                    "fragments": [
                        "def reverse_array(arr):\\n    left = 0\\n    right = len(arr) - 1",
                        "    while left < right:",
                        "        arr[left], arr[right] = arr[right], arr[left]",
                        "        left += 1\\n        right -= 1",
                        "    return arr"
                    ]'''

# Replace Python
content = re.sub(old_python, new_python, content, flags=re.DOTALL)

# Define the pattern to find Level 3 C challenge
old_c = r'"title": "Reversing Array - C",\s*"description": "Implement a function to reverse an array in-place\. Arrange the code fragments in the correct order\.",\s*"language": "c",\s*"level": 3,\s*"fragments": \[\s*"bool isValid\(char\* s\) \{\\n    char stack\[10000\];\\n    int top = -1;",\s*"    for\(int i = 0; s\[i\]; i\+\+\) \{\\n        if\(s\[i\] == \'\\\(\' \|\| s\[i\] == \'\\\{\' \|\| s\[i\] == \'\\\[\'\) \{",\s*"            stack\[\+\+top\] = s\[i\];\\n        \} else \{",\s*"            if\(top == -1\) return false;\\n            char open = stack\[top--\];\\n            if\(\(s\[i\] == \'\\\)\' && open != \'\\\(\'\) \|\| \(s\[i\] == \'\\\}\' && open != \'\\\{\'\) \|\| \(s\[i\] == \'\\\]\' && open != \'\\\[\'\)\) return false;\\n        \}\\n    \}\\n    return top == -1;\\n\}"\s*\]'

new_c = '''"title": "Reversing Array - C",
                    "description": "Implement a function to reverse an array in-place. Arrange the code fragments in the correct order.",
                    "language": "c",
                    "level": 3,
                    "fragments": [
                        "void reverse_array(int arr[], int n) {\\n    int left = 0, right = n - 1;",
                        "    while(left < right) {",
                        "        int temp = arr[left];",
                        "        arr[left] = arr[right];\\n        arr[right] = temp;",
                        "        left++;\\n        right--;\\n    }\\n}"
                    ]'''

# Replace C
content = re.sub(old_c, new_c, content, flags=re.DOTALL)

# Define the pattern to find Level 3 Java challenge
old_java = r'"title": "Reversing Array - Java",\s*"description": "Implement a function to reverse an array in-place\. Arrange the code fragments in the correct order\.",\s*"language": "java",\s*"level": 3,\s*"fragments": \[\s*"public static boolean isValid\(String s\) \{\\n    Stack<Character> stack = new Stack<>\(\);\\n    Map<Character, Character> pairs = Map\.of\(\'\\\(\', \'\\\)\', \'\\\{\',\s*\'\\\}\', \'\\\[\',\s*\'\\\]\'\);",\s*"    for \(char c : s\.toCharArray\(\)\) \{\\n        if \(pairs\.containsKey\(c\)\) \{",\s*"            stack\.push\(c\);\\n        \} else if \(pairs\.containsValue\(c\)\) \{",\s*"            if \(stack\.isEmpty\(\) \|\| pairs\.get\(stack\.pop\(\)\) != c\) return false;\\n        \}\\n    \}\\n    return stack\.isEmpty\(\);\\n\}"\s*\]'

new_java = '''"title": "Reversing Array - Java",
                    "description": "Implement a function to reverse an array in-place. Arrange the code fragments in the correct order.",
                    "language": "java",
                    "level": 3,
                    "fragments": [
                        "public static void reverseArray(int[] arr) {\\n    int left = 0, right = arr.length - 1;",
                        "    while(left < right) {",
                        "        int temp = arr[left];",
                        "        arr[left] = arr[right];\\n        arr[right] = temp;",
                        "        left++;\\n        right--;\\n    }\\n}"
                    ]'''

# Replace Java
content = re.sub(old_java, new_java, content, flags=re.DOTALL)

# Define the pattern to find Level 3 C++ challenge
old_cpp = r'"title": "Reversing Array - C\+\+",\s*"description": "Implement a function to reverse an array in-place\. Arrange the code fragments in the correct order\.",\s*"language": "cpp",\s*"level": 3,\s*"fragments": \[\s*"bool isValid\(string s\) \{\\n    stack<char> st;\\n    unordered_map<char, char> pairs = \{\{\'\\\(\',\s*\'\\\)\'\}, \{\'\\\{\',\s*\'\\\}\'\}, \{\'\\\[\',\s*\'\\\]\'\}\};",\s*"    for\(char c : s\) \{\\n        if\(pairs\.count\(c\)\) \{",\s*"            st\.push\(c\);\\n        \} else \{",\s*"            if\(st\.empty\(\) \|\| pairs\[st\.top\(\)\] != c\) return false;\\n            st\.pop\(\);\\n        \}\\n    \}\\n    return st\.empty\(\);\\n\}"\s*\]'

new_cpp = '''"title": "Reversing Array - C++",
                    "description": "Implement a function to reverse an array in-place. Arrange the code fragments in the correct order.",
                    "language": "cpp",
                    "level": 3,
                    "fragments": [
                        "void reverseArray(vector<int>& arr) {\\n    int left = 0, right = arr.size() - 1;",
                        "    while(left < right) {",
                        "        swap(arr[left], arr[right]);",
                        "        left++;\\n        right--;",
                        "    }\\n}"
                    ]'''

# Replace C++
content = re.sub(old_cpp, new_cpp, content, flags=re.DOTALL)

# Write the updated content
with open('backend/app/main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Successfully updated all Level 3 challenges!")
print("✅ Python: 5 fragments - reverse_array")
print("✅ C: 5 fragments - reverse_array")
print("✅ Java: 5 fragments - reverseArray")
print("✅ C++: 5 fragments - reverseArray")
