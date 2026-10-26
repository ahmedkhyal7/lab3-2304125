# Lab 3 - Foreign Keys and Simple SQL (+ Lab 2 Login & To-Do site)

## 1. Ahmed Khyal Ahmed (2304125) Group2,section 4

## 2. Technology
- Back end: Python 3 + Flask, PyMySQL (plain SQL with `%s` parameters, no ORM), bcrypt
- Front end: written from Python too: `website/pages.py` holds the HTML pages and the CSS as Python strings (Flask/Jinja renders them) Browser-side checks use HTML5 attributes (`required`, `maxlength`, `type=number`); the server repeats every check with the exact messages
- Database: MySQL (`company`, `registration`, `library`)

## 3. How to run it (from an empty machine)
1. Install Python 3.10+, MySQL Server and MySQL Workbench.
2. In MySQL Workbench open and run these scripts (File > Open SQL Script, then the lightning button), in this order:
   1. `problem1_DDL.sql`, then `problem1_DML.sql` (database `company`)
   2. `problem2_DDL.sql`, then `problem2_DML.sql` (database `library`)
   3. `website/database/schema.sql` (database `registration`: users + todos)

   Or from a terminal: `mysql -u root -p < problem2_DDL.sql` (same for the other files).
3. Open a terminal in the `website` folder and run:
   ```
   python -m venv venv
   venv\Scripts\activate          (Windows)   |   source venv/bin/activate   (Mac/Linux)
   pip install -r requirements.txt
   copy .env.example .env         (Windows)   |   cp .env.example .env        (Mac/Linux)
   ```
4. Open `.env` and write your MySQL password in `DB_PASSWORD` (and any long random text in `SECRET_KEY`).
5. Start the server: `python app.py`
6. Open http://127.0.0.1:5000, register an account, then use **To-Do** and **Library** in the top bar.

## 4. Features
- Lab 2: R1 register, R2 login/logout, R3 private list, R4-R7 add/edit/done/delete (delete asks "are you sure?" on a confirmation page),
  R8 validation in the browser (HTML5) and on the server, R9 bcrypt hashes + parameterised queries + `user_id` from the session,
  R10 responsive UI (works at 360 px).
- Lab 3 - Library (log in first):
  - F2.1 table of books (with `author_id`) and table of authors
  - F2.2 add a book / add an author
  - F2.3 edit a book / edit an author
  - F2.4 remove a book
  - F2.5 remove an author (the database deletes their books too: `ON DELETE CASCADE`)
- Problem 1 files: `problem1_DDL.sql`, `problem1_DML.sql`, `problem1_Answers.txt`.
- All the (F2) are in the screenshots folder

## 5. Screenshots
Files of F2. are in the `screenshots/` folder

**Lab 3 Problem 1 (Q1.1 - Q1.3):** see `problem1_Answers.txt`.