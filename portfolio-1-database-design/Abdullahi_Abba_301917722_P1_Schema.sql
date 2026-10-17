-- Portfolio 1: Database Design and Modelling
-- Case study: Campus Library Management System (simulated organisation)
-- Student: Abba Abdullahi (301917722) | MIT 8103 Advanced Database Systems
-- Engine: SQLite 3 (run with PRAGMA foreign_keys = ON)

PRAGMA foreign_keys = ON;

CREATE TABLE categories (
    category_id INTEGER PRIMARY KEY,
    name        TEXT NOT NULL UNIQUE
);

CREATE TABLE books (
    book_id          INTEGER PRIMARY KEY,
    isbn             TEXT NOT NULL UNIQUE,
    title            TEXT NOT NULL,
    author           TEXT NOT NULL,
    category_id      INTEGER NOT NULL REFERENCES categories(category_id),
    total_copies     INTEGER NOT NULL CHECK (total_copies >= 1),
    available_copies INTEGER NOT NULL CHECK (available_copies >= 0),
    CHECK (available_copies <= total_copies)
);

CREATE TABLE members (
    member_id   INTEGER PRIMARY KEY,
    full_name   TEXT NOT NULL,
    email       TEXT NOT NULL UNIQUE,
    joined_date TEXT NOT NULL
);

CREATE TABLE loans (
    loan_id     INTEGER PRIMARY KEY,
    member_id   INTEGER NOT NULL REFERENCES members(member_id),
    book_id     INTEGER NOT NULL REFERENCES books(book_id),
    borrow_date TEXT NOT NULL,
    due_date    TEXT NOT NULL,
    return_date TEXT,                       -- NULL = still borrowed
    CHECK (due_date >= borrow_date)
);

CREATE TABLE fines (
    fine_id INTEGER PRIMARY KEY,
    loan_id INTEGER NOT NULL UNIQUE REFERENCES loans(loan_id),
    amount  INTEGER NOT NULL CHECK (amount > 0),   -- Naira
    paid    INTEGER NOT NULL DEFAULT 0 CHECK (paid IN (0,1))
);

-- ---------- Sample (simulated) data ----------
INSERT INTO categories VALUES (1,'Computing'),(2,'Fiction'),(3,'Science'),(4,'History'),(5,'Business');

INSERT INTO books(book_id,isbn,title,author,category_id,total_copies,available_copies) VALUES
 (1,'9780131103627','The C Programming Language','Brian Kernighan',1,3,3),
 (2,'9780262033848','Introduction to Algorithms','Thomas Cormen',1,2,2),
 (3,'9781449373320','Designing Data-Intensive Applications','Martin Kleppmann',1,2,2),
 (4,'9780141439518','Pride and Prejudice','Jane Austen',2,4,4),
 (5,'9780061120084','To Kill a Mockingbird','Harper Lee',2,2,2),
 (6,'9780553380163','A Brief History of Time','Stephen Hawking',3,2,2),
 (7,'9780385537858','Half of a Yellow Sun','Chimamanda Adichie',2,3,3),
 (8,'9780143127741','Sapiens','Yuval Noah Harari',4,2,2),
 (9,'9780385474542','Things Fall Apart','Chinua Achebe',2,3,3),
 (10,'9781591846444','Zero to One','Peter Thiel',5,1,1);

INSERT INTO members VALUES
 (1,'Aisha Bello','aisha.bello@example.com','2026-01-10'),
 (2,'Chinedu Okafor','chinedu.okafor@example.com','2026-01-15'),
 (3,'Fatima Yusuf','fatima.yusuf@example.com','2026-02-01'),
 (4,'Emeka Nwosu','emeka.nwosu@example.com','2026-02-20'),
 (5,'Zainab Musa','zainab.musa@example.com','2026-03-05'),
 (6,'Tunde Adeyemi','tunde.adeyemi@example.com','2026-03-18');

INSERT INTO loans(loan_id,member_id,book_id,borrow_date,due_date,return_date) VALUES
 (1,1,1,'2026-09-01','2026-09-15','2026-09-14'),
 (2,1,3,'2026-09-02','2026-09-16','2026-09-20'),
 (3,2,2,'2026-09-05','2026-09-19','2026-09-18'),
 (4,2,4,'2026-09-10','2026-09-24','2026-10-01'),
 (5,3,6,'2026-09-12','2026-09-26','2026-09-25'),
 (6,3,7,'2026-09-15','2026-09-29',NULL),
 (7,4,3,'2026-09-20','2026-10-04','2026-10-03'),
 (8,4,8,'2026-10-01','2026-10-15',NULL),
 (9,5,9,'2026-10-05','2026-10-19',NULL),
 (10,5,1,'2026-10-06','2026-10-20',NULL),
 (11,6,10,'2026-10-08','2026-10-22',NULL),
 (12,1,4,'2026-10-10','2026-10-24',NULL);

-- Keep available_copies consistent with books that are still out
UPDATE books SET available_copies = total_copies -
   (SELECT COUNT(*) FROM loans WHERE loans.book_id = books.book_id AND return_date IS NULL);

-- Fines: N50 per day late, only for books returned after the due date
INSERT INTO fines(loan_id,amount)
SELECT loan_id, 50 * CAST(julianday(return_date) - julianday(due_date) AS INTEGER)
FROM loans WHERE return_date > due_date;
