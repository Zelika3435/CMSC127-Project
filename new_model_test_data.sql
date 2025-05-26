-- Test Data Population Script for Student Organization Management System
-- Clear existing data (in correct order due to foreign key constraints)

DELETE FROM payment;
DELETE FROM term;
DELETE FROM has_membership;
DELETE FROM membership;
DELETE FROM member;
DELETE FROM student;
DELETE FROM organization;

-- Reset AUTO_INCREMENT values
ALTER TABLE payment AUTO_INCREMENT = 1;
ALTER TABLE term AUTO_INCREMENT = 1;
ALTER TABLE membership AUTO_INCREMENT = 1;
ALTER TABLE member AUTO_INCREMENT = 1;
ALTER TABLE student AUTO_INCREMENT = 1;
ALTER TABLE organization AUTO_INCREMENT = 1;

-- Insert Organizations
INSERT INTO organization (org_name) VALUES 
('Computer Science Society'),
('Engineering Student Council');

-- Insert 25 Students with valid genders
INSERT INTO student (first_name, last_name, gender, degree_program, standing) VALUES 
('John', 'Smith', 'Male', 'Computer Science', 'Senior'),
('Jane', 'Johnson', 'Female', 'Software Engineering', 'Junior'),
('Michael', 'Williams', 'Male', 'Information Technology', 'Sophomore'),
('Sarah', 'Brown', 'Female', 'Electrical Engineering', 'Senior'),
('David', 'Jones', 'Male', 'Computer Science', 'Freshman'),
('Emily', 'Garcia', 'Female', 'Mechanical Engineering', 'Junior'),
('James', 'Miller', 'Male', 'Civil Engineering', 'Senior'),
('Jessica', 'Davis', 'Female', 'Computer Science', 'Sophomore'),
('Robert', 'Rodriguez', 'Male', 'Chemical Engineering', 'Junior'),
('Ashley', 'Martinez', 'Female', 'Software Engineering', 'Senior'),
('William', 'Hernandez', 'Male', 'Industrial Engineering', 'Freshman'),
('Amanda', 'Lopez', 'Female', 'Computer Science', 'Junior'),
('Christopher', 'Gonzalez', 'Male', 'Information Technology', 'Sophomore'),
('Stephanie', 'Wilson', 'Female', 'Mathematics', 'Senior'),
('Matthew', 'Anderson', 'Male', 'Physics', 'Junior'),
('Jennifer', 'Thomas', 'Female', 'Computer Science', 'Freshman'),
('Anthony', 'Taylor', 'Male', 'Electrical Engineering', 'Senior'),
('Nicole', 'Moore', 'Female', 'Business Administration', 'Sophomore'),
('Daniel', 'Jackson', 'Male', 'Computer Science', 'Junior'),
('Rachel', 'Martin', 'Female', 'Software Engineering', 'Senior'),
('Joshua', 'Lee', 'Male', 'Mechanical Engineering', 'Freshman'),
('Megan', 'Perez', 'Female', 'Computer Science', 'Junior'),
('Andrew', 'Thompson', 'Male', 'Civil Engineering', 'Sophomore'),
('Samantha', 'White', 'Other', 'Information Technology', 'Senior'),
('Joseph', 'Harris', 'Male', 'Computer Science', 'Graduate');

-- Insert Members for students who will have memberships
-- Students 1-10 for Organization 1 (Computer Science Society)
INSERT INTO member (student_id) VALUES 
(1), (2), (3), (4), (5), (6), (7), (8), (9), (10);

-- Students 11-20 for Organization 2 (Engineering Student Council)
INSERT INTO member (student_id) VALUES 
(11), (12), (13), (14), (15), (16), (17), (18), (19), (20);

-- Students 21-25 will be in both organizations
INSERT INTO member (student_id) VALUES 
(21), (22), (23), (24), (25);

-- Insert Memberships with valid committees
-- Organization 1 (Computer Science Society) - Students 1-10
INSERT INTO membership (batch, committee, org_id, student_id) VALUES 
('2020-2021', 'Finance', 1, 1),
('2021-2022', 'Secretariat', 1, 2),
('2022-2023', 'Documentation', 1, 3),
('2020-2021', 'Externals', 1, 4),
('2023-2024', 'Membership', 1, 5),
('2021-2022', 'Logistics', 1, 6),
('2022-2023', 'Education & Research', 1, 7),
('2020-2021', 'Publication', 1, 8),
('2023-2024', 'Finance', 1, 9),
('2021-2022', 'Secretariat', 1, 10);

-- Organization 2 (Engineering Student Council) - Students 11-20
INSERT INTO membership (batch, committee, org_id, student_id) VALUES 
('2020-2021', 'Documentation', 2, 11),
('2022-2023', 'Externals', 2, 12),
('2021-2022', 'Membership', 2, 13),
('2023-2024', 'Logistics', 2, 14),
('2020-2021', 'Education & Research', 2, 15),
('2022-2023', 'Publication', 2, 16),
('2021-2022', 'Finance', 2, 17),
('2023-2024', 'Secretariat', 2, 18),
('2020-2021', 'Documentation', 2, 19),
('2022-2023', 'Externals', 2, 20);

-- Students 21-25 in both organizations
INSERT INTO membership (batch, committee, org_id, student_id) VALUES 
-- Student 21 in both orgs
('2022-2023', 'Membership', 1, 21),
('2022-2023', 'Logistics', 2, 21),
-- Student 22 in both orgs
('2021-2022', 'Education & Research', 1, 22),
('2021-2022', 'Publication', 2, 22),
-- Student 23 in both orgs
('2023-2024', 'Finance', 1, 23),
('2023-2024', 'Secretariat', 2, 23),
-- Student 24 in both orgs
('2020-2021', 'Documentation', 1, 24),
('2020-2021', 'Externals', 2, 24),
-- Student 25 in both orgs
('2022-2023', 'Membership', 1, 25),
('2022-2023', 'Logistics', 2, 25);

-- Insert has_membership relationships
INSERT INTO has_membership (student_id, membership_id) VALUES 
-- Organization 1 memberships (IDs 1-10)
(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10),
-- Organization 2 memberships (IDs 11-20)
(11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20),
-- Dual memberships (IDs 21-30)
(21, 21), (21, 22), (22, 23), (22, 24), (23, 25), (23, 26), (24, 27), (24, 28), (25, 29), (25, 30);

-- Insert Terms with valid roles
-- Terms for Organization 1 memberships (membership_ids 1-10)
INSERT INTO term (semester, payment_status, mem_status, role, term_start, term_end, acad_year, fee_amount, fee_due, balance, membership_id) VALUES 
-- Membership 1 (Student 1) - Finance Committee
('1st', 'paid', 'active', 'Treasurer', '2023-08-15', '2023-12-15', '2023-2024', 250.00, '2023-09-15', 0.00, 1),
('2nd', 'paid', 'active', 'Treasurer', '2024-01-15', '2024-05-15', '2023-2024', 250.00, '2024-02-15', 0.00, 1),
-- Membership 2 (Student 2) - Secretariat
('1st', 'unpaid', 'active', 'Secretary', '2023-08-15', '2023-12-15', '2023-2024', 200.00, '2023-09-15', 200.00, 2),
('2nd', 'partial', 'active', 'Secretary', '2024-01-15', '2024-05-15', '2023-2024', 200.00, '2024-02-15', 75.00, 2),
-- Membership 3 (Student 3) - Documentation
('1st', 'paid', 'alumni', 'Member', '2023-08-15', '2023-12-15', '2023-2024', 150.00, '2023-09-15', 0.00, 3),
('2nd', 'paid', 'alumni', 'Member', '2024-01-15', '2024-05-15', '2023-2024', 150.00, '2024-02-15', 0.00, 3),
-- Membership 4 (Student 4) - Externals
('1st', 'paid', 'active', 'Vice President', '2023-08-15', '2023-12-15', '2023-2024', 300.00, '2023-09-15', 0.00, 4),
('2nd', 'paid', 'active', 'Vice President', '2024-01-15', '2024-05-15', '2023-2024', 300.00, '2024-02-15', 0.00, 4),
-- Membership 5 (Student 5) - Membership
('1st', 'unpaid', 'active', 'Member', '2024-08-15', '2024-12-15', '2024-2025', 180.00, '2024-09-15', 180.00, 5),
-- Membership 6 (Student 6) - Logistics
('1st', 'partial', 'inactive', 'Member', '2023-08-15', '2023-12-15', '2023-2024', 160.00, '2023-09-15', 50.00, 6),
('2nd', 'paid', 'inactive', 'Member', '2024-01-15', '2024-05-15', '2023-2024', 160.00, '2024-02-15', 0.00, 6),
-- Membership 7 (Student 7) - Education & Research
('1st', 'paid', 'active', 'Member', '2023-08-15', '2023-12-15', '2023-2024', 220.00, '2023-09-15', 0.00, 7),
('2nd', 'paid', 'active', 'Member', '2024-01-15', '2024-05-15', '2023-2024', 220.00, '2024-02-15', 0.00, 7),
-- Membership 8 (Student 8) - Publication
('1st', 'paid', 'active', 'President', '2023-08-15', '2023-12-15', '2023-2024', 350.00, '2023-09-15', 0.00, 8),
('2nd', 'paid', 'active', 'President', '2024-01-15', '2024-05-15', '2023-2024', 350.00, '2024-02-15', 0.00, 8),
-- Membership 9 (Student 9) - Finance
('1st', 'unpaid', 'expelled', 'Member', '2023-08-15', '2023-12-15', '2023-2024', 190.00, '2023-09-15', 190.00, 9),
-- Membership 10 (Student 10) - Secretariat
('1st', 'paid', 'active', 'Member', '2023-08-15', '2023-12-15', '2023-2024', 170.00, '2023-09-15', 0.00, 10),
('2nd', 'partial', 'active', 'Member', '2024-01-15', '2024-05-15', '2023-2024', 170.00, '2024-02-15', 85.00, 10);

-- Terms for Organization 2 memberships (membership_ids 11-20)
INSERT INTO term (semester, payment_status, mem_status, role, term_start, term_end, acad_year, fee_amount, fee_due, balance, membership_id) VALUES 
-- Membership 11 (Student 11) - Documentation
('1st', 'paid', 'active', 'Member', '2023-08-15', '2023-12-15', '2023-2024', 200.00, '2023-09-15', 0.00, 11),
('2nd', 'paid', 'active', 'Member', '2024-01-15', '2024-05-15', '2023-2024', 200.00, '2024-02-15', 0.00, 11),
-- Membership 12 (Student 12) - Externals
('1st', 'unpaid', 'active', 'Vice President', '2023-08-15', '2023-12-15', '2023-2024', 280.00, '2023-09-15', 280.00, 12),
('2nd', 'partial', 'active', 'Vice President', '2024-01-15', '2024-05-15', '2023-2024', 280.00, '2024-02-15', 120.00, 12),
-- Membership 13 (Student 13) - Membership
('1st', 'paid', 'alumni', 'Member', '2023-08-15', '2023-12-15', '2023-2024', 180.00, '2023-09-15', 0.00, 13),
-- Membership 14 (Student 14) - Logistics
('1st', 'paid', 'active', 'Treasurer', '2024-08-15', '2024-12-15', '2024-2025', 240.00, '2024-09-15', 0.00, 14),
-- Membership 15 (Student 15) - Education & Research
('1st', 'partial', 'inactive', 'Member', '2023-08-15', '2023-12-15', '2023-2024', 210.00, '2023-09-15', 90.00, 15),
('2nd', 'paid', 'inactive', 'Member', '2024-01-15', '2024-05-15', '2023-2024', 210.00, '2024-02-15', 0.00, 15),
-- Membership 16 (Student 16) - Publication
('1st', 'paid', 'active', 'Secretary', '2023-08-15', '2023-12-15', '2023-2024', 230.00, '2023-09-15', 0.00, 16),
('2nd', 'paid', 'active', 'Secretary', '2024-01-15', '2024-05-15', '2023-2024', 230.00, '2024-02-15', 0.00, 16),
-- Membership 17 (Student 17) - Finance
('1st', 'unpaid', 'expelled', 'Member', '2023-08-15', '2023-12-15', '2023-2024', 195.00, '2023-09-15', 195.00, 17),
-- Membership 18 (Student 18) - Secretariat
('1st', 'paid', 'active', 'President', '2024-08-15', '2024-12-15', '2024-2025', 320.00, '2024-09-15', 0.00, 18),
-- Membership 19 (Student 19) - Documentation
('1st', 'partial', 'active', 'Member', '2023-08-15', '2023-12-15', '2023-2024', 175.00, '2023-09-15', 60.00, 19),
('2nd', 'paid', 'active', 'Member', '2024-01-15', '2024-05-15', '2023-2024', 175.00, '2024-02-15', 0.00, 19),
-- Membership 20 (Student 20) - Externals
('1st', 'paid', 'active', 'Member', '2023-08-15', '2023-12-15', '2023-2024', 185.00, '2023-09-15', 0.00, 20),
('2nd', 'unpaid', 'inactive', 'Member', '2024-01-15', '2024-05-15', '2023-2024', 185.00, '2024-02-15', 185.00, 20);

-- Terms for dual memberships (membership_ids 21-30)
INSERT INTO term (semester, payment_status, mem_status, role, term_start, term_end, acad_year, fee_amount, fee_due, balance, membership_id) VALUES 
-- Student 21 memberships
('1st', 'paid', 'active', 'Member', '2023-08-15', '2023-12-15', '2023-2024', 160.00, '2023-09-15', 0.00, 21),
('1st', 'paid', 'active', 'Member', '2023-08-15', '2023-12-15', '2023-2024', 170.00, '2023-09-15', 0.00, 22),
-- Student 22 memberships
('1st', 'partial', 'alumni', 'Member', '2022-08-15', '2022-12-15', '2022-2023', 200.00, '2022-09-15', 75.00, 23),
('1st', 'paid', 'alumni', 'Member', '2022-08-15', '2022-12-15', '2022-2023', 190.00, '2022-09-15', 0.00, 24),
-- Student 23 memberships
('1st', 'paid', 'active', 'Treasurer', '2024-08-15', '2024-12-15', '2024-2025', 260.00, '2024-09-15', 0.00, 25),
('1st', 'unpaid', 'active', 'Member', '2024-08-15', '2024-12-15', '2024-2025', 180.00, '2024-09-15', 180.00, 26),
-- Student 24 memberships
('1st', 'paid', 'active', 'Member', '2021-08-15', '2021-12-15', '2021-2022', 150.00, '2021-09-15', 0.00, 27),
('2nd', 'paid', 'active', 'Member', '2022-01-15', '2022-05-15', '2021-2022', 150.00, '2022-02-15', 0.00, 27),
('1st', 'paid', 'active', 'Vice President', '2021-08-15', '2021-12-15', '2021-2022', 290.00, '2021-09-15', 0.00, 28),
-- Student 25 memberships
('1st', 'unpaid', 'inactive', 'Member', '2023-08-15', '2023-12-15', '2023-2024', 165.00, '2023-09-15', 165.00, 29),
('Summer', 'partial', 'inactive', 'Member', '2023-06-01', '2023-08-01', '2023-2024', 175.00, '2023-06-30', 80.00, 30);

-- Insert Payments for terms with 'paid' or 'partial' status
INSERT INTO payment (amount, payment_date, term_id) VALUES 
-- Payments for paid terms
(250.00, '2023-09-10', 1),  -- Term 1 - full payment
(250.00, '2024-02-10', 2),  -- Term 2 - full payment
(125.00, '2024-02-05', 4),  -- Term 4 - partial payment
(150.00, '2023-09-08', 5),  -- Term 5 - full payment
(150.00, '2024-02-08', 6),  -- Term 6 - full payment
(300.00, '2023-09-12', 7),  -- Term 7 - full payment
(300.00, '2024-02-12', 8),  -- Term 8 - full payment
(110.00, '2023-09-20', 10), -- Term 10 - partial payment
(220.00, '2023-09-15', 12), -- Term 12 - full payment
(220.00, '2024-02-15', 13), -- Term 13 - full payment
(350.00, '2023-09-05', 14), -- Term 14 - full payment
(350.00, '2024-02-05', 15), -- Term 15 - full payment
(170.00, '2023-09-18', 17), -- Term 17 - full payment
(85.00, '2024-02-20', 18),  -- Term 18 - partial payment
(200.00, '2023-09-14', 19), -- Term 19 - full payment
(200.00, '2024-02-14', 20), -- Term 20 - full payment
(160.00, '2024-02-18', 22), -- Term 22 - partial payment
(180.00, '2023-09-16', 23), -- Term 23 - full payment
(240.00, '2024-09-10', 24), -- Term 24 - full payment
(120.00, '2023-09-25', 25), -- Term 25 - partial payment
(210.00, '2024-02-25', 26), -- Term 26 - full payment
(230.00, '2023-09-13', 27), -- Term 27 - full payment
(230.00, '2024-02-13', 28), -- Term 28 - full payment
(320.00, '2024-09-08', 30), -- Term 30 - full payment
(115.00, '2023-09-22', 31), -- Term 31 - partial payment
(175.00, '2024-02-22', 32), -- Term 32 - full payment
(185.00, '2023-09-17', 33), -- Term 33 - full payment
(160.00, '2023-09-11', 35), -- Term 35 - full payment
(170.00, '2023-09-11', 36), -- Term 36 - full payment
(125.00, '2022-09-15', 37), -- Term 37 - partial payment
(190.00, '2022-09-12', 38), -- Term 38 - full payment
(260.00, '2024-09-12', 39), -- Term 39 - full payment
(150.00, '2021-09-10', 41), -- Term 41 - full payment
(150.00, '2022-02-10', 42), -- Term 42 - full payment
(290.00, '2021-09-08', 43), -- Term 43 - full payment
(95.00, '2023-09-30', 45);  -- Term 45 - partial payment

-- Verification queries to check data integrity
-- You can run these to verify the data was inserted correctly

-- SELECT 'Organizations' as Table_Name, COUNT(*) as Count FROM organization
-- UNION ALL
-- SELECT 'Students', COUNT(*) FROM student
-- UNION ALL
-- SELECT 'Members', COUNT(*) FROM member
-- UNION ALL
-- SELECT 'Memberships', COUNT(*) FROM membership
-- UNION ALL
-- SELECT 'Terms', COUNT(*) FROM term
-- UNION ALL
-- SELECT 'Payments', COUNT(*) FROM payment;

-- Sample queries to test relationships:

-- Show students with multiple memberships:
-- SELECT s.first_name, s.last_name, COUNT(m.membership_id) as membership_count
-- FROM student s
-- JOIN membership m ON s.student_id = m.student_id
-- GROUP BY s.student_id
-- HAVING membership_count > 1;

-- Show payment summary by organization:
-- SELECT o.org_name, 
--        COUNT(DISTINCT m.student_id) as total_members,
--        SUM(t.fee_amount) as total_fees,
--        SUM(CASE WHEN t.payment_status = 'paid' THEN t.fee_amount ELSE 0 END) as paid_amount,
--        SUM(t.balance) as outstanding_balance
-- FROM organization o
-- JOIN membership m ON o.org_id = m.org_id
-- JOIN term t ON m.membership_id = t.membership_id
-- GROUP BY o.org_id, o.org_name;