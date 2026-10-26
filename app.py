import os
from decimal import Decimal, InvalidOperation
from functools import wraps

import bcrypt
import pymysql
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, session, url_for
from jinja2 import DictLoader
from werkzeug.exceptions import HTTPException

from pages import CSS, TEMPLATES

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-only-change-me")
app.jinja_loader = DictLoader(TEMPLATES)  # the HTML lives in pages.py (Python strings)


@app.context_processor
def inject_css():
    return {"css": CSS}


def confirm_page(message, cancel_endpoint):
    """Server-side "are you sure?" page (shown on GET; the delete itself is a POST)."""
    return render_template("confirm.html", message=message, cancel_url=url_for(cancel_endpoint))

REG_DB = "registration"
LIB_DB = "library"

def get_conn(db):
    return pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=db,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )


def query(db, sql, params=(), one=False):
    conn = get_conn(db)
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchone() if one else cur.fetchall()
    finally:
        conn.close()


def execute(db, sql, params=()):
    """Run INSERT/UPDATE/DELETE. Returns (rows_changed, last_insert_id)."""
    conn = get_conn(db)
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.rowcount, cur.lastrowid
    finally:
        conn.close()


def hash_password(password):
    # bcrypt only reads the first 72 bytes
    return bcrypt.hashpw(password.encode()[:72], bcrypt.gensalt(12)).decode()


def check_password(password, password_hash):
    try:
        return bcrypt.checkpw(password.encode()[:72], password_hash.encode())
    except ValueError:
        return False


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped


@app.route("/")
def index():
    return redirect(url_for("todos" if "user_id" in session else "login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        return redirect(url_for("todos"))
    errors, form = [], {}
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")
        form = {"name": name, "email": email}

        if not name:
            errors.append("Name is required")
        elif len(name) > 100:
            errors.append("Name is too long (100 characters at most)")
        if not email:
            errors.append("Email is required")
        elif len(email) > 255:
            errors.append("Email is too long (255 characters at most)")
        if not password:
            errors.append("Password is required")
        if not confirm:
            errors.append("Confirm password is required")
        if password and confirm and password != confirm:
            errors.append("Passwords do not match")

        if not errors:
            try:
                _, new_id = execute(
                    REG_DB,
                    "INSERT INTO users (email, name, password_hash) VALUES (%s, %s, %s)",
                    (email, name, hash_password(password)),
                )
            except pymysql.err.IntegrityError as exc:
                if exc.args[0] == 1062:  # duplicate UNIQUE(email)
                    errors.append("Email Already Exists")
                else:
                    raise
            else:
                session.clear()
                session["user_id"] = new_id
                session["name"] = name
                return redirect(url_for("todos"))
    return render_template("register.html", errors=errors, form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("todos"))
    errors, form = [], {}
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        form = {"email": email}

        if not email:
            errors.append("Email is required")
        if not password:
            errors.append("Password is required")

        if not errors:
            user = query(
                REG_DB,
                "SELECT user_id, name, password_hash FROM users WHERE email = %s",
                (email,),
                one=True,
            )
            if user and check_password(password, user["password_hash"]):
                session.clear()
                session["user_id"] = user["user_id"]
                session["name"] = user["name"]
                return redirect(url_for("todos"))
            errors.append("Invalid email or password")  # same text for both cases
    return render_template("login.html", errors=errors, form=form)


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))

def check_title(title):
    if not title.strip():
        return ["Title is required"]
    if len(title.strip()) > 200:
        return ["Title is too long (200 characters at most)"]
    return []


def render_todos(errors=None, new_title="", row_errors=None, row_values=None):
    rows = query(
        REG_DB,
        "SELECT todo_id, title, is_done, created_at FROM todos "
        "WHERE user_id = %s ORDER BY todo_id DESC",
        (session["user_id"],),
    )
    return render_template(
        "todos.html",
        todos=rows,
        errors=errors or [],
        new_title=new_title,
        row_errors=row_errors or {},
        row_values=row_values or {},
    )


@app.route("/todos")
@login_required
def todos():
    return render_todos()


@app.route("/todos/add", methods=["POST"])
@login_required
def todo_add():
    title = request.form.get("title", "").strip()
    errors = check_title(title)
    if errors:  # same page again, database untouched
        return render_todos(errors=errors, new_title=title)
    execute(
        REG_DB,
        "INSERT INTO todos (user_id, title) VALUES (%s, %s)",
        (session["user_id"], title),
    )
    return redirect(url_for("todos"))


@app.route("/todos/<int:todo_id>/edit", methods=["POST"])
@login_required
def todo_edit(todo_id):
    title = request.form.get("title", "").strip()
    errors = check_title(title)
    if errors:
        return render_todos(row_errors={todo_id: errors}, row_values={todo_id: title})
    execute(
        REG_DB,
        "UPDATE todos SET title = %s WHERE todo_id = %s AND user_id = %s",
        (title, todo_id, session["user_id"]),
    )
    return redirect(url_for("todos"))


@app.route("/todos/<int:todo_id>/toggle", methods=["POST"])
@login_required
def todo_toggle(todo_id):
    is_done = 1 if request.form.get("is_done") == "1" else 0
    execute(
        REG_DB,
        "UPDATE todos SET is_done = %s WHERE todo_id = %s AND user_id = %s",
        (is_done, todo_id, session["user_id"]),
    )
    return redirect(url_for("todos"))


@app.route("/todos/<int:todo_id>/delete", methods=["GET", "POST"])
@login_required
def todo_delete(todo_id):
    if request.method == "GET":
        return confirm_page("Are you sure you want to delete this to-do?", "todos")
    execute(
        REG_DB,
        "DELETE FROM todos WHERE todo_id = %s AND user_id = %s",
        (todo_id, session["user_id"]),
    )
    return redirect(url_for("todos"))


def get_authors():
    return query(LIB_DB, "SELECT author_id, name, country FROM author ORDER BY author_id")


def check_author(name, country):
    errors = []
    if not name:
        errors.append("Name is required")
    elif len(name) > 100:
        errors.append("Name is too long (100 characters at most)")
    if not country:
        errors.append("Country is required")
    elif len(country) > 50:
        errors.append("Country is too long (50 characters at most)")
    return errors


def check_book(title, price, author_id, valid_ids):
    errors = []
    if not title:
        errors.append("Title is required")
    elif len(title) > 200:
        errors.append("Title is too long (200 characters at most)")

    if not price:
        errors.append("Price is required")
    else:
        try:
            value = Decimal(price)
            if not value.is_finite():
                raise InvalidOperation
            if value < 0:
                errors.append("Price cannot be negative")
            elif value > Decimal("99999999.99"):
                errors.append("Price is too large")
        except InvalidOperation:
            errors.append("Price must be a number")

    if not author_id:
        errors.append("Author is required")
    elif not author_id.isdigit() or int(author_id) not in valid_ids:
        errors.append("Author does not exist")
    return errors


@app.route("/library")
@login_required
def library():
    authors = get_authors()
    books = query(LIB_DB, "SELECT book_id, title, price, author_id FROM book ORDER BY book_id")
    names = {a["author_id"]: a["name"] for a in authors}  # no JOIN needed
    return render_template("library.html", authors=authors, books=books, names=names)


@app.route("/library/authors/new", methods=["GET", "POST"])
@login_required
def author_new():
    errors, form = [], {"name": "", "country": ""}
    if request.method == "POST":
        form = {
            "name": request.form.get("name", "").strip(),
            "country": request.form.get("country", "").strip(),
        }
        errors = check_author(form["name"], form["country"])
        if not errors:
            execute(
                LIB_DB,
                "INSERT INTO author (name, country) VALUES (%s, %s)",
                (form["name"], form["country"]),
            )
            flash("Author added")
            return redirect(url_for("library"))
    return render_template("author_form.html", errors=errors, form=form, author_id=None)


@app.route("/library/authors/<int:author_id>/edit", methods=["GET", "POST"])
@login_required
def author_edit(author_id):
    author = query(
        LIB_DB,
        "SELECT author_id, name, country FROM author WHERE author_id = %s",
        (author_id,),
        one=True,
    )
    if not author:
        flash("That author does not exist")
        return redirect(url_for("library"))
    errors, form = [], {"name": author["name"], "country": author["country"]}
    if request.method == "POST":
        form = {
            "name": request.form.get("name", "").strip(),
            "country": request.form.get("country", "").strip(),
        }
        errors = check_author(form["name"], form["country"])
        if not errors:
            execute(
                LIB_DB,
                "UPDATE author SET name = %s, country = %s WHERE author_id = %s",
                (form["name"], form["country"], author_id),
            )
            flash("Author updated")
            return redirect(url_for("library"))
    return render_template("author_form.html", errors=errors, form=form, author_id=author_id)


@app.route("/library/authors/<int:author_id>/delete", methods=["GET", "POST"])
@login_required
def author_delete(author_id):
    if request.method == "GET":
        return confirm_page("Delete this author? All of their books will be deleted too.", "library")
    execute(LIB_DB, "DELETE FROM author WHERE author_id = %s", (author_id,))
    flash("Author and their books deleted")
    return redirect(url_for("library"))


# ---- books
@app.route("/library/books/new", methods=["GET", "POST"])
@login_required
def book_new():
    authors = get_authors()
    valid_ids = {a["author_id"] for a in authors}
    errors, form = [], {"title": "", "price": "", "author_id": ""}
    if request.method == "POST":
        form = {
            "title": request.form.get("title", "").strip(),
            "price": request.form.get("price", "").strip(),
            "author_id": request.form.get("author_id", "").strip(),
        }
        errors = check_book(form["title"], form["price"], form["author_id"], valid_ids)
        if not errors:
            try:
                execute(
                    LIB_DB,
                    "INSERT INTO book (title, price, author_id) VALUES (%s, %s, %s)",
                    (form["title"], form["price"], int(form["author_id"])),
                )
                flash("Book added")
                return redirect(url_for("library"))
            except pymysql.err.IntegrityError as exc:
                if exc.args[0] == 1452:  # foreign key: author does not exist
                    errors.append("Author does not exist")
                else:
                    raise
    return render_template("book_form.html", errors=errors, form=form, authors=authors, book_id=None)


@app.route("/library/books/<int:book_id>/edit", methods=["GET", "POST"])
@login_required
def book_edit(book_id):
    book = query(
        LIB_DB,
        "SELECT book_id, title, price, author_id FROM book WHERE book_id = %s",
        (book_id,),
        one=True,
    )
    if not book:
        flash("That book does not exist")
        return redirect(url_for("library"))
    authors = get_authors()
    valid_ids = {a["author_id"] for a in authors}
    errors = []
    form = {
        "title": book["title"],
        "price": "%.2f" % book["price"],
        "author_id": str(book["author_id"]),
    }
    if request.method == "POST":
        form = {
            "title": request.form.get("title", "").strip(),
            "price": request.form.get("price", "").strip(),
            "author_id": request.form.get("author_id", "").strip(),
        }
        errors = check_book(form["title"], form["price"], form["author_id"], valid_ids)
        if not errors:
            try:
                execute(
                    LIB_DB,
                    "UPDATE book SET title = %s, price = %s, author_id = %s WHERE book_id = %s",
                    (form["title"], form["price"], int(form["author_id"]), book_id),
                )
                flash("Book updated")
                return redirect(url_for("library"))
            except pymysql.err.IntegrityError as exc:
                if exc.args[0] == 1452:
                    errors.append("Author does not exist")
                else:
                    raise
    return render_template("book_form.html", errors=errors, form=form, authors=authors, book_id=book_id)


@app.route("/library/books/<int:book_id>/delete", methods=["GET", "POST"])
@login_required
def book_delete(book_id):
    if request.method == "GET":
        return confirm_page("Are you sure you want to delete this book?", "library")
    execute(LIB_DB, "DELETE FROM book WHERE book_id = %s", (book_id,))
    flash("Book deleted")
    return redirect(url_for("library"))

@app.errorhandler(Exception)
def handle_error(exc):
    if isinstance(exc, HTTPException):
        code, message = exc.code, exc.description
    else:
        app.logger.exception(exc)  # the details go to the terminal only
        code = 500
        message = "Something went wrong. Check that MySQL is running and try again."
    return render_template("error.html", code=code, message=message), code


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
