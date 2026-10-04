from flask import Flask, render_template, request, redirect, session
from database import create_tables, get_db

app = Flask(__name__)

app.secret_key = "adarsh-school-secret-key"

create_tables()


# ==============================
# HOME PAGE
# ==============================

@app.route("/")
def home():
    return render_template("index.html")


# ==============================
# ABOUT PAGE
# ==============================

@app.route("/about")
def about():
    return render_template("about.html")


# ==============================
# EVENTS PAGE
# ==============================

@app.route("/events")
def events():

    conn = get_db()

    events = conn.execute(
        "SELECT * FROM events ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template(
        "events.html",
        events=events
    )


# ==============================
# ADD EVENT PAGE
# ==============================

@app.route("/add-event-page")
def add_event_page():

    if not session.get("admin_logged_in"):
        return redirect("/login")

    return render_template("add_event.html")


# ==============================
# ADD EVENT
# ==============================

@app.route("/add-event", methods=["POST"])
def add_event():

    if not session.get("admin_logged_in"):
        return redirect("/login")

    title = request.form["title"]
    event_date = request.form["event_date"]
    description = request.form["description"]

    conn = get_db()

    conn.execute(
        """
        INSERT INTO events
        (title, event_date, description)
        VALUES (?, ?, ?)
        """,
        (
            title,
            event_date,
            description
        )
    )

    conn.commit()
    conn.close()

    return redirect("/events")


# ==============================
# DELETE EVENT
# ==============================

@app.route("/delete-event/<int:event_id>")
def delete_event(event_id):

    if not session.get("admin_logged_in"):
        return redirect("/login")

    conn = get_db()

    conn.execute(
        "DELETE FROM events WHERE id = ?",
        (event_id,)
    )

    conn.commit()
    conn.close()

    return redirect("/events")


# ==============================
# EDIT EVENT
# ==============================

@app.route("/edit-event/<int:event_id>")
def edit_event(event_id):

    if not session.get("admin_logged_in"):
        return redirect("/login")

    conn = get_db()

    event = conn.execute(
        "SELECT * FROM events WHERE id = ?",
        (event_id,)
    ).fetchone()

    conn.close()

    return render_template(
        "edit_event.html",
        event=event
    )


# ==============================
# UPDATE EVENT
# ==============================

@app.route(
    "/update-event/<int:event_id>",
    methods=["POST"]
)
def update_event(event_id):

    if not session.get("admin_logged_in"):
        return redirect("/login")

    title = request.form["title"]
    event_date = request.form["event_date"]
    description = request.form["description"]

    conn = get_db()

    conn.execute(
        """
        UPDATE events
        SET
            title = ?,
            event_date = ?,
            description = ?
        WHERE id = ?
        """,
        (
            title,
            event_date,
            description,
            event_id
        )
    )

    conn.commit()
    conn.close()

    return redirect("/events")


# ==============================
# DEFAULTERS PAGE
# ==============================

@app.route("/defaulters")
def defaulters():

    conn = get_db()

    defaulters = conn.execute(
        "SELECT * FROM defaulters ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template(
        "defaulters.html",
        defaulters=defaulters
    )


# ==============================
# ADD STUDENT PAGE
# ==============================

@app.route("/add-student-page")
def add_student_page():

    if not session.get("admin_logged_in"):
        return redirect("/login")

    return render_template(
        "add_student.html"
    )


# ==============================
# ADD DEFAULTER
# ==============================

@app.route("/add-defaulter", methods=["POST"])
def add_defaulter():

    if not session.get("admin_logged_in"):
        return redirect("/login")

    student_name = request.form["student_name"]
    class_name = request.form["class_name"]
    roll_number = request.form["roll_number"]
    due_amount = request.form["due_amount"]
    due_date = request.form["due_date"]
    reason = request.form["reason"]

    conn = get_db()

    conn.execute(
        """
        INSERT INTO defaulters
        (
            student_name,
            class_name,
            roll_number,
            due_amount,
            due_date,
            reason
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            student_name,
            class_name,
            roll_number,
            due_amount,
            due_date,
            reason
        )
    )

    conn.commit()
    conn.close()

    return redirect("/defaulters")


# ==============================
# DELETE DEFAULTER
# ==============================

@app.route("/delete-defaulter/<int:student_id>")
def delete_defaulter(student_id):

    if not session.get("admin_logged_in"):
        return redirect("/login")

    conn = get_db()

    conn.execute(
        "DELETE FROM defaulters WHERE id = ?",
        (student_id,)
    )

    conn.commit()
    conn.close()

    return redirect("/defaulters")


# ==============================
# EDIT DEFAULTER
# ==============================

@app.route("/edit-defaulter/<int:student_id>")
def edit_defaulter(student_id):

    if not session.get("admin_logged_in"):
        return redirect("/login")

    conn = get_db()

    student = conn.execute(
        "SELECT * FROM defaulters WHERE id = ?",
        (student_id,)
    ).fetchone()

    conn.close()

    return render_template(
        "edit_defaulter.html",
        student=student
    )


# ==============================
# UPDATE DEFAULTER
# ==============================

@app.route(
    "/update-defaulter/<int:student_id>",
    methods=["POST"]
)
def update_defaulter(student_id):

    if not session.get("admin_logged_in"):
        return redirect("/login")

    student_name = request.form["student_name"]
    class_name = request.form["class_name"]
    roll_number = request.form["roll_number"]
    due_amount = request.form["due_amount"]
    due_date = request.form["due_date"]
    reason = request.form["reason"]

    conn = get_db()

    conn.execute(
        """
        UPDATE defaulters
        SET
            student_name = ?,
            class_name = ?,
            roll_number = ?,
            due_amount = ?,
            due_date = ?,
            reason = ?
        WHERE id = ?
        """,
        (
            student_name,
            class_name,
            roll_number,
            due_amount,
            due_date,
            reason,
            student_id
        )
    )

    conn.commit()
    conn.close()

    return redirect("/defaulters")


# ==============================
# ADMIN LOGIN
# ==============================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin123":

            session["admin_logged_in"] = True

            return redirect("/admin")

        return "Invalid username or password"

    return render_template(
        "login.html"
    )


# ==============================
# ADMIN DASHBOARD
# ==============================

@app.route("/admin")
def admin():

    if not session.get("admin_logged_in"):
        return redirect("/login")

    return render_template(
        "admin.html"
    )


# ==============================
# LOGOUT
# ==============================

@app.route("/logout")
def logout():

    session.pop(
        "admin_logged_in",
        None
    )

    return redirect("/login")


# ==============================
# RUN SERVER
# ==============================

if __name__ == "__main__":
    app.run(debug=True)