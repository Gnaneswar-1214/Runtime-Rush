#!/usr/bin/env python3
"""Final complete fix for Level 3 challenges"""

# Read the file
with open('backend/app/main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# New Level 3 challenges data
level3_python = '''                {
                    "title": "Reversing Array - Python",
                    "description": "Implement a function to reverse an array in-place. Arrange the code fragments in the correct order.",
                    "language": "python",
                    "level": 3,
                    "fragments": [
                        "def reverse_array(arr):\\n    left = 0\\n    right = len(arr) - 1",
                        "    while left < right:",
                        "        arr[left], arr[right] = arr[right], arr[left]",
                        "        left += 1\\n        right -= 1",
                        "    return arr"
                    ]
                },
'''

level3_c = '''                {
                    "title": "Reversing Array - C",
                    "description": "Implement a function to reverse an array in-place. Arrange the code fragments in the correct order.",
                    "language": "c",
                    "level": 3,
                    "fragments": [
                        "void reverse_array(int arr[], int n) {\\n    int left = 0, right = n - 1;",
                        "    while(left < right) {",
                        "        int temp = arr[left];",
                        "        arr[left] = arr[right];\\n        arr[right] = temp;",
                        "        left++;\\n        right--;\\n    }\\n}"
                    ]
                },
'''

level3_java = '''                {
                    "title": "Reversing Array - Java",
                    "description": "Implement a function to reverse an array in-place. Arrange the code fragments in the correct order.",
                    "language": "java",
                    "level": 3,
                    "fragments": [
                        "public static void reverseArray(int[] arr) {\\n    int left = 0, right = arr.length - 1;",
                        "    while(left < right) {",
                        "        int temp = arr[left];",
                        "        arr[left] = arr[right];\\n        arr[right] = temp;",
                        "        left++;\\n        right--;\\n    }\\n}"
                    ]
                },
'''

level3_cpp = '''                {
                    "title": "Reversing Array - C++",
                    "description": "Implement a function to reverse an array in-place. Arrange the code fragments in the correct order.",
                    "language": "cpp",
                    "level": 3,
                    "fragments": [
                        "void reverseArray(vector<int>& arr) {\\n    int left = 0, right = arr.size() - 1;",
                        "    while(left < right) {",
                        "        swap(arr[left], arr[right]);",
                        "        left++;\\n        right--;",
                        "    }\\n}"
                    ]
                }
'''

# Find and replace Level 3 sections
output = []
i = 0
replacements_made = 0

while i < len(lines):
    line = lines[i]
    
    # Check if this is the start of Level 3 section
    if '# Level 3:' in line and 'Reversing Array' in line:
        print(f"Found Level 3 section at line {i+1}")
        output.append(line)  # Keep the comment
        i += 1
        
        # Skip until we find the opening brace of Python challenge
        while i < len(lines) and '"title": "Reversing Array - Python"' not in lines[i]:
            i += 1
        
        if i < len(lines):
            # Found Python challenge start, now skip all 4 languages
            depth = 0
            lang_count = 0
            start_i = i
            
            # Count braces to find where all 4 languages end
            while i < len(lines) and lang_count < 4:
                if '{' in lines[i]:
                    depth += lines[i].count('{')
                if '}' in lines[i]:
                    depth -= lines[i].count('}')
                    if depth == 0:
                        lang_count += 1
                        if lang_count < 4:
                            i += 1  # Move past the closing brace
                            # Skip comma and whitespace
                            while i < len(lines) and lines[i].strip() in [',', '']:
                                i += 1
                        else:
                            break
                i += 1
            
            # Now insert the new Level 3 challenges
            output.append(level3_python)
            output.append(level3_c)
            output.append(level3_java)
            output.append(level3_cpp)
            
            replacements_made += 1
            print(f"Replaced Level 3 section #{replacements_made}")
            continue
    
    output.append(line)
    i += 1

# Write the fixed content
with open('backend/app/main.py', 'w', encoding='utf-8') as f:
    f.writelines(output)

print(f"\n✅ Successfully replaced {replacements_made} Level 3 sections!")
print("✅ All 4 languages updated with 5 fragments each")
print("✅ Python: reverse_array")
print("✅ C: reverse_array")
print("✅ Java: reverseArray")
print("✅ C++: reverseArray")
