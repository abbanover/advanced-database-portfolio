"""Portfolio 5: Distributed database ideas on the library case study (simulated on one computer).
Shows: replication (primary -> replica), eventual consistency, failover, and sharding.
Run:  python3 Abdullahi_Abba_301917722_P5_Distributed.py
"""
import glob, os, sqlite3, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
SCHEMA = open(glob.glob(os.path.join(HERE, "..", "portfolio-1-database-design", "*_P1_Schema.sql"))[0]).read()
tmp = tempfile.mkdtemp()

# ---------- 1. Replication ----------
primary = sqlite3.connect(os.path.join(tmp, "primary.db")); primary.executescript(SCHEMA); primary.commit()
def sync_replica():
    rep = sqlite3.connect(os.path.join(tmp, "replica.db"))
    primary.backup(rep)           # copy primary -> replica
    return rep
replica = sync_replica()
n = lambda c: c.execute("SELECT COUNT(*) FROM loans").fetchone()[0]

print("=== 1. Replication (primary + read replica) ===")
print("After first sync: primary loans =", n(primary), "| replica loans =", n(replica))
primary.execute("INSERT INTO loans(member_id,book_id,borrow_date,due_date) VALUES (2,5,'2026-10-17','2026-10-31')")
primary.commit()
print("New loan written to primary: primary =", n(primary), "| replica =", n(replica),
      "-> replica is briefly behind (eventual consistency)")
replica.close(); replica = sync_replica()
print("After replication catches up: replica =", n(replica), "-> consistent again")

print("\n=== 2. Availability / failover ===")
print("Primary goes DOWN. Readers are sent to the replica instead:")
print("Replica still answers:", replica.execute("SELECT title FROM books WHERE book_id=1").fetchone()[0])
print("(Writes pause until a replica is promoted to primary - consistency is chosen over write availability.)")

# ---------- 3. Sharding ----------
print("\n=== 3. Sharding loans by member_id (2 shards) ===")
shards = [sqlite3.connect(os.path.join(tmp, f"shard{i}.db")) for i in range(2)]
for s in shards:
    s.execute("""CREATE TABLE loans(loan_id INTEGER, member_id INTEGER, book_id INTEGER,
                 borrow_date TEXT, due_date TEXT, return_date TEXT)""")
shard_of = lambda member_id: member_id % 2          # shard key rule
for row in primary.execute("SELECT * FROM loans"):
    shards[shard_of(row[1])].execute("INSERT INTO loans VALUES (?,?,?,?,?,?)", row)
for i, s in enumerate(shards):
    ids = sorted({r[0] for r in s.execute("SELECT member_id FROM loans")})
    print(f"Shard {i}: {s.execute('SELECT COUNT(*) FROM loans').fetchone()[0]} loans, members {ids}")
print("Query for member 3 goes only to shard", shard_of(3), "->",
      shards[shard_of(3)].execute("SELECT COUNT(*) FROM loans WHERE member_id=3").fetchone()[0], "loans")
total = sum(s.execute("SELECT COUNT(*) FROM loans").fetchone()[0] for s in shards)
print("Total loans across all shards (scatter-gather query):", total)
