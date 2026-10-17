-- Portfolio 2: Query Processing and Optimisation
-- Reference date for "today" is fixed at 2026-10-17 so results are repeatable.

-- Q1: Books that are overdue right now (JOIN of 3 tables)
SELECT m.full_name, b.title, l.due_date,
       CAST(julianday('2026-10-17') - julianday(l.due_date) AS INTEGER) AS days_overdue
FROM loans l
JOIN members m ON m.member_id = l.member_id
JOIN books   b ON b.book_id   = l.book_id
WHERE l.return_date IS NULL AND l.due_date < '2026-10-17'
ORDER BY days_overdue DESC;

-- Q2: Three most borrowed books (GROUP BY + aggregate)
SELECT b.title, COUNT(*) AS times_borrowed
FROM loans l JOIN books b ON b.book_id = l.book_id
GROUP BY b.book_id
ORDER BY times_borrowed DESC, b.title
LIMIT 3;

-- Q3: Total unpaid fines per member
SELECT m.full_name, SUM(f.amount) AS total_fines_naira
FROM fines f
JOIN loans l   ON l.loan_id = f.loan_id
JOIN members m ON m.member_id = l.member_id
WHERE f.paid = 0
GROUP BY m.member_id;

-- Q4: Loan history of one member (this is the query we optimise with an index)
SELECT l.loan_id, l.book_id, l.borrow_date, l.due_date, l.return_date
FROM loans l
WHERE l.member_id = 2;

-- ==INDEXES==
CREATE INDEX idx_loans_member_id ON loans(member_id);
CREATE INDEX idx_loans_book_id   ON loans(book_id);
