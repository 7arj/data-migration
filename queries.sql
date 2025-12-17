-- 1. Aggregation: Count students per department
SELECT d.Name, COUNT(s.StudentID) as StudentCount
FROM Departments d
JOIN Students s ON d.DepartmentID = s.DepartmentID
GROUP BY d.Name;

-- 2. Optimization Check
EXPLAIN ANALYZE SELECT * FROM Students WHERE Email = 'rahul.sharma@example.com';