import sqlite3

# إنشاء الاتصال بملف قاعدة البيانات
conn = sqlite3.connect("database/yc2.db")
cursor = conn.cursor()

# إنشاء جدول الأعضاء
cursor.execute("""
CREATE TABLE IF NOT EXISTS members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    phone TEXT,
    email TEXT,
    status TEXT DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# إنشاء جدول طلبات العضوية
cursor.execute("""
CREATE TABLE IF NOT EXISTS membership_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    phone TEXT,
    email TEXT,
    reason TEXT,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# إنشاء جدول الفعاليات
cursor.execute("""
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    place TEXT,
    date TEXT,
    image TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()
print("تم إنشاء قاعدة البيانات والجداول بنجاح!")
