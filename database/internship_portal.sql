CREATE DATABASE IF NOT EXISTS internship_portal;

USE internship_portal;


-- ================= ADMIN =================

CREATE TABLE IF NOT EXISTS admins (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ================= STUDENTS =================

CREATE TABLE IF NOT EXISTS students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(15),
    course VARCHAR(100),
    college VARCHAR(150),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ================= INTERNSHIPS =================

CREATE TABLE IF NOT EXISTS internships (
    internship_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    company VARCHAR(150) NOT NULL,
    location VARCHAR(100) NOT NULL,
    duration VARCHAR(50),
    stipend VARCHAR(50),
    skills VARCHAR(255),
    description TEXT,
    deadline DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ================= APPLICATIONS =================

CREATE TABLE IF NOT EXISTS applications (
    application_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    internship_id INT NOT NULL,
    status VARCHAR(30) DEFAULT 'Pending',
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (student_id)
        REFERENCES students(student_id)
        ON DELETE CASCADE,

    FOREIGN KEY (internship_id)
        REFERENCES internships(internship_id)
        ON DELETE CASCADE,

    UNIQUE(student_id, internship_id)
);


-- ================= SAMPLE INTERNSHIPS =================

INSERT INTO internships
(title, company, location, duration, stipend, skills, description, deadline)
VALUES
(
    'Web Development Intern',
    'TechNova Solutions',
    'Bangalore',
    '3 Months',
    '₹10,000/month',
    'HTML, CSS, JavaScript, Python',
    'Work on real-world web development projects and gain practical development experience.',
    '2026-12-30'
),
(
    'Python Developer Intern',
    'CodeCraft Technologies',
    'Hyderabad',
    '6 Months',
    '₹15,000/month',
    'Python, Flask, MySQL',
    'Develop backend applications and work with databases using Python and Flask.',
    '2026-11-30'
);