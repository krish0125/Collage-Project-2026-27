"""
setup_mongodb.py
----------------
KisanCare – MongoDB Database Setup Script
==========================================
Run this ONCE after MongoDB is installed:
    python setup_mongodb.py

What it does:
  1. Connects to MongoDB at localhost:27017
  2. Creates 'kisancare_db' database
  3. Creates ALL required collections with proper indexes
  4. Seeds the demo user (demo@gmail.com / Demo@1234)
  5. Verifies authentication works (signup + login flow)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime

try:
    from pymongo import MongoClient, ASCENDING, DESCENDING
    from pymongo.errors import CollectionInvalid, DuplicateKeyError, ServerSelectionTimeoutError
except ImportError:
    print("[ERROR] pymongo not installed. Run: pip install pymongo")
    sys.exit(1)

try:
    from werkzeug.security import generate_password_hash, check_password_hash
except ImportError:
    print("[ERROR] werkzeug not installed. Run: pip install werkzeug")
    sys.exit(1)

# ── Config ────────────────────────────────────────────────────────────────────
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME   = "kisancare_db"

# ── Connect ───────────────────────────────────────────────────────────────────
print("=" * 60)
print("  KisanCare -- MongoDB Database Setup")
print("=" * 60)

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    print(f"[OK] Connected to MongoDB at {MONGO_URI}")
except ServerSelectionTimeoutError as e:
    print(f"[ERROR] Cannot connect to MongoDB: {e}")
    print()
    print("  Make sure MongoDB is running:")
    print("  1. Open Services (Win+R -> services.msc)")
    print("  2. Find 'MongoDB' or 'MongoDB Server' service")
    print("  3. Right-click -> Start")
    print("  OR run:  net start MongoDB")
    sys.exit(1)

db = client[DB_NAME]
print(f"[OK] Using database: '{DB_NAME}'")


# ── Helper: safe collection creation ─────────────────────────────────────────
def ensure_collection(db, name):
    try:
        db.create_collection(name)
        print(f"  [+] Created collection: {name}")
    except CollectionInvalid:
        print(f"  [=] Collection already exists: {name}")
    return db[name]


# 1. USERS / LOGIN COLLECTION
print("\n[1/8] Setting up 'login' (users) collection...")
login_col = ensure_collection(db, "login")
login_col.create_index([("email", ASCENDING)], unique=True, name="email_unique")
print("  [+] Created unique index on email")

# 2. LOGIN HISTORY
print("\n[2/8] Setting up 'login_history' collection...")
history_col = ensure_collection(db, "login_history")
history_col.create_index([("email", ASCENDING)])
history_col.create_index([("timestamp", DESCENDING)])

# 3. PROFILES
print("\n[3/8] Setting up 'profiles' collection...")
profiles_col = ensure_collection(db, "profiles")
profiles_col.create_index([("email", ASCENDING)], unique=True, name="profile_email_unique")

# 4. CROP HISTORY
print("\n[4/8] Setting up 'crop_history' collection...")
crop_history_col = ensure_collection(db, "crop_history")
crop_history_col.create_index([("user_email", ASCENDING)])
crop_history_col.create_index([("created_at", DESCENDING)])

# 5. EXPENSES
print("\n[5/8] Setting up 'expenses' collection...")
expenses_col = ensure_collection(db, "expenses")
expenses_col.create_index([("user_email", ASCENDING)])
expenses_col.create_index([("date", DESCENDING)])

# 6. FEEDBACK
print("\n[6/8] Setting up 'feedback' collection...")
ensure_collection(db, "feedback")

# 7. MARKET DATA
print("\n[7/8] Setting up 'market_data' collection...")
market_col = ensure_collection(db, "market_data")
market_col.create_index([("commodity", ASCENDING)])
market_col.create_index([("date", DESCENDING)])

# 8. NOTIFICATION LOGS
print("\n[8/8] Setting up 'notification_logs' collection...")
ensure_collection(db, "notification_logs")


# SEED: Demo User
print("\n[SEED] Seeding users...")
demo_email = "demo@gmail.com"
demo_password = "Demo@1234"

existing = login_col.find_one({"email": demo_email})
if existing:
    print(f"  [=] Demo user already exists: {demo_email}")
else:
    try:
        login_col.insert_one({
            "name": "Demo User",
            "email": demo_email,
            "password": generate_password_hash(demo_password),
            "phone": "9876543210",
            "role": "farmer",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        print(f"  [+] Demo user created: {demo_email} / {demo_password}")
    except DuplicateKeyError:
        print(f"  [=] Demo user already exists: {demo_email}")

admin_email = "admin@kisancare.com"
existing_admin = login_col.find_one({"email": admin_email})
if not existing_admin:
    try:
        login_col.insert_one({
            "name": "KisanCare Admin",
            "email": admin_email,
            "password": generate_password_hash("Admin@1234"),
            "phone": "9999999999",
            "role": "admin",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        print(f"  [+] Admin user created: {admin_email} / Admin@1234")
    except DuplicateKeyError:
        print(f"  [=] Admin already exists: {admin_email}")
else:
    print(f"  [=] Admin user already exists: {admin_email}")


# VERIFY: Test auth flow
print("\n[VERIFY] Testing authentication flow...")
user = login_col.find_one({"email": demo_email})
if user:
    print(f"  [OK] Found user: {user['email']} (role: {user.get('role', 'N/A')})")
    if check_password_hash(user["password"], demo_password):
        print(f"  [OK] Password verification: PASSED")
    else:
        print(f"  [FAIL] Password verification: FAILED")
    if not check_password_hash(user["password"], "wrongpassword"):
        print(f"  [OK] Wrong password rejection: PASSED")
else:
    print(f"  [FAIL] Demo user not found in database!")

indexes = list(login_col.list_indexes())
email_index_exists = any(idx.get("name") == "email_unique" for idx in indexes)
print(f"  [{'OK' if email_index_exists else 'FAIL'}] Unique email index: {'EXISTS' if email_index_exists else 'MISSING'}")


# SUMMARY
print("\n" + "=" * 60)
print("  Database Setup Complete!")
print("=" * 60)
print(f"  Database:    {DB_NAME}")
print(f"  Collections: {', '.join(db.list_collection_names())}")
print(f"  Total Users: {login_col.count_documents({})}")
print()
print("  Demo Credentials:")
print("  Email:    demo@gmail.com")
print("  Password: Demo@1234")
print()
print("  Admin Credentials:")
print("  Email:    admin@kisancare.com")
print("  Password: Admin@1234")
print("=" * 60)
print("  Next step: python run.py")
print("=" * 60)
