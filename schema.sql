-- schema.sql
-- Clean up previous tables if they exist
DROP TABLE IF EXISTS Enrollments;
DROP TABLE IF EXISTS Courses;
DROP TABLE IF EXISTS Students;
DROP TABLE IF EXISTS Departments;

-- 1. Departments Table
CREATE TABLE Departments (
    DepartmentID SERIAL PRIMARY KEY,
    Name VARCHAR(100) UNIQUE NOT NULL,
    Head VARCHAR(100)
);

-- 2. Students Table
CREATE TABLE Students (
    StudentID SERIAL PRIMARY KEY,
    FullName VARCHAR(100) NOT NULL,
    Email VARCHAR(150) UNIQUE NOT NULL,
    EnrollmentYear INT CHECK (EnrollmentYear > 2000),
    DepartmentID INT REFERENCES Departments(DepartmentID)
);

-- 3. Courses Table
CREATE TABLE Courses (
    CourseID SERIAL PRIMARY KEY,
    CourseName VARCHAR(100) NOT NULL,
    Credits INT CHECK (Credits > 0),
    DepartmentID INT REFERENCES Departments(DepartmentID)
);

-- 4. Enrollments Table (Junction Table for M:N)
CREATE TABLE Enrollments (
    EnrollmentID SERIAL PRIMARY KEY,
    StudentID INT REFERENCES Students(StudentID) ON DELETE CASCADE,
    CourseID INT REFERENCES Courses(CourseID),
    Grade VARCHAR(2),
    EnrollmentDate DATE DEFAULT CURRENT_DATE,
    CONSTRAINT unique_enrollment UNIQUE (StudentID, CourseID)
);

-- Indexes for Optimization
    CREATE INDEX idx_student_email ON Students(Email);
    CREATE INDEX idx_enrollment_student ON Enrollments(StudentID);