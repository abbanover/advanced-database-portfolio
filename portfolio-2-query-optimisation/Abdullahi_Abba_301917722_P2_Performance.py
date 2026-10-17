"""Portfolio 2: runs the queries, shows execution plans, adds indexes and measures speed.
Run:  python3 Abdullahi_Abba_301917722_P2_Performance.py
"""
import glob, os, random, sqlite3, time
HERE = os.path.dirname(os.path.abspath(__file__))
SCHEMA = open(glob.glob(os.path.join(HERE, "..", "portfolio-1-database-design", "*_P1_Schema.sql"))[0]).read()
QUERIES = open(glob.glob(os.path.join(HERE, "*_P2_Queries.sql"))[0]).read()
body, index_sql = QUERIES.split("-- ==INDEXES==")
queries = [q.strip() for q in body.split(";") if "SELECT" in q]

db = sqlite3.connect(":memory:")
db.executescript(SCHEMA)

print("=== Query results ===")
for i, q in enumerate(queries, 1):
    print(f"\n-- Q{i}")
    for row in db.execute(q):
        print(row)

def plan(q):
    return [r[3] for r in db.execute("EXPLAIN QUERY PLAN " + q)]

print("\n=== Execution plans BEFORE indexes (Q4) ===")
for p in plan(queries[3]): print(p)
print("\n=== Execution plans BEFORE indexes (Q2) ===")
for p in plan(queries[1]): print(p)

db.executescript(index_sql)
print("\n=== Execution plans AFTER indexes (Q4) ===")
for p in plan(queries[3]): print(p)
print("\n=== Execution plans AFTER indexes (Q2) ===")
for p in plan(queries[1]): print(p)

# ---- Performance test on a bigger table (100,000 loans) ----
print("\n=== Performance test: 100,000 loans, 2,000 members ===")
big = sqlite3.connect(":memory:")
big.executescript(SCHEMA.split("-- ---------- Sample")[0])  # tables only
random.seed(42)
big.executemany("INSERT INTO members VALUES (?,?,?,?)",
    [(i, f"Member {i}", f"m{i}@example.com", "2026-01-01") for i in range(1, 2001)])
big.executemany("INSERT INTO categories VALUES (?,?)", [(1, "Computing")])
big.executemany("INSERT INTO books VALUES (?,?,?,?,?,?,?)",
    [(i, f"isbn{i}", f"Book {i}", "Author", 1, 5, 5) for i in range(1, 501)])
big.executemany("INSERT INTO loans(member_id,book_id,borrow_date,due_date,return_date) VALUES (?,?,?,?,?)",
    [(random.randint(1, 2000), random.randint(1, 500), "2026-09-01", "2026-09-15", None) for _ in range(100000)])
big.commit()

def timed(label):
    t = time.perf_counter()
    for m in range(1, 301):
        big.execute("SELECT * FROM loans WHERE member_id = ?", (m,)).fetchall()
    ms = (time.perf_counter() - t) * 1000
    print(f"{label}: 300 lookups took {ms:.1f} ms")
    return ms

print("Plan before:", [r[3] for r in big.execute("EXPLAIN QUERY PLAN SELECT * FROM loans WHERE member_id = 5")])
before = timed("Without index")
big.execute("CREATE INDEX idx_loans_member_id ON loans(member_id)")
print("Plan after: ", [r[3] for r in big.execute("EXPLAIN QUERY PLAN SELECT * FROM loans WHERE member_id = 5")])
after = timed("With index   ")
print(f"Speed-up: about {before/after:.0f}x faster")
