"""All HTML and CSS of the website, written as Python strings (no .js / .css / .html files)."""

CSS = r"""
:root {
  --bg: #eef2f1;
  --card: #ffffff;
  --ink: #1b2a33;
  --muted: #62727b;
  --primary: #0f766e;
  --primary-dark: #0b5953;
  --danger: #b42318;
  --line: #cfd9d6;
  --err-bg: #fdecea;
  --ok-bg: #e3f4ef;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  background: var(--bg);
  color: var(--ink);
  line-height: 1.5;
}
a { color: var(--primary); }

.topbar {
  display: flex; flex-wrap: wrap; align-items: center; gap: 0.5rem 1.25rem;
  padding: 0.75rem 1rem; background: var(--ink); color: #fff;
}
.brand { font-weight: 700; font-size: 1.15rem; color: #fff; text-decoration: none; margin-right: auto; }
.topbar nav { display: flex; gap: 1rem; }
.topbar nav a { color: #d6e4e0; text-decoration: none; }
.topbar nav a:hover { color: #fff; text-decoration: underline; }
.user { display: flex; align-items: center; gap: 0.75rem; }
.topbar .btn-outline { color: #fff; border-color: #6c828b; }

.container { max-width: 860px; margin: 1.25rem auto; padding: 0 1rem; }
.card {
  background: var(--card); border: 1px solid var(--line); border-radius: 8px;
  padding: 1.25rem; margin-bottom: 1.25rem;
}
.card.narrow { max-width: 420px; margin-left: auto; margin-right: auto; }
h1 { font-size: 1.4rem; margin: 0 0 1rem; }
.section-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; }
.section-head h1 { margin: 0; }
.muted { color: var(--muted); }

label { display: block; font-weight: 600; margin-bottom: 0.9rem; }
input[type=text], input[type=email], input[type=password], select {
  display: block; width: 100%; margin-top: 0.3rem; padding: 0.55rem 0.65rem;
  font: inherit; font-weight: 400; color: var(--ink);
  border: 1px solid var(--line); border-radius: 6px; background: #fff;
}
input:focus, select:focus, button:focus-visible, .btn:focus-visible {
  outline: 3px solid #7cc5bb; outline-offset: 1px;
}
.row { display: flex; gap: 0.5rem; align-items: center; }
.row input[type=text] { margin-top: 0; flex: 1; min-width: 0; }

.btn {
  display: inline-block; padding: 0.55rem 1rem; font: inherit; font-weight: 600;
  color: #fff; background: var(--primary); border: 1px solid var(--primary);
  border-radius: 6px; cursor: pointer; text-decoration: none; text-align: center;
}
.btn:hover { background: var(--primary-dark); }
.btn-small { padding: 0.35rem 0.7rem; font-size: 0.9rem; }
.btn-block { width: 100%; }
.btn-outline { background: transparent; color: var(--primary); }
.btn-outline:hover { background: var(--ok-bg); }
.topbar .btn-outline:hover { background: #2c4350; }
.btn-danger { background: var(--danger); border-color: var(--danger); }
.btn-danger:hover { background: #8e1b12; }

.errors {
  background: var(--err-bg); border: 1px solid #f2b8b2; color: var(--danger);
  border-radius: 6px; padding: 0.5rem 0.75rem; margin-bottom: 0.75rem;
}
.errors ul { margin: 0; padding-left: 1.1rem; }
.flash {
  background: var(--ok-bg); border: 1px solid #a8d8cd; color: var(--primary-dark);
  border-radius: 6px; padding: 0.6rem 0.9rem; margin-bottom: 1rem;
}
.empty { color: var(--muted); text-align: center; padding: 1.5rem 0.5rem; margin: 0; }

.todo-list { list-style: none; margin: 1.25rem 0 0; padding: 0; }
.todo { display: flex; flex-wrap: wrap; align-items: flex-start; gap: 0.5rem; padding: 0.6rem 0; border-top: 1px solid var(--line); }
.todo form.edit { flex: 1; min-width: 180px; }
.check {
  width: 2.1rem; height: 2.1rem; border-radius: 50%; cursor: pointer;
  border: 2px solid var(--primary); background: #fff; color: #fff; font-size: 1.1rem; line-height: 1;
}
.todo.done .check { background: var(--primary); }
.todo.done input[type=text] { text-decoration: line-through; color: var(--muted); background: #f4f7f6; }

.table-wrap { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; }
th, td { text-align: left; padding: 0.55rem 0.6rem; border-bottom: 1px solid var(--line); white-space: nowrap; }
th { background: #f3f7f6; font-size: 0.9rem; }
td.actions { display: flex; gap: 0.4rem; }

@media (max-width: 480px) {
  .container { margin-top: 0.75rem; }
  .card { padding: 1rem; }
}
"""

TEMPLATES = {}

TEMPLATES["_macros.html"] = r"""
{% macro errors_box(errors) %}
{% if errors %}
<div class="errors" role="alert"><ul>{% for e in errors %}<li>{{ e }}</li>{% endfor %}</ul></div>
{% endif %}
{% endmacro %}
"""

TEMPLATES["base.html"] = r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{% block title %}Lab Site{% endblock %}</title>
  <style>{{ css|safe }}</style>
</head>
<body>
  <header class="topbar">
    <a class="brand" href="{{ url_for('index') }}">Lab Site</a>
    {% if session.user_id %}
    <nav>
      <a href="{{ url_for('todos') }}">To-Do</a>
      <a href="{{ url_for('library') }}">Library</a>
    </nav>
    <div class="user">
      <span>Hi, {{ session.name }}</span>
      <form method="post" action="{{ url_for('logout') }}">
        <button class="btn btn-outline btn-small">Log out</button>
      </form>
    </div>
    {% endif %}
  </header>
  <main class="container">
    {% for message in get_flashed_messages() %}<div class="flash">{{ message }}</div>{% endfor %}
    {% block content %}{% endblock %}
  </main>
</body>
</html>
"""

TEMPLATES["register.html"] = r"""{% extends "base.html" %}
{% from "_macros.html" import errors_box %}
{% block title %}Register{% endblock %}
{% block content %}
<section class="card narrow">
  <h1>Create your account</h1>
  <form method="post" action="{{ url_for('register') }}">
    {{ errors_box(errors) }}
    <label>Name
      <input type="text" name="name" value="{{ form.get('name', '') }}" required maxlength="100" pattern=".*\S.*">
    </label>
    <label>Email
      <input type="email" name="email" value="{{ form.get('email', '') }}" required maxlength="255">
    </label>
    <label>Password
      <input type="password" name="password" required>
    </label>
    <label>Confirm password
      <input type="password" name="confirm_password" required>
    </label>
    <button class="btn btn-block">Register</button>
  </form>
  <p class="muted">Already have an account? <a href="{{ url_for('login') }}">Log in</a></p>
</section>
{% endblock %}
"""

TEMPLATES["login.html"] = r"""{% extends "base.html" %}
{% from "_macros.html" import errors_box %}
{% block title %}Log in{% endblock %}
{% block content %}
<section class="card narrow">
  <h1>Log in</h1>
  <form method="post" action="{{ url_for('login') }}">
    {{ errors_box(errors) }}
    <label>Email
      <input type="email" name="email" value="{{ form.get('email', '') }}" required>
    </label>
    <label>Password
      <input type="password" name="password" required>
    </label>
    <button class="btn btn-block">Log in</button>
  </form>
  <p class="muted">New here? <a href="{{ url_for('register') }}">Create an account</a></p>
</section>
{% endblock %}
"""

TEMPLATES["todos.html"] = r"""{% extends "base.html" %}
{% from "_macros.html" import errors_box %}
{% block title %}To-Do{% endblock %}
{% block content %}
<section class="card">
  <h1>To-Do</h1>
  <form method="post" action="{{ url_for('todo_add') }}">
    {{ errors_box(errors) }}
    <div class="row">
      <input type="text" name="title" placeholder="What needs to be done?" value="{{ new_title }}"
             required maxlength="200" pattern=".*\S.*">
      <button class="btn">Add</button>
    </div>
  </form>

  {% if todos %}
  <ul class="todo-list">
    {% for t in todos %}
    <li class="todo{% if t.is_done %} done{% endif %}">
      <form method="post" action="{{ url_for('todo_toggle', todo_id=t.todo_id) }}">
        <input type="hidden" name="is_done" value="{{ 0 if t.is_done else 1 }}">
        <button class="check" aria-label="{{ 'Mark as not done' if t.is_done else 'Mark as done' }}"
                title="{{ 'Mark as not done' if t.is_done else 'Mark as done' }}">{{ '✓' if t.is_done else '' }}</button>
      </form>
      <form class="edit" method="post" action="{{ url_for('todo_edit', todo_id=t.todo_id) }}">
        {{ errors_box(row_errors.get(t.todo_id, [])) }}
        <div class="row">
          <input type="text" name="title" value="{{ row_values.get(t.todo_id, t.title) }}"
                 required maxlength="200" pattern=".*\S.*">
          <button class="btn btn-small">Save</button>
        </div>
      </form>
      <a class="btn btn-danger btn-small" href="{{ url_for('todo_delete', todo_id=t.todo_id) }}">Delete</a>
    </li>
    {% endfor %}
  </ul>
  {% else %}
  <p class="empty">Nothing to do yet. Add your first to-do above.</p>
  {% endif %}
</section>
{% endblock %}
"""

TEMPLATES["library.html"] = r"""{% extends "base.html" %}
{% block title %}Library{% endblock %}
{% block content %}
<section class="card">
  <div class="section-head">
    <h1>Books</h1>
    <a class="btn btn-small" href="{{ url_for('book_new') }}">Add book</a>
  </div>
  {% if books %}
  <div class="table-wrap">
    <table>
      <thead><tr><th>ID</th><th>Title</th><th>Price</th><th>Author ID</th><th>Author</th><th></th></tr></thead>
      <tbody>
      {% for b in books %}
        <tr>
          <td>{{ b.book_id }}</td>
          <td>{{ b.title }}</td>
          <td>{{ '%.2f'|format(b.price) }}</td>
          <td>{{ b.author_id }}</td>
          <td>{{ names.get(b.author_id, '') }}</td>
          <td class="actions">
            <a class="btn btn-outline btn-small" href="{{ url_for('book_edit', book_id=b.book_id) }}">Edit</a>
            <a class="btn btn-danger btn-small" href="{{ url_for('book_delete', book_id=b.book_id) }}">Delete</a>
          </td>
        </tr>
      {% endfor %}
      </tbody>
    </table>
  </div>
  {% else %}
  <p class="empty">No books yet. Add the first one.</p>
  {% endif %}
</section>

<section class="card">
  <div class="section-head">
    <h1>Authors</h1>
    <a class="btn btn-small" href="{{ url_for('author_new') }}">Add author</a>
  </div>
  {% if authors %}
  <div class="table-wrap">
    <table>
      <thead><tr><th>ID</th><th>Name</th><th>Country</th><th></th></tr></thead>
      <tbody>
      {% for a in authors %}
        <tr>
          <td>{{ a.author_id }}</td>
          <td>{{ a.name }}</td>
          <td>{{ a.country }}</td>
          <td class="actions">
            <a class="btn btn-outline btn-small" href="{{ url_for('author_edit', author_id=a.author_id) }}">Edit</a>
            <a class="btn btn-danger btn-small" href="{{ url_for('author_delete', author_id=a.author_id) }}">Delete</a>
          </td>
        </tr>
      {% endfor %}
      </tbody>
    </table>
  </div>
  {% else %}
  <p class="empty">No authors yet. Add the first one.</p>
  {% endif %}
</section>
{% endblock %}
"""

TEMPLATES["author_form.html"] = r"""{% extends "base.html" %}
{% from "_macros.html" import errors_box %}
{% block title %}{{ 'Edit author' if author_id else 'Add author' }}{% endblock %}
{% block content %}
<section class="card narrow">
  <h1>{{ 'Edit author' if author_id else 'Add author' }}</h1>
  <form method="post">
    {{ errors_box(errors) }}
    <label>Name
      <input type="text" name="name" value="{{ form.get('name', '') }}" required maxlength="100" pattern=".*\S.*">
    </label>
    <label>Country
      <input type="text" name="country" value="{{ form.get('country', '') }}" required maxlength="50" pattern=".*\S.*">
    </label>
    <div class="row">
      <button class="btn">Save author</button>
      <a class="btn btn-outline" href="{{ url_for('library') }}">Cancel</a>
    </div>
  </form>
</section>
{% endblock %}
"""

TEMPLATES["book_form.html"] = r"""{% extends "base.html" %}
{% from "_macros.html" import errors_box %}
{% block title %}{{ 'Edit book' if book_id else 'Add book' }}{% endblock %}
{% block content %}
<section class="card narrow">
  <h1>{{ 'Edit book' if book_id else 'Add book' }}</h1>
  {% if not authors %}
    <p class="empty">There are no authors yet. <a href="{{ url_for('author_new') }}">Add an author</a> first.</p>
  {% else %}
  <form method="post">
    {{ errors_box(errors) }}
    <label>Title
      <input type="text" name="title" value="{{ form.get('title', '') }}" required maxlength="200" pattern=".*\S.*">
    </label>
    <label>Price
      <input type="number" name="price" value="{{ form.get('price', '') }}" required min="0" step="0.01">
    </label>
    <label>Author
      <select name="author_id" required>
        <option value="">Choose an author</option>
        {% for a in authors %}
        <option value="{{ a.author_id }}"{% if form.get('author_id', '')|string == a.author_id|string %} selected{% endif %}>
          {{ a.name }} (ID {{ a.author_id }})
        </option>
        {% endfor %}
      </select>
    </label>
    <div class="row">
      <button class="btn">Save book</button>
      <a class="btn btn-outline" href="{{ url_for('library') }}">Cancel</a>
    </div>
  </form>
  {% endif %}
</section>
{% endblock %}
"""

TEMPLATES["confirm.html"] = r"""{% extends "base.html" %}
{% block title %}Are you sure?{% endblock %}
{% block content %}
<section class="card narrow">
  <h1>Are you sure?</h1>
  <p>{{ message }}</p>
  <form method="post" class="row">
    <button class="btn btn-danger">Yes, delete</button>
    <a class="btn btn-outline" href="{{ cancel_url }}">Cancel</a>
  </form>
</section>
{% endblock %}
"""

TEMPLATES["error.html"] = r"""{% extends "base.html" %}
{% block title %}Error {{ code }}{% endblock %}
{% block content %}
<section class="card narrow">
  <h1>{{ code }}</h1>
  <p>{{ message }}</p>
  <a class="btn" href="{{ url_for('index') }}">Back to the site</a>
</section>
{% endblock %}
"""
