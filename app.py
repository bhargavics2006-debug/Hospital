from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = "hospital.db"


# Database connection
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# Create database tables
def init_db():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            phone TEXT NOT NULL,
            disease TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialization TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient TEXT NOT NULL,
            doctor TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# Home page
@app.route("/")
def index():
    return render_template("index.html")


# ---------------- PATIENTS ----------------

@app.route("/patients")
def patients():
    conn = get_db_connection()
    patients = conn.execute(
        "SELECT * FROM patients ORDER BY id DESC"
    ).fetchall()
    conn.close()

    return render_template("patients.html", patients=patients)


@app.route("/add_patient", methods=["GET", "POST"])
def add_patient():
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        gender = request.form["gender"]
        phone = request.form["phone"]
        disease = request.form["disease"]

        conn = get_db_connection()

        conn.execute("""
            INSERT INTO patients
            (name, age, gender, phone, disease)
            VALUES (?, ?, ?, ?, ?)
        """, (name, age, gender, phone, disease))

        conn.commit()
        conn.close()

        return redirect(url_for("patients"))

    return render_template("add_patient.html")


@app.route("/edit_patient/<int:id>", methods=["GET", "POST"])
def edit_patient(id):
    conn = get_db_connection()

    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        gender = request.form["gender"]
        phone = request.form["phone"]
        disease = request.form["disease"]

        conn.execute("""
            UPDATE patients
            SET name=?, age=?, gender=?, phone=?, disease=?
            WHERE id=?
        """, (name, age, gender, phone, disease, id))

        conn.commit()
        conn.close()

        return redirect(url_for("patients"))

    patient = conn.execute(
        "SELECT * FROM patients WHERE id=?",
        (id,)
    ).fetchone()

    conn.close()

    return render_template("edit_patient.html", patient=patient)


@app.route("/delete_patient/<int:id>")
def delete_patient(id):
    conn = get_db_connection()

    conn.execute(
        "DELETE FROM patients WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("patients"))


# ---------------- DOCTORS ----------------

@app.route("/doctors")
def doctors():
    conn = get_db_connection()

    doctors = conn.execute(
        "SELECT * FROM doctors ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template("doctors.html", doctors=doctors)


@app.route("/add_doctor", methods=["GET", "POST"])
def add_doctor():
    if request.method == "POST":
        name = request.form["name"]
        specialization = request.form["specialization"]
        phone = request.form["phone"]

        conn = get_db_connection()

        conn.execute("""
            INSERT INTO doctors
            (name, specialization, phone)
            VALUES (?, ?, ?)
        """, (name, specialization, phone))

        conn.commit()
        conn.close()

        return redirect(url_for("doctors"))

    return render_template("add_doctor.html")


@app.route("/edit_doctor/<int:id>", methods=["GET", "POST"])
def edit_doctor(id):
    conn = get_db_connection()

    if request.method == "POST":
        name = request.form["name"]
        specialization = request.form["specialization"]
        phone = request.form["phone"]

        conn.execute("""
            UPDATE doctors
            SET name=?, specialization=?, phone=?
            WHERE id=?
        """, (name, specialization, phone, id))

        conn.commit()
        conn.close()

        return redirect(url_for("doctors"))

    doctor = conn.execute(
        "SELECT * FROM doctors WHERE id=?",
        (id,)
    ).fetchone()

    conn.close()

    return render_template("edit_doctor.html", doctor=doctor)


@app.route("/delete_doctor/<int:id>")
def delete_doctor(id):
    conn = get_db_connection()

    conn.execute(
        "DELETE FROM doctors WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("doctors"))


# ---------------- APPOINTMENTS ----------------

@app.route("/appointments")
def appointments():
    conn = get_db_connection()

    appointments = conn.execute(
        "SELECT * FROM appointments ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template(
        "appointments.html",
        appointments=appointments
    )


@app.route("/add_appointment", methods=["GET", "POST"])
def add_appointment():
    if request.method == "POST":
        patient = request.form["patient"]
        doctor = request.form["doctor"]
        date = request.form["date"]
        time = request.form["time"]

        conn = get_db_connection()

        conn.execute("""
            INSERT INTO appointments
            (patient, doctor, date, time)
            VALUES (?, ?, ?, ?)
        """, (patient, doctor, date, time))

        conn.commit()
        conn.close()

        return redirect(url_for("appointments"))

    return render_template("add_appointment.html")


@app.route("/delete_appointment/<int:id>")
def delete_appointment(id):
    conn = get_db_connection()

    conn.execute(
        "DELETE FROM appointments WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("appointments"))


# Start application
if __name__ == "__main__":
    init_db()
    app.run(debug=True)