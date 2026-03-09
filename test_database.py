"""
Quick script to check database contents
Run this to verify database has data
"""
import sqlite3
import os

db_path = "backend/runtime_rush.db"

if not os.path.exists(db_path):
    print(f"❌ Database not found at {db_path}")
    exit(1)

print(f"✅ Database found at {db_path}")
print("\n" + "="*50)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check users
cursor.execute("SELECT COUNT(*) FROM users")
user_count = cursor.fetchone()[0]
print(f"👥 Users: {user_count}")

cursor.execute("SELECT username, email, role FROM users")
users = cursor.fetchall()
for username, email, role in users:
    print(f"   - {username} ({email}) - {role}")

# Check challenges
cursor.execute("SELECT COUNT(*) FROM challenges")
challenge_count = cursor.fetchone()[0]
print(f"\n🎯 Challenges: {challenge_count}")

cursor.execute("SELECT title, language, level FROM challenges ORDER BY level, language")
challenges = cursor.fetchall()
for title, language, level in challenges:
    print(f"   - Level {level}: {title} ({language})")

# Check fragments
cursor.execute("SELECT COUNT(*) FROM code_fragments")
fragment_count = cursor.fetchone()[0]
print(f"\n📦 Code Fragments: {fragment_count}")

conn.close()

print("\n" + "="*50)
print("\n✅ Database check complete!")
print("\nNext steps:")
print("1. Start backend: cd backend && uvicorn app.main:app --reload")
print("2. Start frontend: cd frontend && npm start")
print("3. Visit: http://localhost:8000/initialize-db (if needed)")
print("4. Login as admin: mouniadmin / 1214@")
