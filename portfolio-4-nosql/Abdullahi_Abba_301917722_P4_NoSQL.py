"""Portfolio 4: NoSQL (document model) for the same library case study.
Builds JSON documents from the relational data and runs document-style queries.
Run:  python3 Abdullahi_Abba_301917722_P4_NoSQL.py

Equivalent MongoDB shell queries (reference only - not executed in this submission):
  db.books.find({category:"Computing", "copies.available":{$gt:0}})
  db.books.aggregate([{$project:{title:1, n:{$size:"$loans"}}},{$sort:{n:-1}}])
"""
import glob, json, os, sqlite3
HERE = os.path.dirname(os.path.abspath(__file__))
SCHEMA = open(glob.glob(os.path.join(HERE, "..", "portfolio-1-database-design", "*_P1_Schema.sql"))[0]).read()
db = sqlite3.connect(":memory:"); db.row_factory = sqlite3.Row
db.executescript(SCHEMA)

# One document per book; loan history is EMBEDDED (no joins needed to read a book's history)
books = []
for b in db.execute("SELECT b.*, c.name AS category FROM books b JOIN categories c USING(category_id)"):
    loans = [dict(member=r["full_name"], borrowed=r["borrow_date"], due=r["due_date"], returned=r["return_date"])
             for r in db.execute("""SELECT m.full_name, l.borrow_date, l.due_date, l.return_date
                                    FROM loans l JOIN members m USING(member_id)
                                    WHERE l.book_id=? ORDER BY l.loan_id""", (b["book_id"],))]
    books.append({"_id": b["book_id"], "isbn": b["isbn"], "title": b["title"], "author": b["author"],
                  "category": b["category"],
                  "copies": {"total": b["total_copies"], "available": b["available_copies"]},
                  "loans": loans})

out = os.path.join(HERE, [f for f in os.listdir(HERE) if f.endswith("_P4_Documents.json")][0]
                   if any(f.endswith("_P4_Documents.json") for f in os.listdir(HERE))
                   else "Abdullahi_Abba_301917722_P4_Documents.json")
json.dump(books, open(out, "w"), indent=2)
print(f"Saved {len(books)} book documents to {os.path.basename(out)}")
print("\nSample document (book 3):")
print(json.dumps(books[2], indent=2))

print("\n=== Query 1: Computing books with copies available ===")
for d in books:
    if d["category"] == "Computing" and d["copies"]["available"] > 0:
        print(d["title"], "| available:", d["copies"]["available"])

print("\n=== Query 2: Books ever borrowed by Chinedu Okafor ===")
for d in books:
    if any(l["member"] == "Chinedu Okafor" for l in d["loans"]):
        print(d["title"])

print("\n=== Query 3: Loan count per book (aggregation) ===")
for d in sorted(books, key=lambda d: -len(d["loans"]))[:3]:
    print(d["title"], "->", len(d["loans"]), "loans")

print("\n=== Key-value example (fast availability check, like Redis) ===")
kv = {f"book:{d['_id']}:available": d["copies"]["available"] for d in books}
print("GET book:4:available ->", kv["book:4:available"])
