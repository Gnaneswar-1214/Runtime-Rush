import requests
import uuid
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:8000"

# Create admin user
print("Creating admin user...")
try:
    response = requests.post(
        f"{BASE_URL}/api/admin/create-admin",
        params={
            "username": "admin",
            "email": "admin@runtimerush.com",
            "password": "admin123"
        }
    )
    if response.status_code == 200:
        admin_data = response.json()
        print(f"✅ Admin created: {admin_data}")
    else:
        print(f"⚠️ Admin creation response: {response.json()}")
except Exception as e:
    print(f"❌ Error creating admin: {e}")

# Create sample challenges for each level
print("\nCreating sample challenges...")

challenges = [
    {
        "title": "Level 1: Hello World",
        "description": "Write a simple Hello World program",
        "language": "python",
        "level": 1,
        "correct_solution": "print('Hello, World!')",
        "start_time": datetime.now().isoformat(),
        "end_time": (datetime.now() + timedelta(days=7)).isoformat(),
        "created_by": str(uuid.uuid4())
    },
    {
        "title": "Level 1: Sum Two Numbers",
        "description": "Write a function that adds two numbers",
        "language": "python",
        "level": 1,
        "correct_solution": "def add(a, b):\n    return a + b",
        "start_time": datetime.now().isoformat(),
        "end_time": (datetime.now() + timedelta(days=7)).isoformat(),
        "created_by": str(uuid.uuid4())
    },
    {
        "title": "Level 2: Fibonacci Sequence",
        "description": "Generate the first n Fibonacci numbers",
        "language": "python",
        "level": 2,
        "correct_solution": "def fibonacci(n):\n    if n <= 0:\n        return []\n    elif n == 1:\n        return [0]\n    fib = [0, 1]\n    for i in range(2, n):\n        fib.append(fib[i-1] + fib[i-2])\n    return fib",
        "start_time": datetime.now().isoformat(),
        "end_time": (datetime.now() + timedelta(days=7)).isoformat(),
        "created_by": str(uuid.uuid4())
    },
    {
        "title": "Level 2: Palindrome Checker",
        "description": "Check if a string is a palindrome",
        "language": "python",
        "level": 2,
        "correct_solution": "def is_palindrome(s):\n    s = s.lower().replace(' ', '')\n    return s == s[::-1]",
        "start_time": datetime.now().isoformat(),
        "end_time": (datetime.now() + timedelta(days=7)).isoformat(),
        "created_by": str(uuid.uuid4())
    },
    {
        "title": "Level 3: Binary Search Tree",
        "description": "Implement a binary search tree with insert and search operations",
        "language": "python",
        "level": 3,
        "correct_solution": "class Node:\n    def __init__(self, value):\n        self.value = value\n        self.left = None\n        self.right = None\n\nclass BST:\n    def __init__(self):\n        self.root = None\n    \n    def insert(self, value):\n        if not self.root:\n            self.root = Node(value)\n        else:\n            self._insert_recursive(self.root, value)\n    \n    def _insert_recursive(self, node, value):\n        if value < node.value:\n            if node.left is None:\n                node.left = Node(value)\n            else:\n                self._insert_recursive(node.left, value)\n        else:\n            if node.right is None:\n                node.right = Node(value)\n            else:\n                self._insert_recursive(node.right, value)",
        "start_time": datetime.now().isoformat(),
        "end_time": (datetime.now() + timedelta(days=7)).isoformat(),
        "created_by": str(uuid.uuid4())
    },
    {
        "title": "Level 3: Graph Traversal",
        "description": "Implement BFS and DFS for graph traversal",
        "language": "python",
        "level": 3,
        "correct_solution": "from collections import deque\n\ndef bfs(graph, start):\n    visited = set()\n    queue = deque([start])\n    result = []\n    \n    while queue:\n        node = queue.popleft()\n        if node not in visited:\n            visited.add(node)\n            result.append(node)\n            queue.extend(graph[node])\n    \n    return result\n\ndef dfs(graph, start, visited=None):\n    if visited is None:\n        visited = set()\n    visited.add(start)\n    result = [start]\n    \n    for neighbor in graph[start]:\n        if neighbor not in visited:\n            result.extend(dfs(graph, neighbor, visited))\n    \n    return result",
        "start_time": datetime.now().isoformat(),
        "end_time": (datetime.now() + timedelta(days=7)).isoformat(),
        "created_by": str(uuid.uuid4())
    }
]

for challenge in challenges:
    try:
        response = requests.post(
            f"{BASE_URL}/api/challenges",
            json=challenge
        )
        if response.status_code == 200:
            print(f"✅ Created: {challenge['title']}")
        else:
            print(f"⚠️ Failed to create {challenge['title']}: {response.text}")
    except Exception as e:
        print(f"❌ Error creating {challenge['title']}: {e}")

print("\n✅ Setup complete!")
print("\nAdmin credentials:")
print("Username: admin")
print("Password: admin123")
print("\nYou can now:")
print("1. Login as admin to access the admin dashboard")
print("2. Register as a regular user to test the level progression")
