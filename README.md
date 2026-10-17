MIT 8103 ADVANCED DATABASE SYSTEMS - PORTFOLIO README
Student : Abba Muhammad Abdullahi
ID      : 301917722
Email   : a.abdullahi7722@miva.edu.ng
Case study: Campus Library Management System (simulated organisation, sample data)
GitHub  : https://github.com/abbanover/advanced-database-portfolio

FILES IN THE ZIP
Abdullahi_Abba_301917722_Documentation.docx   2-page summary, reflection, AI declaration, references
Abdullahi_Abba_301917722_P1_Schema.sql        Portfolio 1: tables, keys, constraints, sample data
Abdullahi_Abba_301917722_P1_ERD.png           Portfolio 1: ER diagram
Abdullahi_Abba_301917722_P2_Queries.sql       Portfolio 2: 4 queries + index statements
Abdullahi_Abba_301917722_P2_Performance.py    Portfolio 2: runs queries, execution plans, timing test
Abdullahi_Abba_301917722_P3_Transactions.py   Portfolio 3: commit, rollback, concurrency demo
Abdullahi_Abba_301917722_P4_NoSQL.py          Portfolio 4: builds JSON documents and queries them
Abdullahi_Abba_301917722_P4_Documents.json    Portfolio 4: the generated document collection
Abdullahi_Abba_301917722_P5_Distributed.py    Portfolio 5: replication, failover, sharding demo
Abdullahi_Abba_301917722_Evidence.txt         Saved output of all scripts (execution plans, results)
Abdullahi_Abba_301917722_P2_Screenshot.png    Screenshot of P2 output (run on my MacBook)
Abdullahi_Abba_301917722_P3_Screenshot.png    Screenshot of P3 output
Abdullahi_Abba_301917722_P4_Screenshot.png    Screenshot of P4 output
Abdullahi_Abba_301917722_P5_Screenshot.png    Screenshot of P5 output

HOW TO RUN (needs only Python 3, no installs; SQLite is built in)
1. Unzip the folder.
2. Open a terminal in the folder.
3. Run each script, for example:
      python3 Abdullahi_Abba_301917722_P2_Performance.py
      python3 Abdullahi_Abba_301917722_P3_Transactions.py
      python3 Abdullahi_Abba_301917722_P4_NoSQL.py
      python3 Abdullahi_Abba_301917722_P5_Distributed.py
   Each script builds a fresh database from the P1 schema file, so P1_Schema.sql must stay in the same folder.

HOW EACH PORTFOLIO WAS IMPLEMENTED AND TESTED
P1  Designed 5 tables in 3NF. Tested that bad data is rejected (missing member -> FOREIGN KEY error;
    copies above total -> CHECK error). See Evidence.txt.
P2  Ran 4 queries, compared EXPLAIN QUERY PLAN before/after indexes (SCAN -> SEARCH), and timed
    300 lookups on 100,000 loans (about 37x faster with the index on my MacBook; exact timing varies by computer).
P3  Tested COMMIT (loan added), ROLLBACK (no copies left, nothing saved) and two users at once
    (no dirty read, write lock prevents lost update).
P4  Converted the relational data to JSON documents with embedded loans and ran 3 document-style
    queries plus a key-value example.
P5  Simulated a primary/replica copy (eventual consistency), failover reads, and 2-shard split by
    member_id. Cloud deployment is a written design only (not deployed).

SAMPLE DATA: all members, books and loans are made up for this exercise.
AI USE: Claude (Anthropic) helped draft the scripts and documents; I ran, checked and can explain all of it.
