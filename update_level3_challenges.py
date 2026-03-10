#!/usr/bin/env python3
"""Script to update Level 3 challenges from Valid Parenthesis to Reversing Array"""

# Read the file
with open('backend/app/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Define the old Level 3 challenges (Valid Parenthesis)
old_level3_python = '"title": "Valid Parenthesis - Python"'
old_level3_c = '"title": "Valid Parenthesis - C"'
old_level3_java = '"title": "Valid Parenthesis - Java"'
old_level3_cpp = '"title": "Valid Parenthesis - C++"'

# Define the new Level 3 challenges (Reversing Array)
new_level3_python = '"title": "Reversing Array - Python"'
new_level3_c = '"title": "Reversing Array - C"'
new_level3_java = '"title": "Reversing Array - Java"'
new_level3_cpp = '"title": "Reversing Array - C++"'

# Replace titles
content = content.replace(old_level3_python, new_level3_python)
content = content.replace(old_level3_c, new_level3_c)
content = content.replace(old_level3_java, new_level3_java)
content = content.replace(old_level3_cpp, new_level3_cpp)

# Replace descriptions
content = content.replace(
    '"description": "Check if parentheses in a string are balanced. Arrange the code fragments in the correct order."',
    '"description": "Implement a function to reverse an array in-place. Arrange the code fragments in the correct order."'
)

# Replace comment
content = content.replace(
    '# Level 3: Valid Parenthesis - 4 languages',
    '# Level 3: Reversing Array - 4 languages (5 fragments each)'
)

# Now replace the fragments for each language
# Python fragments
old_python_fragments = '''                    "fragments": [
                        "def is_valid(s):\\n    stack = []\\n    pairs = {'(': ')', '{': '}', '[': ']'}",
                        "    for char in s:\\n        if char in pairs:",
                        "            stack.append(char)\\n        elif char in pairs.values():",
                        "            if not stack or pairs[stack.pop()] != char:\\n                return False\\n    return len(stack) == 0"
                    ]'''

new_python_fragments = '''                    "fragments": [
                        "def reverse_array(arr):\\n    left = 0\\n    right = len(arr) - 1",
                        "    while left < right:",
                        "        arr[left], arr[right] = arr[right], arr[left]",
                        "        left += 1\\n        right -= 1",
                        "    return arr"
                    ]'''

content = content.replace(old_python_fragments, new_python_fragments)

# C fragments
old_c_fragments = '''                    "fragments": [
                        "bool isValid(char* s) {\\n    char stack[10000];\\n    int top = -1;",
                        "    for(int i = 0; s[i]; i++) {\\n        if(s[i] == '(' || s[i] == '{' || s[i] == '[') {",
                        "            stack[++top] = s[i];\\n        } else {",
                        "            if(top == -1) return false;\\n            char open = stack[top--];\\n            if((s[i] == ')' && open != '(') || (s[i] == '}' && open != '{') || (s[i] == ']' && open != '[')) return false;\\n        }\\n    }\\n    return top == -1;\\n}"
                    ]'''

new_c_fragments = '''                    "fragments": [
                        "void reverse_array(int arr[], int n) {\\n    int left = 0, right = n - 1;",
                        "    while(left < right) {",
                        "        int temp = arr[left];",
                        "        arr[left] = arr[right];\\n        arr[right] = temp;",
                        "        left++;\\n        right--;\\n    }\\n}"
                    ]'''

content = content.replace(old_c_fragments, new_c_fragments)

# Java fragments
old_java_fragments = '''                    "fragments": [
                        "public static boolean isValid(String s) {\\n    Stack<Character> stack = new Stack<>();\\n    Map<Character, Character> pairs = Map.of('(', ')', '{', '}', '[', ']');",
                        "    for (char c : s.toCharArray()) {\\n        if (pairs.containsKey(c)) {",
                        "            stack.push(c);\\n        } else if (pairs.containsValue(c)) {",
                        "            if (stack.isEmpty() || pairs.get(stack.pop()) != c) return false;\\n        }\\n    }\\n    return stack.isEmpty();\\n}"
                    ]'''

new_java_fragments = '''                    "fragments": [
                        "public static void reverseArray(int[] arr) {\\n    int left = 0, right = arr.length - 1;",
                        "    while(left < right) {",
                        "        int temp = arr[left];",
                        "        arr[left] = arr[right];\\n        arr[right] = temp;",
                        "        left++;\\n        right--;\\n    }\\n}"
                    ]'''

content = content.replace(old_java_fragments, new_java_fragments)

# C++ fragments
old_cpp_fragments = '''                    "fragments": [
                        "bool isValid(string s) {\\n    stack<char> st;\\n    unordered_map<char, char> pairs = {{'(', ')'}, {'{', '}'}, {'[', ']'}};",
                        "    for(char c : s) {\\n        if(pairs.count(c)) {",
                        "            st.push(c);\\n        } else {",
                        "            if(st.empty() || pairs[st.top()] != c) return false;\\n            st.pop();\\n        }\\n    }\\n    return st.empty();\\n}"
                    ]'''

new_cpp_fragments = '''                    "fragments": [
                        "void reverseArray(vector<int>& arr) {\\n    int left = 0, right = arr.size() - 1;",
                        "    while(left < right) {",
                        "        swap(arr[left], arr[right]);",
                        "        left++;\\n        right--;",
                        "    }\\n}"
                    ]'''

content = content.replace(old_cpp_fragments, new_cpp_fragments)

# Write the updated content
with open('backend/app/main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Successfully updated Level 3 challenges from Valid Parenthesis to Reversing Array!")
print("✅ All 4 languages updated with 5 fragments each")
