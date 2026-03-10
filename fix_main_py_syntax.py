#!/usr/bin/env python3
"""Fix syntax errors in backend/app/main.py"""

# Read the file
with open('backend/app/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# The malformed lines that need to be removed (they appear twice)
malformed_lines = '''                        "        left++;\\n        right--;",\\n                        "    }\\n}"
                    ]
                }'''

# Remove all occurrences of the malformed lines
fixed_content = content.replace(malformed_lines, '')

# Write the fixed content back
with open('backend/app/main.py', 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print("✅ Fixed syntax errors in backend/app/main.py")
print("✅ Removed malformed duplicate lines")
