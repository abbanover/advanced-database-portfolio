"""Portfolio 3: Transactions and Concurrency (ACID demo on the library database).
Run:  python3 Abdullahi_Abba_301917722_P3_Transactions.py
"""
import glob, os, sqlite3, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
SCHEMA = open(glob.glob(os.path.join(HERE, "..", "portfolio-1-database-design", "*_P1_Schema.sql"))[0]).read()
path = os.path.join(tempfile.mkdtemp(), "library.db")

setup = sqlite3.connect(path)
setup.executescript(SCHEMA)
setup.close()

def connect(timeout=0.2):
    c = sqlite3.connect(path, timeout=timeout, isolation_level=None)  # we control BEGIN/COMMIT
    c.execute("PRAGMA foreign_keys = ON")
    return c

def available(c, book_id):
    return c.execute("SELECT available_copies FROM books WHERE book_id=?", (book_id,)).fetchone()[0]

def borrow(c, member_id, book_id):
    """Borrow = insert a loan AND reduce available copies. Both must succeed together (atomicity)."""
    c.execute("BEGIN IMMEDIATE")
    try:
        c.execute("INSERT INTO loans(member_id,book_id,borrow_date,due_date) VALUES (?,?,'2026-10-17','2026-10-31')",
                  (member_id, book_id))
        c.execute("UPDATE books SET available_copies = available_copies - 1 WHERE book_id=?", (book_id,))
        c.execute("COMMIT")
        return "COMMITTED"
    except sqlite3.Error as e:
        c.execute("ROLLBACK")
        return f"ROLLED BACK ({e})"

db = connect()
count_loans = lambda c: c.execute("SELECT COUNT(*) FROM loans").fetchone()[0]

print("=== Test 1: successful transaction (COMMIT) ===")
print("Before: loans =", count_loans(db), "| copies of book 4 =", available(db, 4))
print("Result:", borrow(db, 6, 4))
print("After:  loans =", count_loans(db), "| copies of book 4 =", available(db, 4))

print("\n=== Test 2: failing transaction (ROLLBACK) ===")
print("Book 10 has only 1 copy and it is already borrowed (available =", available(db, 10), ")")
print("Before: loans =", count_loans(db))
print("Result:", borrow(db, 1, 10))
print("After:  loans =", count_loans(db), "(unchanged - the loan INSERT was undone, so no half-finished data)")

print("\n=== Test 3: concurrency control (two users at the same time) ===")
A, B = connect(), connect()
A.execute("BEGIN IMMEDIATE")
A.execute("UPDATE books SET available_copies = available_copies - 1 WHERE book_id=2")
print("User A started borrowing book 2 (not committed yet). A sees copies =", available(A, 2))
print("User B reads book 2 meanwhile and sees copies =", available(B, 2), "-> no dirty read (isolation)")
try:
    B.execute("BEGIN IMMEDIATE")
    print("User B got write lock (unexpected)")
except sqlite3.OperationalError as e:
    print("User B tries to write book 2 at the same time ->", e, "-> blocked, so no lost update")
A.execute("COMMIT")
print("User A COMMITTED.")
B.execute("BEGIN IMMEDIATE")
print("User B retries after A finished: B now sees copies =", available(B, 2))
B.execute("UPDATE books SET available_copies = available_copies - 1 WHERE book_id=2")
B.execute("COMMIT")
print("User B COMMITTED. Final copies of book 2 =", available(db, 2), "(2 total - 2 borrowers = 0, correct)")
