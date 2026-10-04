from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import get_db
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "internship_portal_secret_key"


# =========================================================
# HOME
# =========================================================

@app.route("/")
def index():
    return render_template("index.html")


# =========================================================
# ADMIN - REGISTER
# =========================================================

@app.route("/admin/register", methods=["GET", "POST"])
def admin_register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM admins WHERE email=%s",
            (email,)
        )

        if cursor.fetchone():
            cursor.close()
            db.close()

            flash("Admin email already registered.", "error")
            return redirect(url_for("admin_register"))

        cursor.execute("""
            INSERT INTO admins
            (name, email, password)
            VALUES (%s, %s, %s)
        """, (name, email, password))

        db.commit()

        cursor.close()
        db.close()

        flash("Admin registration successful. Please login.", "success")

        return redirect(url_for("admin_login"))

    return render_template("admin/register.html")


# =========================================================
# ADMIN - LOGIN
# =========================================================

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM admins WHERE email=%s",
            (email,)
        )

        admin = cursor.fetchone()

        cursor.close()
        db.close()

        if admin and check_password_hash(
            admin["password"],
            password
        ):

            session["admin_id"] = admin["admin_id"]
            session["admin_name"] = admin["name"]

            return redirect(url_for("admin_dashboard"))

        flash("Invalid email or password.", "error")

    return render_template("admin/login.html")


# =========================================================
# ADMIN - DASHBOARD
# =========================================================

@app.route("/admin/dashboard")
def admin_dashboard():

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    db = get_db()
    cursor = db.cursor(dictionary=True)

    # Total internships
    cursor.execute(
        "SELECT COUNT(*) AS total FROM internships"
    )

    total_internships = cursor.fetchone()["total"]

    # Total students
    cursor.execute(
        "SELECT COUNT(*) AS total FROM students"
    )

    total_students = cursor.fetchone()["total"]

    # Total applications
    cursor.execute(
        "SELECT COUNT(*) AS total FROM applications"
    )

    total_applications = cursor.fetchone()["total"]

    # Get all internships
    cursor.execute("""
        SELECT *
        FROM internships
        ORDER BY internship_id DESC
    """)

    internships = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "admin/dashboard.html",
        total_internships=total_internships,
        total_students=total_students,
        total_applications=total_applications,
        internships=internships
    )


# =========================================================
# ADMIN - ADD INTERNSHIP
# =========================================================

@app.route("/admin/internship/add", methods=["GET", "POST"])
def add_internship():

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    if request.method == "POST":

        title = request.form["title"]
        company = request.form["company"]
        location = request.form["location"]
        duration = request.form["duration"]
        stipend = request.form["stipend"]
        skills = request.form["skills"]
        description = request.form["description"]
        deadline = request.form["deadline"]

        db = get_db()
        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO internships
            (
                title,
                company,
                location,
                duration,
                stipend,
                skills,
                description,
                deadline
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            title,
            company,
            location,
            duration,
            stipend,
            skills,
            description,
            deadline
        ))

        db.commit()

        cursor.close()
        db.close()

        flash(
            "Internship added successfully!",
            "success"
        )

        return redirect(url_for("admin_dashboard"))

    return render_template(
        "admin/add_internship.html"
    )


# =========================================================
# ADMIN - EDIT INTERNSHIP
# =========================================================

@app.route(
    "/admin/internship/edit/<int:internship_id>",
    methods=["GET", "POST"]
)
def edit_internship(internship_id):

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    db = get_db()
    cursor = db.cursor(dictionary=True)

    # Update internship
    if request.method == "POST":

        title = request.form["title"]
        company = request.form["company"]
        location = request.form["location"]
        duration = request.form["duration"]
        stipend = request.form["stipend"]
        skills = request.form["skills"]
        description = request.form["description"]
        deadline = request.form["deadline"]

        cursor.execute("""
            UPDATE internships
            SET
                title=%s,
                company=%s,
                location=%s,
                duration=%s,
                stipend=%s,
                skills=%s,
                description=%s,
                deadline=%s
            WHERE internship_id=%s
        """, (
            title,
            company,
            location,
            duration,
            stipend,
            skills,
            description,
            deadline,
            internship_id
        ))

        db.commit()

        cursor.close()
        db.close()

        flash(
            "Internship updated successfully!",
            "success"
        )

        return redirect(
            url_for("admin_dashboard")
        )

    # Get internship details
    cursor.execute("""
        SELECT *
        FROM internships
        WHERE internship_id=%s
    """, (internship_id,))

    internship = cursor.fetchone()

    cursor.close()
    db.close()

    if not internship:
        flash(
            "Internship not found.",
            "error"
        )

        return redirect(
            url_for("admin_dashboard")
        )

    return render_template(
        "admin/edit_internship.html",
        internship=internship
    )


# =========================================================
# ADMIN - DELETE INTERNSHIP
# =========================================================

@app.route(
    "/admin/internship/delete/<int:internship_id>",
    methods=["GET", "POST"]
)
def delete_internship(internship_id):

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM internships WHERE internship_id=%s",
        (internship_id,)
    )

    db.commit()

    cursor.close()
    db.close()

    flash(
        "Internship deleted successfully!",
        "success"
    )

    return redirect(
        url_for("admin_dashboard")
    )


# =========================================================
# ADMIN - VIEW APPLICATIONS
# =========================================================

@app.route("/admin/applications")
def admin_applications():

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            applications.application_id,
            applications.status,
            applications.applied_at,

            students.name AS student_name,
            students.email AS student_email,

            internships.title AS internship_title,
            internships.company

        FROM applications

        JOIN students
            ON applications.student_id =
               students.student_id

        JOIN internships
            ON applications.internship_id =
               internships.internship_id

        ORDER BY applications.application_id DESC
    """)

    applications = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "admin/applications.html",
        applications=applications
    )


# =========================================================
# ADMIN - SHORTLIST / REJECT
# =========================================================

@app.route(
    "/admin/application/<int:application_id>/<status>"
)
def update_application(application_id, status):

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    if status not in [
        "Shortlisted",
        "Rejected"
    ]:
        return redirect(
            url_for("admin_applications")
        )

    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        UPDATE applications
        SET status=%s
        WHERE application_id=%s
    """, (
        status,
        application_id
    ))

    db.commit()

    cursor.close()
    db.close()

    flash(
        "Application status updated.",
        "success"
    )

    return redirect(
        url_for("admin_applications")
    )


# =========================================================
# STUDENT - REGISTER
# =========================================================

@app.route("/student/register", methods=["GET", "POST"])
def student_register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = generate_password_hash(
            request.form["password"]
        )

        phone = request.form["phone"]
        course = request.form["course"]
        college = request.form["college"]

        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM students WHERE email=%s",
            (email,)
        )

        if cursor.fetchone():

            cursor.close()
            db.close()

            flash(
                "Student email already registered.",
                "error"
            )

            return redirect(
                url_for("student_register")
            )

        cursor.execute("""
            INSERT INTO students
            (
                name,
                email,
                password,
                phone,
                course,
                college
            )
            VALUES (%s,%s,%s,%s,%s,%s)
        """, (
            name,
            email,
            password,
            phone,
            course,
            college
        ))

        db.commit()

        cursor.close()
        db.close()

        flash(
            "Registration successful. Please login.",
            "success"
        )

        return redirect(
            url_for("student_login")
        )

    return render_template(
        "student/register.html"
    )


# =========================================================
# STUDENT - LOGIN
# =========================================================

@app.route("/student/login", methods=["GET", "POST"])
def student_login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM students WHERE email=%s",
            (email,)
        )

        student = cursor.fetchone()

        cursor.close()
        db.close()

        if student and check_password_hash(
            student["password"],
            password
        ):

            session["student_id"] = student["student_id"]
            session["student_name"] = student["name"]

            return redirect(
                url_for("student_dashboard")
            )

        flash(
            "Invalid email or password.",
            "error"
        )

    return render_template(
        "student/login.html"
    )


# =========================================================
# STUDENT - DASHBOARD
# =========================================================

@app.route("/student/dashboard")
def student_dashboard():

    if "student_id" not in session:
        return redirect(
            url_for("student_login")
        )

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM internships
        WHERE deadline >= CURDATE()
        ORDER BY internship_id DESC
        LIMIT 6
    """)

    internships = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "student/dashboard.html",
        internships=internships
    )


# =========================================================
# STUDENT - BROWSE INTERNSHIPS
# =========================================================

@app.route("/student/internships")
def student_internships():

    if "student_id" not in session:
        return redirect(
            url_for("student_login")
        )

    search = request.args.get(
        "search",
        ""
    )

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM internships
        WHERE deadline >= CURDATE()
        AND (
            title LIKE %s
            OR company LIKE %s
            OR skills LIKE %s
        )
        ORDER BY internship_id DESC
    """, (
        f"%{search}%",
        f"%{search}%",
        f"%{search}%"
    ))

    internships = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "student/internships.html",
        internships=internships,
        search=search
    )


# =========================================================
# STUDENT - INTERNSHIP DETAILS
# =========================================================

@app.route(
    "/student/internship/<int:internship_id>"
)
def internship_details(internship_id):

    if "student_id" not in session:
        return redirect(
            url_for("student_login")
        )

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM internships
        WHERE internship_id=%s
    """, (internship_id,))

    internship = cursor.fetchone()

    cursor.close()
    db.close()

    return render_template(
        "student/internship_details.html",
        internship=internship
    )


# =========================================================
# STUDENT - APPLY
# =========================================================

@app.route(
    "/student/apply/<int:internship_id>"
)
def apply_internship(internship_id):

    if "student_id" not in session:
        return redirect(
            url_for("student_login")
        )

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM applications
        WHERE student_id=%s
        AND internship_id=%s
    """, (
        session["student_id"],
        internship_id
    ))

    existing = cursor.fetchone()

    if existing:

        flash(
            "You have already applied for this internship.",
            "error"
        )

    else:

        cursor.execute("""
            INSERT INTO applications
            (
                student_id,
                internship_id,
                status
            )
            VALUES (%s,%s,'Pending')
        """, (
            session["student_id"],
            internship_id
        ))

        db.commit()

        flash(
            "Application submitted successfully!",
            "success"
        )

    cursor.close()
    db.close()

    return redirect(
        url_for(
            "internship_details",
            internship_id=internship_id
        )
    )


# =========================================================
# STUDENT - MY APPLICATIONS
# =========================================================

@app.route("/student/applications")
def student_applications():

    if "student_id" not in session:
        return redirect(
            url_for("student_login")
        )

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            applications.*,
            internships.title,
            internships.company,
            internships.location

        FROM applications

        JOIN internships
            ON applications.internship_id =
               internships.internship_id

        WHERE applications.student_id=%s

        ORDER BY applications.application_id DESC
    """, (
        session["student_id"],
    ))

    applications = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "student/applications.html",
        applications=applications
    )


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("index")
    )


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":
    app.run(debug=True)