# ⚠️ Level 3 Challenges - Manual Fix Required

## Current Status
- ✅ Titles updated to "Reversing Array"
- ✅ Descriptions updated
- ❌ **Fragment code still contains old "Valid Parenthesis" logic**

## What Needs to Be Done

You need to manually edit `backend/app/main.py` in **TWO** locations:

### Location 1: Line ~156 (in `auto_initialize_database` function)
### Location 2: Line ~409 (in `initialize_database` endpoint)

## Exact Replacements Needed

### Python (5 fragments):
**FIND:**
```python
"fragments": [
    "def is_valid(s):\n    stack = []\n    pairs = {'(': ')', '{': '}', '[': ']'}",
    "    for char in s:\n        if char in pairs:",
    "            stack.append(char)\n        elif char in pairs.values():",
    "            if not stack or pairs[stack.pop()] != char:\n                return False\n    return len(stack) == 0"
]
```

**REPLACE WITH:**
```python
"fragments": [
    "def reverse_array(arr):\n    left = 0\n    right = len(arr) - 1",
    "    while left < right:",
    "        arr[left], arr[right] = arr[right], arr[left]",
    "        left += 1\n        right -= 1",
    "    return arr"
]
```

### C (5 fragments):
**FIND:**
```python
"fragments": [
    "bool isValid(char* s) {\n    char stack[10000];\n    int top = -1;",
    "    for(int i = 0; s[i]; i++) {\n        if(s[i] == '(' || s[i] == '{' || s[i] == '[') {",
    "            stack[++top] = s[i];\n        } else {",
    "            if(top == -1) return false;\n            char open = stack[top--];\n            if((s[i] == ')' && open != '(') || (s[i] == '}' && open != '{') || (s[i] == ']' && open != '[')) return false;\n        }\n    }\n    return top == -1;\n}"
]
```

**REPLACE WITH:**
```python
"fragments": [
    "void reverse_array(int arr[], int n) {\n    int left = 0, right = n - 1;",
    "    while(left < right) {",
    "        int temp = arr[left];",
    "        arr[left] = arr[right];\n        arr[right] = temp;",
    "        left++;\n        right--;\n    }\n}"
]
```

### Java (5 fragments):
**FIND:**
```python
"fragments": [
    "public static boolean isValid(String s) {\n    Stack<Character> stack = new Stack<>();\n    Map<Character, Character> pairs = Map.of('(', ')', '{', '}', '[', ']');",
    "    for (char c : s.toCharArray()) {\n        if (pairs.containsKey(c)) {",
    "            stack.push(c);\n        } else if (pairs.containsValue(c)) {",
    "            if (stack.isEmpty() || pairs.get(stack.pop()) != c) return false;\n        }\n    }\n    return stack.isEmpty();\n}"
]
```

**REPLACE WITH:**
```python
"fragments": [
    "public static void reverseArray(int[] arr) {\n    int left = 0, right = arr.length - 1;",
    "    while(left < right) {",
    "        int temp = arr[left];",
    "        arr[left] = arr[right];\n        arr[right] = temp;",
    "        left++;\n        right--;\n    }\n}"
]
```

### C++ (5 fragments):
**FIND:**
```python
"fragments": [
    "bool isValid(string s) {\n    stack<char> st;\n    unordered_map<char, char> pairs = {{'(', ')'}, {'{', '}'}, {'[', ']'}};",
    "    for(char c : s) {\n        if(pairs.count(c)) {",
    "            st.push(c);\n        } else {",
            "            if(st.empty() || pairs[st.top()] != c) return false;\n            st.pop();\n        }\n    }\n    return st.empty();\n}"
]
```

**REPLACE WITH:**
```python
"fragments": [
    "void reverseArray(vector<int>& arr) {\n    int left = 0, right = arr.size() - 1;",
    "    while(left < right) {",
    "        swap(arr[left], arr[right]);",
    "        left++;\n        right--;",
    "    }\n}"
]
```

## Quick Steps:
1. Open `backend/app/main.py` in your editor
2. Search for `def is_valid(s):` - you'll find 2 occurrences
3. For each occurrence, replace all 4 languages (Python, C, Java, C++) with the code above
4. Save the file
5. Commit and push

## After Manual Fix:
```bash
git add backend/app/main.py
git commit -m "Complete Level 3 challenge update - all fragments fixed"
git push
```

Then Railway will redeploy with the correct challenges!
