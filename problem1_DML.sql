USE company;

INSERT INTO employee (ssn, fname, lname, bdate, address, gender, salary) VALUES
('111111111', 'Ahmed', 'Khyal',  '2004-10-1', 'Alexandria', 'M', 9000.00),
('222222222', 'Sara',  'Mostafa', '1990-07-25', 'Cairo',      'F', 7500.00),
('333333333', 'Mona',  'Adel',    '1988-11-02', 'Giza',       'F', 8200.00),
('444444444', 'Omar',  'Khaled',  '1993-01-18', 'Alexandria', 'M', 6000.00);

INSERT INTO department (Dnumber, Dname, mgr_ssn, mgr_start_date) VALUES
(1, 'Engineering', '111111111', '2015-01-01'),
(2, 'Sales',       '222222222', '2018-06-15'),
(3, 'HR',          '333333333', '2020-09-01');

INSERT INTO project (Pnumber, Pname, Plocation, Dno) VALUES
(10, 'Website Redesign', 'Alexandria', 1),
(20, 'Sales Campaign',   'Cairo',      2),
(30, 'Hiring Drive',     'Giza',       3);

UPDATE employee SET Dno = 1 WHERE ssn = '111111111';
UPDATE employee SET Dno = 2 WHERE ssn = '222222222';
UPDATE employee SET Dno = 3 WHERE ssn = '333333333';
UPDATE employee SET Dno = 1 WHERE ssn = '444444444';

SELECT * FROM employee;
SELECT * FROM department;
SELECT * FROM project;
