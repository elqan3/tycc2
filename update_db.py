import sqlite3

DB_PATH = "database/yc2.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# إضافة عمود role إذا لم يكن موجود
try:
    cursor.execute("ALTER TABLE members ADD COLUMN role TEXT DEFAULT 'عضو'")
except sqlite3.OperationalError:
    print("عمود role موجود بالفعل")

# إضافة عمود serial_number إذا لم يكن موجود
try:
    cursor.execute("ALTER TABLE members ADD COLUMN serial_number TEXT")
except sqlite3.OperationalError:
    print(" 111111 !!!!عمود serial_number موجود بالفعل")

conn.commit()
conn.close()
print(" 000000 ؟؟؟؟تم تعديل قاعدة البيانات بنجاح")
