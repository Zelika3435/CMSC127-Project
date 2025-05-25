-- ============================================================================
-- STUDENT MEMBERSHIP MANAGEMENT SYSTEM - COMPREHENSIVE TEST SQL
-- ============================================================================

-- Use the database
USE student_membership_db;

-- ============================================================================
-- SECTION 1: CLEAN SLATE - DROP AND RECREATE ALL TABLES
-- ============================================================================

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS payment;
DROP TABLE IF EXISTS term;
DROP TABLE IF EXISTS membership;
DROP TABLE IF EXISTS member;
DROP TABLE IF EXISTS student;
DROP TABLE IF EXISTS organization;
SET FOREIGN_KEY_CHECKS = 1;

-- ============================================================================
-- SECTION 2: CREATE TABLES WITH CORRECT SCHEMA
-- ============================================================================

CREATE TABLE organization (
    org_id INT PRIMARY KEY AUTO_INCREMENT,
    org_name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE student (
    student_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    gender VARCHAR(10),
    degree_program VARCHAR(100),
    standing VARCHAR(20)
);

CREATE TABLE member (
    member_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    FOREIGN KEY (student_id) REFERENCES student(student_id) ON DELETE CASCADE
);

CREATE TABLE membership (
    membership_id INT PRIMARY KEY AUTO_INCREMENT,
    batch VARCHAR(20),
    mem_status VARCHAR(20),
    committee VARCHAR(50),
    org_id INT,
    student_id INT,
    FOREIGN KEY (org_id) REFERENCES organization(org_id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES student(student_id) ON DELETE CASCADE
);

CREATE TABLE term (
    term_id INT PRIMARY KEY AUTO_INCREMENT,
    semester VARCHAR(20),
    term_start DATE,
    term_end DATE,
    acad_year VARCHAR(20),
    fee_amount DECIMAL(10,2),
    fee_due DATE,
    membership_id INT,
    FOREIGN KEY (membership_id) REFERENCES membership(membership_id) ON DELETE CASCADE
);

CREATE TABLE payment (
    payment_id INT PRIMARY KEY AUTO_INCREMENT,
    payment_status VARCHAR(20),
    amount DECIMAL(10,2),
    payment_date DATE,
    term_id INT,
    FOREIGN KEY (term_id) REFERENCES term(term_id) ON DELETE CASCADE
);

-- ============================================================================
-- SECTION 3: INSERT COMPREHENSIVE TEST DATA
-- ============================================================================

-- Insert Organizations
INSERT INTO organization (org_name) VALUES 
('Computer Science Society'),
('Mathematics Club'),
('Engineering Society'),
('Debate Club'),
('Photography Club'),
('Student Council'),
('Drama Club'),
('Chess Club');

-- Insert Students (30+ students for comprehensive testing)
INSERT INTO student (first_name, last_name, gender, degree_program, standing) VALUES 
-- CS Students
('John', 'Doe', 'Male', 'BS Computer Science', 'Junior'),
('Jane', 'Smith', 'Female', 'BS Computer Science', 'Senior'),
('Mike', 'Johnson', 'Male', 'BS Computer Science', 'Sophomore'),
('Sarah', 'Williams', 'Female', 'BS Computer Science', 'Freshman'),
('David', 'Brown', 'Male', 'BS Computer Science', 'Junior'),
('Emily', 'Davis', 'Female', 'BS Computer Science', 'Senior'),
('James', 'Wilson', 'Male', 'BS Computer Science', 'Sophomore'),
('Lisa', 'Moore', 'Female', 'BS Computer Science', 'Freshman'),

-- Math Students
('Robert', 'Taylor', 'Male', 'BS Mathematics', 'Junior'),
('Mary', 'Anderson', 'Female', 'BS Mathematics', 'Senior'),
('William', 'Thomas', 'Male', 'BS Mathematics', 'Sophomore'),
('Patricia', 'Jackson', 'Female', 'BS Mathematics', 'Freshman'),
('Christopher', 'White', 'Male', 'BS Mathematics', 'Junior'),
('Jennifer', 'Harris', 'Female', 'BS Mathematics', 'Senior'),

-- Engineering Students
('Michael', 'Martin', 'Male', 'BS Engineering', 'Junior'),
('Linda', 'Thompson', 'Female', 'BS Engineering', 'Senior'),
('Richard', 'Garcia', 'Male', 'BS Engineering', 'Sophomore'),
('Barbara', 'Martinez', 'Female', 'BS Engineering', 'Freshman'),
('Joseph', 'Robinson', 'Male', 'BS Engineering', 'Junior'),
('Susan', 'Clark', 'Female', 'BS Engineering', 'Senior'),

-- Mixed Programs
('Thomas', 'Rodriguez', 'Male', 'BS Information Technology', 'Junior'),
('Dorothy', 'Lewis', 'Female', 'BS Information Systems', 'Senior'),
('Charles', 'Lee', 'Male', 'BS Computer Engineering', 'Sophomore'),
('Helen', 'Walker', 'Female', 'BS Software Engineering', 'Freshman'),
('Daniel', 'Hall', 'Male', 'BS Data Science', 'Junior'),
('Nancy', 'Allen', 'Female', 'BS Cybersecurity', 'Senior'),
('Matthew', 'Young', 'Male', 'BS Game Development', 'Sophomore'),
('Betty', 'Hernandez', 'Female', 'BS Web Development', 'Freshman'),
('Anthony', 'King', 'Male', 'BS Network Administration', 'Junior'),
('Sandra', 'Wright', 'Female', 'BS Database Management', 'Senior');

-- Add all students to member table
INSERT INTO member (student_id) 
SELECT student_id FROM student;

-- Insert Memberships with various scenarios
INSERT INTO membership (batch, mem_status, committee, org_id, student_id) VALUES 
-- Computer Science Society (org_id = 1)
('2023-2024', 'active', 'President', 1, 1),
('2023-2024', 'active', 'Vice President', 1, 2),
('2023-2024', 'active', 'Secretary', 1, 3),
('2023-2024', 'active', 'Treasurer', 1, 4),
('2023-2024', 'active', 'Member', 1, 5),
('2023-2024', 'active', 'Member', 1, 6),
('2023-2024', 'inactive', 'Member', 1, 7),
('2022-2023', 'alumni', 'President', 1, 8),
('2023-2024', 'suspended', 'Member', 1, 21),
('2023-2024', 'active', 'Member', 1, 22),

-- Mathematics Club (org_id = 2)
('2023-2024', 'active', 'President', 2, 9),
('2023-2024', 'active', 'Vice President', 2, 10),
('2023-2024', 'active', 'Secretary', 2, 11),
('2023-2024', 'active', 'Treasurer', 2, 12),
('2023-2024', 'inactive', 'Member', 2, 13),
('2022-2023', 'alumni', 'President', 2, 14),
('2023-2024', 'active', 'Member', 2, 23),

-- Engineering Society (org_id = 3)
('2023-2024', 'active', 'President', 3, 15),
('2023-2024', 'active', 'Vice President', 3, 16),
('2023-2024', 'active', 'Secretary', 3, 17),
('2023-2024', 'suspended', 'Member', 3, 18),
('2023-2024', 'active', 'Member', 3, 19),
('2022-2023', 'alumni', 'Treasurer', 3, 20),
('2023-2024', 'active', 'Member', 3, 24),

-- Student Council (org_id = 6) - Cross-organization memberships
('2023-2024', 'active', 'President', 6, 1),    -- John also in Student Council
('2023-2024', 'active', 'Vice President', 6, 9), -- Robert also in Student Council
('2023-2024', 'active', 'Secretary', 6, 15),   -- Michael also in Student Council

-- Other clubs with fewer members
('2023-2024', 'active', 'President', 4, 25),   -- Debate Club
('2023-2024', 'active', 'Member', 4, 26),
('2023-2024', 'active', 'President', 5, 27),   -- Photography Club
('2023-2024', 'active', 'Member', 5, 28),
('2023-2024', 'active', 'President', 7, 29),   -- Drama Club
('2023-2024', 'active', 'President', 8, 30);   -- Chess Club

-- Insert Terms with various fee scenarios
INSERT INTO term (semester, term_start, term_end, acad_year, fee_amount, fee_due, membership_id) VALUES 
-- 2023-2024 Academic Year Terms
-- 1st Semester
('1st', '2023-08-15', '2023-12-15', '2023-2024', 1000.00, '2023-09-15', 1),  -- John CS
('1st', '2023-08-15', '2023-12-15', '2023-2024', 1000.00, '2023-09-15', 2),  -- Jane CS
('1st', '2023-08-15', '2023-12-15', '2023-2024', 1000.00, '2023-09-15', 3),  -- Mike CS
('1st', '2023-08-15', '2023-12-15', '2023-2024', 1000.00, '2023-09-15', 4),  -- Sarah CS
('1st', '2023-08-15', '2023-12-15', '2023-2024', 1000.00, '2023-09-15', 5),  -- David CS

('1st', '2023-08-15', '2023-12-15', '2023-2024', 800.00, '2023-09-15', 11),  -- Math Club
('1st', '2023-08-15', '2023-12-15', '2023-2024', 800.00, '2023-09-15', 12),
('1st', '2023-08-15', '2023-12-15', '2023-2024', 800.00, '2023-09-15', 13),

('1st', '2023-08-15', '2023-12-15', '2023-2024', 1200.00, '2023-09-15', 18), -- Engineering
('1st', '2023-08-15', '2023-12-15', '2023-2024', 1200.00, '2023-09-15', 19),
('1st', '2023-08-15', '2023-12-15', '2023-2024', 1200.00, '2023-09-15', 20),

-- 2nd Semester
('2nd', '2024-01-15', '2024-05-15', '2023-2024', 1000.00, '2024-02-15', 1),  -- John CS
('2nd', '2024-01-15', '2024-05-15', '2023-2024', 1000.00, '2024-02-15', 2),  -- Jane CS
('2nd', '2024-01-15', '2024-05-15', '2023-2024', 1000.00, '2024-02-15', 3),  -- Mike CS

('2nd', '2024-01-15', '2024-05-15', '2023-2024', 800.00, '2024-02-15', 11),  -- Math Club
('2nd', '2024-01-15', '2024-05-15', '2023-2024', 800.00, '2024-02-15', 12),

-- Previous year terms for alumni testing
('1st', '2022-08-15', '2022-12-15', '2022-2023', 900.00, '2022-09-15', 8),   -- Alumni
('2nd', '2023-01-15', '2023-05-15', '2022-2023', 900.00, '2023-02-15', 8);

-- Insert Payments with various scenarios
INSERT INTO payment (payment_status, amount, payment_date, term_id) VALUES 
-- Full payments (on time)
('completed', 1000.00, '2023-09-10', 1),  -- John paid full, on time
('completed', 1000.00, '2023-09-12', 2),  -- Jane paid full, on time

-- Partial payments
('partial', 500.00, '2023-09-14', 3),     -- Mike partial payment
('partial', 300.00, '2023-10-01', 3),     -- Mike second payment

-- Late payments
('completed', 1000.00, '2023-09-20', 4),  -- Sarah paid full, late
('completed', 500.00, '2023-09-25', 5),   -- David partial, late

-- Math club payments
('completed', 800.00, '2023-09-08', 6),   -- Math club on time
('partial', 400.00, '2023-09-16', 7),     -- Math club partial

-- Engineering payments (higher fees)
('completed', 1200.00, '2023-09-05', 9),  -- Engineering full
('partial', 600.00, '2023-09-18', 10),    -- Engineering partial

-- Second semester payments
('completed', 1000.00, '2024-02-10', 12), -- John 2nd sem
('partial', 500.00, '2024-02-20', 13),    -- Jane 2nd sem partial

-- Alumni payments (previous years)
('completed', 900.00, '2022-09-10', 16),  -- Alumni 1st sem
('completed', 900.00, '2023-02-10', 17);  -- Alumni 2nd sem

-- ============================================================================
-- SECTION 4: COMPREHENSIVE FUNCTIONALITY TESTS
-- ============================================================================

-- Test 1: Basic Student Operations
SELECT '=== TEST 1: ALL STUDENTS ===' AS test_section;
SELECT student_id, first_name, last_name, gender, degree_program, standing 
FROM student 
ORDER BY last_name, first_name;

-- Test 2: All Organizations
SELECT '=== TEST 2: ALL ORGANIZATIONS ===' AS test_section;
SELECT org_id, org_name FROM organization ORDER BY org_name;

-- Test 3: Members by Organization (CS Society)
SELECT '=== TEST 3: COMPUTER SCIENCE SOCIETY MEMBERS ===' AS test_section;
SELECT s.student_id, s.first_name, s.last_name, 
       m.mem_status, m.batch, m.committee, org.org_name, m.membership_id,
       s.gender, s.degree_program
FROM student s
JOIN member mb ON s.student_id = mb.student_id
JOIN membership m ON mb.student_id = m.student_id
JOIN organization org ON m.org_id = org.org_id
WHERE org.org_id = 1
ORDER BY s.last_name, s.first_name;

-- Test 4: All Members Across Organizations
SELECT '=== TEST 4: ALL MEMBERS BY ORGANIZATION ===' AS test_section;
SELECT s.student_id, s.first_name, s.last_name, 
       m.mem_status, m.batch, m.committee, org.org_name, m.membership_id,
       s.gender, s.degree_program
FROM student s
JOIN member mb ON s.student_id = mb.student_id
JOIN membership m ON mb.student_id = m.student_id
JOIN organization org ON m.org_id = org.org_id
ORDER BY org.org_name, s.last_name;

-- Test 5: Members with Unpaid Fees (CS Society, 1st Semester 2023-2024)
SELECT '=== TEST 5: MEMBERS WITH UNPAID FEES (CS Society, 1st Sem 2023-2024) ===' AS test_section;
SELECT s.student_id, s.first_name, s.last_name, 
       t.fee_amount, COALESCE(SUM(p.amount), 0) as total_paid,
       (t.fee_amount - COALESCE(SUM(p.amount), 0)) as balance
FROM student s
JOIN member mb ON s.student_id = mb.student_id
JOIN membership m ON mb.student_id = m.student_id
JOIN organization org ON m.org_id = org.org_id
JOIN term t ON m.membership_id = t.membership_id
LEFT JOIN payment p ON t.term_id = p.term_id
WHERE org.org_id = 1 AND t.semester = '1st' AND t.acad_year = '2023-2024'
GROUP BY s.student_id, t.term_id
HAVING balance > 0;

-- Test 6: Member Unpaid Fees (John Doe - student_id = 1)
SELECT '=== TEST 6: JOHN DOE UNPAID FEES ===' AS test_section;
SELECT org.org_name, t.semester, t.acad_year,
       t.fee_amount, COALESCE(SUM(p.amount), 0) as total_paid,
       (t.fee_amount - COALESCE(SUM(p.amount), 0)) as balance
FROM student s
JOIN member mb ON s.student_id = mb.student_id
JOIN membership m ON mb.student_id = m.student_id
JOIN organization org ON m.org_id = org.org_id
JOIN term t ON m.membership_id = t.membership_id
LEFT JOIN payment p ON t.term_id = p.term_id
WHERE s.student_id = 1
GROUP BY org.org_id, t.term_id
HAVING balance > 0;

-- Test 7: Executive Committee (CS Society, 2023-2024)
SELECT '=== TEST 7: CS SOCIETY EXECUTIVE COMMITTEE 2023-2024 ===' AS test_section;
SELECT s.student_id, s.first_name, s.last_name, m.committee
FROM student s
JOIN member mb ON s.student_id = mb.student_id
JOIN membership m ON mb.student_id = m.student_id
JOIN organization org ON m.org_id = org.org_id
WHERE org.org_id = 1 AND m.batch = '2023-2024' 
AND m.committee IN ('President', 'Vice President', 'Secretary', 'Treasurer');

-- Test 8: Role History (Presidents of CS Society)
SELECT '=== TEST 8: PRESIDENT HISTORY - CS SOCIETY ===' AS test_section;
SELECT s.student_id, s.first_name, s.last_name, m.batch
FROM student s
JOIN member mb ON s.student_id = mb.student_id
JOIN membership m ON mb.student_id = m.student_id
JOIN organization org ON m.org_id = org.org_id
WHERE org.org_id = 1 AND m.committee = 'President'
ORDER BY m.batch DESC;

-- Test 9: Late Payments (CS Society, 1st Semester 2023-2024)
SELECT '=== TEST 9: LATE PAYMENTS - CS SOCIETY 1ST SEM 2023-2024 ===' AS test_section;
SELECT s.student_id, s.first_name, s.last_name,
       p.payment_date, t.fee_due, p.amount
FROM student s
JOIN member mb ON s.student_id = mb.student_id
JOIN membership m ON mb.student_id = m.student_id
JOIN organization org ON m.org_id = org.org_id
JOIN term t ON m.membership_id = t.membership_id
JOIN payment p ON t.term_id = p.term_id
WHERE org.org_id = 1 AND t.semester = '1st' AND t.acad_year = '2023-2024'
AND p.payment_date > t.fee_due;

-- Test 10: Membership Status Percentage (CS Society, last 2 academic years)
SELECT '=== TEST 10: MEMBERSHIP STATUS PERCENTAGE - CS SOCIETY ===' AS test_section;
SELECT 
    COUNT(CASE WHEN m.mem_status = 'active' THEN 1 END) as active_count,
    COUNT(CASE WHEN m.mem_status = 'inactive' THEN 1 END) as inactive_count,
    COUNT(CASE WHEN m.mem_status = 'suspended' THEN 1 END) as suspended_count,
    COUNT(CASE WHEN m.mem_status = 'alumni' THEN 1 END) as alumni_count,
    COUNT(*) as total_count,
    ROUND((COUNT(CASE WHEN m.mem_status = 'active' THEN 1 END) / COUNT(*)) * 100, 2) as active_percentage,
    ROUND((COUNT(CASE WHEN m.mem_status = 'inactive' THEN 1 END) / COUNT(*)) * 100, 2) as inactive_percentage
FROM membership m
JOIN organization org ON m.org_id = org.org_id
WHERE org.org_id = 1;

-- Test 11: Alumni Members (CS Society, as of 2024-01-01)
SELECT '=== TEST 11: ALUMNI MEMBERS - CS SOCIETY ===' AS test_section;
SELECT s.student_id, s.first_name, s.last_name, m.batch
FROM student s
JOIN member mb ON s.student_id = mb.student_id
JOIN membership m ON mb.student_id = m.student_id
JOIN organization org ON m.org_id = org.org_id
WHERE org.org_id = 1 AND m.mem_status = 'alumni'
AND m.batch <= '2023-2024';

-- Test 12: Organization Financial Status (CS Society, as of 2024-05-01)
SELECT '=== TEST 12: CS SOCIETY FINANCIAL STATUS ===' AS test_section;
SELECT 
    org.org_name,
    SUM(t.fee_amount) as total_fees,
    COALESCE(SUM(p.amount), 0) as total_paid,
    SUM(t.fee_amount) - COALESCE(SUM(p.amount), 0) as total_unpaid
FROM organization org
JOIN membership m ON org.org_id = m.org_id
JOIN term t ON m.membership_id = t.membership_id
LEFT JOIN payment p ON t.term_id = p.term_id
WHERE org.org_id = 1 AND t.term_start <= '2024-05-01'
GROUP BY org.org_id, org.org_name;

-- Test 13: Highest Debt Members (CS Society, 1st Semester 2023-2024)
SELECT '=== TEST 13: HIGHEST DEBT MEMBERS - CS SOCIETY 1ST SEM 2023-2024 ===' AS test_section;
SELECT s.student_id, s.first_name, s.last_name,
       t.fee_amount, COALESCE(SUM(p.amount), 0) as total_paid,
       (t.fee_amount - COALESCE(SUM(p.amount), 0)) as balance
FROM student s
JOIN member mb ON s.student_id = mb.student_id
JOIN membership m ON mb.student_id = m.student_id
JOIN organization org ON m.org_id = org.org_id
JOIN term t ON m.membership_id = t.membership_id
LEFT JOIN payment p ON t.term_id = p.term_id
WHERE org.org_id = 1 AND t.semester = '1st' AND t.acad_year = '2023-2024'
GROUP BY s.student_id, t.term_id
HAVING balance > 0
ORDER BY balance DESC;

-- Test 14: Term Balances (All Terms)
SELECT '=== TEST 14: ALL TERM BALANCES ===' AS test_section;
SELECT t.term_id, t.semester, t.acad_year, t.fee_amount,
       COALESCE(SUM(p.amount), 0) AS total_paid,
       (t.fee_amount - COALESCE(SUM(p.amount), 0)) AS balance,
       org.org_name, s.first_name, s.last_name
FROM term t
LEFT JOIN payment p ON t.term_id = p.term_id
JOIN membership m ON t.membership_id = m.membership_id
JOIN organization org ON m.org_id = org.org_id
JOIN student s ON m.student_id = s.student_id
GROUP BY t.term_id
ORDER BY t.acad_year DESC, t.semester, org.org_name;

-- Test 15: Financial Summary by Organization
SELECT '=== TEST 15: FINANCIAL SUMMARY BY ORGANIZATION ===' AS test_section;
SELECT org.org_name,
       SUM(t.fee_amount) AS total_fees,
       COALESCE(SUM(p.amount), 0) AS total_collected,
       SUM(t.fee_amount) - COALESCE(SUM(p.amount), 0) AS total_balance 
FROM organization org
JOIN membership m ON org.org_id = m.org_id
JOIN term t ON m.membership_id = t.membership_id
LEFT JOIN (
    SELECT term_id, SUM(amount) AS amount
    FROM payment
    GROUP BY term_id
) p ON t.term_id = p.term_id
GROUP BY org.org_name
ORDER BY total_balance DESC;

-- Test 16: Cross-Organization Memberships
SELECT '=== TEST 16: STUDENTS WITH MULTIPLE ORGANIZATION MEMBERSHIPS ===' AS test_section;
SELECT s.student_id, s.first_name, s.last_name,
       COUNT(DISTINCT m.org_id) as org_count,
       GROUP_CONCAT(DISTINCT org.org_name SEPARATOR ', ') as organizations
FROM student s
JOIN member mb ON s.student_id = mb.student_id
JOIN membership m ON mb.student_id = m.student_id
JOIN organization org ON m.org_id = org.org_id
GROUP BY s.student_id
HAVING org_count > 1
ORDER BY org_count DESC;

-- Test 17: Payment Summary by Status
SELECT '=== TEST 17: PAYMENT SUMMARY BY STATUS ===' AS test_section;
SELECT payment_status, 
       COUNT(*) as payment_count,
       SUM(amount) as total_amount,
       AVG(amount) as average_amount,
       MIN(amount) as min_amount,
       MAX(amount) as max_amount
FROM payment
GROUP BY payment_status
ORDER BY total_amount DESC;

-- ============================================================================
-- SECTION 5: DATA INTEGRITY VERIFICATION
-- ============================================================================

SELECT '=== DATA INTEGRITY VERIFICATION ===' AS test_section;

-- Check for orphaned records
SELECT 'Orphaned members (students not in student table):' as check_type, COUNT(*) as count
FROM member m LEFT JOIN student s ON m.student_id = s.student_id WHERE s.student_id IS NULL
UNION ALL
SELECT 'Orphaned memberships (invalid student_id):', COUNT(*)
FROM membership m LEFT JOIN student s ON m.student_id = s.student_id WHERE s.student_id IS NULL
UNION ALL
SELECT 'Orphaned memberships (invalid org_id):', COUNT(*)
FROM membership m LEFT JOIN organization o ON m.org_id = o.org_id WHERE o.org_id IS NULL
UNION ALL
SELECT 'Orphaned terms (invalid membership_id):', COUNT(*)
FROM term t LEFT JOIN membership m ON t.membership_id = m.membership_id WHERE m.membership_id IS NULL
UNION ALL
SELECT 'Orphaned payments (invalid term_id):', COUNT(*)
FROM payment p LEFT JOIN term t ON p.term_id = t.term_id WHERE t.term_id IS NULL;

-- Summary statistics
SELECT '=== SUMMARY STATISTICS ===' AS test_section;
SELECT 'Total Students' as metric, COUNT(*) as count FROM student
UNION ALL
SELECT 'Total Organizations', COUNT(*) FROM organization
UNION ALL
SELECT 'Total Members', COUNT(*) FROM member
UNION ALL
SELECT 'Total Memberships', COUNT(*) FROM membership
UNION ALL
SELECT 'Total Terms', COUNT(*) FROM term
UNION ALL
SELECT 'Total Payments', COUNT(*) FROM payment;

-- ============================================================================
-- END OF COMPREHENSIVE TEST
-- ============================================================================

SELECT '=== COMPREHENSIVE TEST COMPLETED ===' AS test_section;