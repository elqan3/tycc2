from flask import Flask, render_template, request, redirect, jsonify
import sqlite3
import os

app = Flask(__name__)

# --- إعدادات ---
DB_PATH = "database/yc2.db"
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------- الصفحة الرئيسية ----------
@app.route('/')
def index():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events ORDER BY date DESC")
    events = cursor.fetchall()
    conn.close()
    return render_template("index.html", events=events)

# ---------- لوحة الأدمن ----------
@app.route("/admin")
def admin_dashboard():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members")
    members = cursor.fetchall()
    cursor.execute("SELECT * FROM membership_requests")
    requests = cursor.fetchall()
    cursor.execute("SELECT * FROM events ORDER BY date DESC")
    events = cursor.fetchall()
    conn.close()
    return render_template("admin.html", members=members, requests=requests, events=events)

# ---------- صفحة النشر ----------
@app.route("/templates/post.html")
def post_page():
    return render_template("post.html")

# ---------- إضافة فعالية أو خبر ----------
@app.route("/add_event", methods=["POST"])
def add_event():
    title = request.form.get("title")
    description = request.form.get("description")
    place = request.form.get("place")
    date = request.form.get("date")

    image_file = request.files.get("image")
    image_path = None
    if image_file:
        filename = image_file.filename
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        image_file.save(save_path)
        image_path = f"uploads/{filename}"  # مسار نسبي للويب

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO events (title, description, place, date, image) VALUES (?,?,?,?,?)",
        (title, description, place, date, image_path)
    )
    conn.commit()
    conn.close()
    return redirect("/")  # العودة للصفحة الرئيسية بعد الإضافة

# ---------- نموذج طلب العضوية ----------
@app.route("/membership", methods=["GET", "POST"])
def membership():
    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
        phone = request.form.get("phone")
        email = request.form.get("email")
        reason = request.form.get("reason")

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO membership_requests (name, age, phone, email, reason) VALUES (?,?,?,?,?)",
            (name, age, phone, email, reason)
        )
        conn.commit()
        conn.close()
        return "<h3>تم إرسال طلبك بنجاح! سيتم مراجعته من قبل الإدارة.</h3><a href='/'>العودة للصفحة الرئيسية</a>"

    return render_template("membership.html")

# ---------- الموافقة على طلب عضوية ----------
@app.route("/approve_request/<int:request_id>", methods=["POST"])
def approve_request(request_id):
    data = request.get_json()
    role = data.get("role")
    serial_number = data.get("serial_number")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, age, phone, email FROM membership_requests WHERE id=?", (request_id,))
    req = cursor.fetchone()
    if req:
        name, age, phone, email = req
        cursor.execute(
            "INSERT INTO members (name, age, phone, email, role, serial_number) VALUES (?,?,?,?,?,?)",
            (name, age, phone, email, role, serial_number)
        )
        cursor.execute("DELETE FROM membership_requests WHERE id=?", (request_id,))
        conn.commit()
    conn.close()
    return jsonify({"status": "success"})

# ---------- رفض طلب العضوية ----------
@app.route("/reject_request/<int:request_id>")
def reject_request(request_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM membership_requests WHERE id=?", (request_id,))
    conn.commit()
    conn.close()
    return redirect("/admin")

# ---------- تحديث بيانات عضو ----------
@app.route("/update_member/<int:member_id>", methods=["POST"])
def update_member(member_id):
    data = request.get_json()
    name = data.get("name")
    age = data.get("age")
    phone = data.get("phone")
    email = data.get("email")
    role = data.get("role")
    serial_number = data.get("serial_number")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE members 
        SET name=?, age=?, phone=?, email=?, role=?, serial_number=?
        WHERE id=?
    """, (name, age, phone, email, role, serial_number, member_id))
    conn.commit()
    conn.close()
    return jsonify({"status":"success"})

if __name__ == "__main__":
    app.run(debug=True)
