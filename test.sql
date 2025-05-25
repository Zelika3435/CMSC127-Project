-- ============================================================================
-- STUDENT MEMBERSHIP MANAGEMENT SYSTEM - COMPLETE REFRESH WITH PROPER FEE LOGIC
-- ============================================================================

-- ============================================================================
-- SECTION 1: COMPLETE DATABASE REFRESH
-- ============================================================================

-- Drop the entire database and recreate it
DROP DATABASE IF EXISTS student_membership_db;
CREATE DATABASE student_membership_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE student_membership_db;

-- ============================================================================
-- SECTION 2: CREATE TABLES WITH PROPER SCHEMA
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
    org_id INT,
    FOREIGN KEY (org_id) REFERENCES organization(org_id) ON DELETE CASCADE
);

CREATE TABLE has_membership (
    student_id INT,
    membership_id INT,
    PRIMARY KEY (student_id, membership_id),
    FOREIGN KEY (student_id) REFERENCES student(student_id) ON DELETE CASCADE,
    FOREIGN KEY (membership_id) REFERENCES membership(membership_id) ON DELETE CASCADE
);

CREATE TABLE term (
    term_id INT PRIMARY KEY AUTO_INCREMENT,
    semester VARCHAR(20),
    payment_status VARCHAR(20),
    role VARCHAR(50),
    term_start DATE,
    term_end DATE,
    acad_year VARCHAR(20),
    fee_amount DECIMAL(10,2),
    fee_due DATE,
    balance DECIMAL(10,2),
    membership_id INT,
    FOREIGN KEY (membership_id) REFERENCES membership(membership_id) ON DELETE CASCADE
);

CREATE TABLE payment (
    payment_id INT PRIMARY KEY AUTO_INCREMENT,
    amount DECIMAL(10,2),
    payment_date DATE,
    term_id INT,
    FOREIGN KEY (term_id) REFERENCES term(term_id) ON DELETE CASCADE
);

-- ============================================================================
-- SECTION 3: INSERT ORGANIZATIONS AND STUDENTS
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

-- Insert Students (mix of current and former students)
INSERT INTO student (first_name, last_name, gender, degree_program, standing) VALUES 
-- Current active students
('John', 'Doe', 'Male', 'BS Computer Science', 'Junior'),
('Jane', 'Smith', 'Female', 'BS Computer Science', 'Senior'),
('Mike', 'Johnson', 'Male', 'BS Computer Science', 'Sophomore'),
('Sarah', 'Williams', 'Female', 'BS Computer Science', 'Freshman'),
('David', 'Brown', 'Male', 'BS Computer Science', 'Junior'),
('Emily', 'Davis', 'Female', 'BS Computer Science', 'Senior'),
('James', 'Wilson', 'Male', 'BS Computer Science', 'Sophomore'),
('Lisa', 'Moore', 'Female', 'BS Computer Science', 'Freshman'),

-- Math students
('Robert', 'Taylor', 'Male', 'BS Mathematics', 'Junior'),
('Mary', 'Anderson', 'Female', 'BS Mathematics', 'Senior'),
('William', 'Thomas', 'Male', 'BS Mathematics', 'Sophomore'),
('Patricia', 'Jackson', 'Female', 'BS Mathematics', 'Freshman'),
('Christopher', 'White', 'Male', 'BS Mathematics', 'Junior'),
('Jennifer', 'Harris', 'Female', 'BS Mathematics', 'Senior'),

-- Engineering students
('Michael', 'Martin', 'Male', 'BS Engineering', 'Junior'),
('Linda', 'Thompson', 'Female', 'BS Engineering', 'Senior'),
('Richard', 'Garcia', 'Male', 'BS Engineering', 'Sophomore'),
('Barbara', 'Martinez', 'Female', 'BS Engineering', 'Freshman'),
('Joseph', 'Robinson', 'Male', 'BS Engineering', 'Junior'),
('Susan', 'Clark', 'Female', 'BS Engineering', 'Senior'),

-- Former students (now alumni or expelled)
('Thomas', 'Rodriguez', 'Male', 'BS Information Technology', 'Graduate'),
('Dorothy', 'Lewis', 'Female', 'BS Information Systems', 'Graduate'),
('Charles', 'Lee', 'Male', 'BS Computer Engineering', 'Graduate'),
('Helen', 'Walker', 'Female', 'BS Software Engineering', 'Graduate'),

-- More current students for testing
('Daniel', 'Hall', 'Male', 'BS Data Science', 'Junior'),
('Nancy', 'Allen', 'Female', 'BS Cybersecurity', 'Senior'),
('Matthew', 'Young', 'Male', 'BS Game Development', 'Sophomore'),
('Betty', 'Hernandez', 'Female', 'BS Web Development', 'Freshman'),
('Anthony', 'King', 'Male', 'BS Network Administration', 'Junior'),
('Sandra', 'Wright', 'Female', 'BS Database Management', 'Senior');

-- Add all students to member table
INSERT INTO member (student_id) 
SELECT student_id FROM student;

-- ============================================================================
-- SECTION 4: INSERT MEMBERSHIPS WITH VARIOUS STATUSES
-- ============================================================================

-- First insert memberships
INSERT INTO membership (batch, mem_status, org_id) VALUES 
-- Computer Science Society
('2023-2024', 'active', 1),
('2023-2024', 'active', 1),
('2023-2024', 'active', 1),
('2023-2024', 'active', 1),
('2023-2024', 'active', 1),
('2023-2024', 'active', 1),
('2023-2024', 'active', 1),
('2023-2024', 'active', 1),
('2023-2024', 'inactive', 1),
('2023-2024', 'inactive', 1),
('2023-2024', 'expelled', 1),
('2022-2023', 'alumni', 1),
('2021-2022', 'alumni', 1),

-- Mathematics Club
('2023-2024', 'active', 2),
('2023-2024', 'active', 2),
('2023-2024', 'active', 2),
('2023-2024', 'active', 2),
('2023-2024', 'active', 2),
('2023-2024', 'active', 2),
('2023-2024', 'inactive', 2),
('2020-2021', 'alumni', 2),

-- Engineering Society
('2023-2024', 'active', 3),
('2023-2024', 'active', 3),
('2023-2024', 'active', 3),
('2023-2024', 'active', 3),
('2023-2024', 'active', 3),
('2023-2024', 'active', 3),
('2023-2024', 'inactive', 3),
('2023-2024', 'expelled', 3),
('2019-2020', 'alumni', 3),

-- Student Council
('2023-2024', 'active', 6),
('2023-2024', 'active', 6),
('2023-2024', 'active', 6),

-- Debate Club
('2023-2024', 'active', 4),
('2023-2024', 'active', 4),
('2023-2024', 'inactive', 4),

-- Photography Club
('2023-2024', 'active', 5),
('2023-2024', 'active', 5);

-- Then create the has_membership relationships
INSERT INTO has_membership (student_id, membership_id) VALUES
-- Computer Science Society
(1, 1),  -- John Doe
(2, 2),  -- Jane Smith
(3, 3),  -- Mike Johnson
(4, 4),  -- Sarah Williams
(5, 5),  -- David Brown
(6, 6),  -- Emily Davis
(25, 7), -- Daniel Hall
(26, 8), -- Nancy Allen
(7, 9),  -- James Wilson (inactive)
(8, 10), -- Lisa Moore (inactive)
(27, 11), -- Matthew Young (expelled)
(21, 12), -- Thomas Rodriguez (alumni)
(22, 13), -- Dorothy Lewis (alumni)

-- Mathematics Club
(9, 14),  -- Robert Taylor
(10, 15), -- Mary Anderson
(11, 16), -- William Thomas
(12, 17), -- Patricia Jackson
(13, 18), -- Christopher White
(14, 19), -- Jennifer Harris
(28, 20), -- Betty Hernandez (inactive)
(23, 21), -- Charles Lee (alumni)

-- Engineering Society
(15, 22), -- Michael Martin
(16, 23), -- Linda Thompson
(17, 24), -- Richard Garcia
(18, 25), -- Barbara Martinez
(19, 26), -- Joseph Robinson
(20, 27), -- Susan Clark
(29, 28), -- Anthony King (inactive)
(30, 29), -- Sandra Wright (expelled)
(24, 30), -- Helen Walker (alumni)

-- Student Council
(1, 31),  -- John Doe
(9, 32),  -- Robert Taylor
(15, 33), -- Michael Martin

-- Debate Club
(11, 34), -- William Thomas
(17, 35), -- Richard Garcia
(12, 36), -- Patricia Jackson (inactive)

-- Photography Club
(14, 37), -- Jennifer Harris
(18, 38); -- Barbara Martinez

-- ============================================================================
-- SECTION 5: CREATE TERMS WITH PROPER FEE LOGIC
-- ============================================================================

-- Create terms for 1st Semester 2023-2024 - ACTIVE MEMBERS
INSERT INTO term (semester, term_start, term_end, acad_year, fee_amount, fee_due, membership_id, payment_status, role, balance)
SELECT 
    '1st',
    '2023-08-15',
    '2023-12-15',
    '2023-2024',
    1000.00,
    '2023-09-15',
    m.membership_id,
    'unpaid',
    m.role,
    1000.00
FROM membership m
WHERE m.batch = '2023-2024' 
AND m.mem_status = 'active';

-- Create terms for 1st Semester 2023-2024 - INACTIVE MEMBERS
INSERT INTO term (semester, term_start, term_end, acad_year, fee_amount, fee_due, membership_id, payment_status, role, balance)
SELECT 
    '1st',
    '2023-08-15',
    '2023-12-15',
    '2023-2024',
    500.00,
    '2023-09-15',
    m.membership_id,
    'unpaid',
    m.role,
    500.00
FROM membership m
WHERE m.batch = '2023-2024' 
AND m.mem_status = 'inactive';

-- Create terms for 2nd Semester 2023-2024 - ACTIVE MEMBERS
INSERT INTO term (semester, term_start, term_end, acad_year, fee_amount, fee_due, membership_id, payment_status, role, balance)
SELECT 
    '2nd',
    '2024-01-15',
    '2024-05-15',
    '2023-2024',
    1000.00,
    '2024-02-15',
    m.membership_id,
    'unpaid',
    m.role,
    1000.00
FROM membership m
WHERE m.batch = '2023-2024' 
AND m.mem_status = 'active';

-- Create terms for 2nd Semester 2023-2024 - INACTIVE MEMBERS
INSERT INTO term (semester, term_start, term_end, acad_year, fee_amount, fee_due, membership_id, payment_status, role, balance)
SELECT 
    '2nd',
    '2024-01-15',
    '2024-05-15',
    '2023-2024',
    500.00,
    '2024-02-15',
    m.membership_id,
    'unpaid',
    m.role,
    500.00
FROM membership m
WHERE m.batch = '2023-2024' 
AND m.mem_status = 'inactive';

-- Create terms for Summer 2024 - ACTIVE MEMBERS (major orgs only)
INSERT INTO term (semester, term_start, term_end, acad_year, fee_amount, fee_due, membership_id, payment_status, role, balance)
SELECT 
    'Summer',
    '2024-06-01',
    '2024-07-31',
    '2023-2024',
    1000.00,
    '2024-06-15',
    m.membership_id,
    'unpaid',
    m.role,
    1000.00
FROM membership m
WHERE m.batch = '2023-2024' 
AND m.mem_status = 'active'
AND m.org_id IN (1, 2, 3);

-- Create terms for Summer 2024 - INACTIVE MEMBERS (major orgs only)
INSERT INTO term (semester, term_start, term_end, acad_year, fee_amount, fee_due, membership_id, payment_status, role, balance)
SELECT 
    'Summer',
    '2024-06-01',
    '2024-07-31',
    '2023-2024',
    500.00,
    '2024-06-15',
    m.membership_id,
    'unpaid',
    m.role,
    500.00
FROM membership m
WHERE m.batch = '2023-2024' 
AND m.mem_status = 'inactive'
AND m.org_id IN (1, 2, 3);

-- ============================================================================
-- SECTION 6: INSERT REALISTIC PAYMENT SCENARIOS
-- ============================================================================

-- SCENARIO 1: Active members who paid in full (1000.00)
INSERT INTO payment (amount, payment_date, term_id)
SELECT 
    1000.00,
    '2023-09-10',
    t.term_id
FROM term t
JOIN membership m ON t.membership_id = m.membership_id
JOIN has_membership hm ON m.membership_id = hm.membership_id
WHERE m.mem_status = 'active' 
AND t.semester = '1st' 
AND hm.student_id IN (1, 2, 9, 10, 15, 16);

-- SCENARIO 2: Active members with partial payments
-- Mike Johnson (student_id=3) - partial payment
INSERT INTO payment (amount, payment_date, term_id)
SELECT 600.00, '2023-09-14', t.term_id 
FROM term t 
JOIN membership m ON t.membership_id = m.membership_id
JOIN has_membership hm ON m.membership_id = hm.membership_id
WHERE hm.student_id = 3 AND t.semester = '1st' AND t.acad_year = '2023-2024' LIMIT 1;

-- Sarah Williams (student_id=4) - first partial payment
INSERT INTO payment (amount, payment_date, term_id)
SELECT 400.00, '2023-09-20', t.term_id 
FROM term t 
JOIN membership m ON t.membership_id = m.membership_id
JOIN has_membership hm ON m.membership_id = hm.membership_id
WHERE hm.student_id = 4 AND t.semester = '1st' AND t.acad_year = '2023-2024' LIMIT 1;

-- Sarah Williams (student_id=4) - second partial payment
INSERT INTO payment (amount, payment_date, term_id)
SELECT 300.00, '2023-10-05', t.term_id 
FROM term t 
JOIN membership m ON t.membership_id = m.membership_id
JOIN has_membership hm ON m.membership_id = hm.membership_id
WHERE hm.student_id = 4 AND t.semester = '1st' AND t.acad_year = '2023-2024' LIMIT 1;

-- David Brown (student_id=5) - late full payment
INSERT INTO payment (amount, payment_date, term_id)
SELECT 1000.00, '2023-09-25', t.term_id 
FROM term t 
JOIN membership m ON t.membership_id = m.membership_id
JOIN has_membership hm ON m.membership_id = hm.membership_id
WHERE hm.student_id = 5 AND t.semester = '1st' AND t.acad_year = '2023-2024' LIMIT 1;

-- SCENARIO 3: Inactive members who paid their reduced fee (500.00)
INSERT INTO payment (amount, payment_date, term_id)
SELECT 
    500.00,
    '2023-09-12',
    t.term_id
FROM term t
JOIN membership m ON t.membership_id = m.membership_id
JOIN has_membership hm ON m.membership_id = hm.membership_id
WHERE m.mem_status = 'inactive' 
AND t.semester = '1st' 
AND hm.student_id IN (7, 28, 29);

-- SCENARIO 4: One inactive member with partial payment
-- Lisa Moore (inactive) - partial payment of reduced fee
INSERT INTO payment (amount, payment_date, term_id)
SELECT 300.00, '2023-09-18', t.term_id 
FROM term t 
JOIN membership m ON t.membership_id = m.membership_id
JOIN has_membership hm ON m.membership_id = hm.membership_id
WHERE hm.student_id = 8 AND t.semester = '1st' AND t.acad_year = '2023-2024' LIMIT 1;

-- SCENARIO 5: Second semester payments
-- Some active members paid for 2nd semester
INSERT INTO payment (amount, payment_date, term_id)
SELECT 
    1000.00,
    '2024-02-08',
    t.term_id
FROM term t
JOIN membership m ON t.membership_id = m.membership_id
JOIN has_membership hm ON m.membership_id = hm.membership_id
WHERE m.mem_status = 'active' 
AND t.semester = '2nd' 
AND hm.student_id IN (1, 9, 15);

-- Some inactive members paid reduced fee for 2nd semester
-- James Wilson paid 2nd semester inactive fee
INSERT INTO payment (amount, payment_date, term_id)
SELECT 500.00, '2024-02-10', t.term_id 
FROM term t 
JOIN membership m ON t.membership_id = m.membership_id
JOIN has_membership hm ON m.membership_id = hm.membership_id
WHERE m.mem_status = 'inactive' AND t.semester = '2nd' AND hm.student_id = 7 LIMIT 1;

-- ============================================================================
-- SECTION 7: COMPREHENSIVE TESTING QUERIES
-- ============================================================================

-- Test 1: Verify fee structure implementation
SELECT '=== TEST 1: FEE STRUCTURE VERIFICATION ===' AS test_section;
SELECT 
    s.first_name,
    s.last_name,
    org.org_name,
    m.mem_status,
    COUNT(t.term_id) as terms_created,
    CASE m.mem_status
        WHEN 'active' THEN 'Should pay 1000 per semester'
        WHEN 'inactive' THEN 'Should pay 500 per semester'
        WHEN 'expelled' THEN 'Should pay NOTHING (no terms)'
        WHEN 'alumni' THEN 'Should pay NOTHING (no terms)'
        ELSE 'Unknown status'
    END as fee_rule,
    CASE 
        WHEN m.mem_status IN ('expelled', 'alumni') AND COUNT(t.term_id) = 0 THEN '✓ CORRECT'
        WHEN m.mem_status IN ('active', 'inactive') AND COUNT(t.term_id) > 0 THEN '✓ CORRECT'
        WHEN m.mem_status IN ('expelled', 'alumni') AND COUNT(t.term_id) > 0 THEN '✗ ERROR: Should not have terms'
        WHEN m.mem_status IN ('active', 'inactive') AND COUNT(t.term_id) = 0 THEN '✗ ERROR: Missing terms'
        ELSE '? UNKNOWN'
    END as validation_status
FROM student s
JOIN has_membership hm ON s.student_id = hm.student_id
JOIN membership m ON hm.membership_id = m.membership_id
JOIN organization org ON m.org_id = org.org_id
LEFT JOIN term t ON m.membership_id = t.membership_id
WHERE m.batch = '2023-2024'
GROUP BY s.student_id, org.org_id
ORDER BY org.org_name, m.mem_status, s.last_name;

-- Test 2: Fee amount verification
SELECT '=== TEST 2: FEE AMOUNT VERIFICATION ===' AS test_section;
SELECT 
    s.first_name,
    s.last_name,
    org.org_name,
    m.mem_status,
    t.semester,
    t.fee_amount,
    CASE m.mem_status
        WHEN 'active' THEN 1000.00
        WHEN 'inactive' THEN 500.00
        ELSE 0.00
    END as expected_fee,
    CASE 
        WHEN m.mem_status = 'active' AND t.fee_amount = 1000.00 THEN '✓ CORRECT'
        WHEN m.mem_status = 'inactive' AND t.fee_amount = 500.00 THEN '✓ CORRECT'
        ELSE '✗ INCORRECT FEE'
    END as fee_validation
FROM student s
JOIN has_membership hm ON s.student_id = hm.student_id
JOIN membership m ON hm.membership_id = m.membership_id
JOIN organization org ON m.org_id = org.org_id
JOIN term t ON m.membership_id = t.membership_id
WHERE m.batch = '2023-2024'
ORDER BY org.org_name, t.semester, s.last_name;

-- Test 3: Payment status by membership type
SELECT '=== TEST 3: PAYMENT STATUS BY MEMBERSHIP TYPE ===' AS test_section;
SELECT 
    m.mem_status,
    COUNT(DISTINCT m.membership_id) as total_members,
    COUNT(DISTINCT t.term_id) as total_terms,
    SUM(t.fee_amount) as total_fees_due,
    COALESCE(SUM(p.amount), 0) as total_payments,
    SUM(t.fee_amount) - COALESCE(SUM(p.amount), 0) as outstanding_balance,
    ROUND(AVG(t.fee_amount), 2) as average_fee_per_term
FROM membership m
LEFT JOIN term t ON m.membership_id = t.membership_id
LEFT JOIN payment p ON t.term_id = p.term_id
WHERE m.batch = '2023-2024'
GROUP BY m.mem_status
ORDER BY m.mem_status;

-- Test 4: Detailed member payment tracking
SELECT '=== TEST 4: DETAILED MEMBER PAYMENT TRACKING ===' AS test_section;
SELECT 
    s.first_name,
    s.last_name,
    org.org_name,
    m.mem_status,
    t.semester,
    t.fee_amount as amount_due,
    COALESCE(SUM(p.amount), 0) as amount_paid,
    t.fee_amount - COALESCE(SUM(p.amount), 0) as balance,
    CASE 
        WHEN t.fee_amount - COALESCE(SUM(p.amount), 0) = 0 THEN 'PAID IN FULL'
        WHEN COALESCE(SUM(p.amount), 0) = 0 THEN 'NO PAYMENT'
        WHEN COALESCE(SUM(p.amount), 0) > 0 THEN 'PARTIAL PAYMENT'
        ELSE 'UNKNOWN'
    END as payment_status
FROM student s
JOIN has_membership hm ON s.student_id = hm.student_id
JOIN membership m ON hm.membership_id = m.membership_id
JOIN organization org ON m.org_id = org.org_id
LEFT JOIN term t ON m.membership_id = t.membership_id
LEFT JOIN payment p ON t.term_id = p.term_id
WHERE m.batch = '2023-2024'
GROUP BY s.student_id, org.org_id, t.term_id
ORDER BY org.org_name, s.last_name, t.semester;

-- Test 5: Verify expelled and alumni have no financial obligations
SELECT '=== TEST 5: VERIFY NO FEES FOR EXPELLED/ALUMNI ===' AS test_section;
SELECT 
    s.first_name,
    s.last_name,
    org.org_name,
    m.mem_status,
    m.batch,
    COUNT(t.term_id) as terms_count,
    COALESCE(SUM(t.fee_amount), 0) as total_fees,
    COUNT(p.payment_id) as payments_count,
    CASE 
        WHEN COUNT(t.term_id) = 0 AND COUNT(p.payment_id) = 0 THEN '✓ CORRECT - No financial obligations'
        ELSE '✗ ERROR - Should not have any fees or payments'
    END as validation
FROM student s
JOIN has_membership hm ON s.student_id = hm.student_id
JOIN membership m ON hm.membership_id = m.membership_id
JOIN organization org ON m.org_id = org.org_id
LEFT JOIN term t ON m.membership_id = t.membership_id
LEFT JOIN payment p ON t.term_id = p.term_id
WHERE m.mem_status IN ('expelled', 'alumni')
GROUP BY s.student_id, org.org_id
ORDER BY m.mem_status, org.org_name, s.last_name;

-- Test 6: Outstanding balances by organization
SELECT '=== TEST 6: OUTSTANDING BALANCES BY ORGANIZATION ===' AS test_section;
SELECT 
    org.org_name,
    m.mem_status,
    COUNT(DISTINCT s.student_id) as member_count,
    SUM(t.fee_amount) as total_fees_due,
    COALESCE(SUM(p.amount), 0) as total_paid,
    SUM(t.fee_amount) - COALESCE(SUM(p.amount), 0) as outstanding_balance,
    CASE 
        WHEN SUM(t.fee_amount) - COALESCE(SUM(p.amount), 0) = 0 THEN 'All paid'
        WHEN COALESCE(SUM(p.amount), 0) = 0 THEN 'No payments received'
        ELSE 'Partial payments'
    END as status
FROM organization org
JOIN membership m ON org.org_id = m.org_id
JOIN has_membership hm ON m.membership_id = hm.membership_id
JOIN student s ON hm.student_id = s.student_id
LEFT JOIN term t ON m.membership_id = t.membership_id
LEFT JOIN payment p ON t.term_id = p.term_id
WHERE m.batch = '2023-2024'
GROUP BY org.org_id, m.mem_status
ORDER BY org.org_name, m.mem_status;

-- Test 7: Cross-organization memberships with fee implications
SELECT '=== TEST 7: CROSS-ORGANIZATION MEMBERSHIPS ===' AS test_section;
SELECT 
    s.first_name,
    s.last_name,
    COUNT(DISTINCT m.org_id) as organizations_count,
    GROUP_CONCAT(DISTINCT org.org_name SEPARATOR ', ') as organizations,
    GROUP_CONCAT(DISTINCT m.mem_status SEPARATOR ', ') as statuses,
    SUM(t.fee_amount) as total_fees_all_orgs,
    COALESCE(SUM(p.amount), 0) as total_paid_all_orgs,
    SUM(t.fee_amount) - COALESCE(SUM(p.amount), 0) as total_outstanding
FROM student s
JOIN has_membership hm ON s.student_id = hm.student_id
JOIN membership m ON hm.membership_id = m.membership_id
JOIN organization org ON m.org_id = org.org_id
LEFT JOIN term t ON m.membership_id = t.membership_id
LEFT JOIN payment p ON t.term_id = p.term_id
WHERE m.batch = '2023-2024'
GROUP BY s.student_id
HAVING organizations_count > 1
ORDER BY total_outstanding DESC;

-- Test 8: Summary statistics
SELECT '=== TEST 8: SUMMARY STATISTICS ===' AS test_section;
SELECT 
    'Total Students' as metric, 
    COUNT(*) as count, 
    '' as additional_info
FROM student
UNION ALL
SELECT 
    'Total Organizations', 
    COUNT(*), 
    ''
FROM organization
UNION ALL
SELECT 
    'Total Memberships (2023-2024)', 
    COUNT(*), 
    ''
FROM membership WHERE batch = '2023-2024'
UNION ALL
SELECT 
    'Active Members', 
    COUNT(*), 
    'Pay 1000 per semester'
FROM membership WHERE batch = '2023-2024' AND mem_status = 'active'
UNION ALL
SELECT 
    'Inactive Members', 
    COUNT(*), 
    'Pay 500 per semester'
FROM membership WHERE batch = '2023-2024' AND mem_status = 'inactive'
UNION ALL
SELECT 
    'Expelled Members', 
    COUNT(*), 
    'Pay nothing'
FROM membership WHERE batch = '2023-2024' AND mem_status = 'expelled'
UNION ALL
SELECT 
    'Alumni Members', 
    COUNT(*), 
    'Pay nothing'
FROM membership WHERE mem_status = 'alumni'
UNION ALL
SELECT 
    'Total Terms Created', 
    COUNT(*), 
    'Only for active/inactive'
FROM term
UNION ALL
SELECT 
    'Total Payments Made', 
    COUNT(*), 
    ''
FROM payment;

-- ============================================================================
-- FINAL VALIDATION
-- ============================================================================

SELECT '=== FINAL BUSINESS LOGIC VALIDATION ===' AS test_section;

-- Check that business rules are correctly implemented
SELECT 
    'BUSINESS RULE VALIDATION' as check_type,
    CASE 
        WHEN (SELECT COUNT(*) FROM term t JOIN membership m ON t.membership_id = m.membership_id 
              WHERE m.mem_status IN ('expelled', 'alumni')) = 0 
        THEN '✓ PASSED: No terms for expelled/alumni members'
        ELSE '✗ FAILED: Found terms for expelled/alumni members'
    END as rule_1_expelled_alumni,
    
    CASE 
        WHEN (SELECT COUNT(*) FROM term t JOIN membership m ON t.membership_id = m.membership_id 
              WHERE m.mem_status = 'active' AND t.fee_amount != 1000.00) = 0
        THEN '✓ PASSED: All active members have 1000 fee'
        ELSE '✗ FAILED: Some active members have incorrect fee'
    END as rule_2_active_fee,
    
    CASE 
        WHEN (SELECT COUNT(*) FROM term t JOIN membership m ON t.membership_id = m.membership_id 
              WHERE m.mem_status = 'inactive' AND t.fee_amount != 500.00) = 0
        THEN '✓ PASSED: All inactive members have 500 fee'
        ELSE '✗ FAILED: Some inactive members have incorrect fee'
    END as rule_3_inactive_fee;

SELECT '=== DATABASE TESTING COMPLETED SUCCESSFULLY ===' AS test_section;