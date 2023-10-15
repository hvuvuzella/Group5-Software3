DROP DATABASE IF EXISTS hair_salon;
-- create database:
CREATE DATABASE hair_salon;

USE hair_salon;

-- create normalised tables:
CREATE TABLE clients (
	id INT AUTO_INCREMENT PRIMARY KEY,
	first_name VARCHAR(40) NOT NULL,
	last_name VARCHAR(40) NOT NULL,
	mobile VARCHAR(15),
	email VARCHAR(150)
);

CREATE TABLE stylists (
    id INT AUTO_INCREMENT PRIMARY KEY,
	first_name VARCHAR(50) NOT NULL,
	last_name VARCHAR(50) NOT NULL,
	mobile VARCHAR(15)
);

CREATE TABLE treatments (
    id INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(150) NOT NULL,
	description VARCHAR(400),
	price DECIMAL(10,2),
	duration TIME
);

CREATE TABLE salon_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    salon_name VARCHAR(100),
    telephone INT,
    email VARCHAR(100),
    address VARCHAR(200)
);

CREATE TABLE opening_hours (
    id INT AUTO_INCREMENT PRIMARY KEY,
    day_of_week ENUM('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday') NOT NULL, -- column can only consist of these values
    opening_time TIME,
    closing_time TIME
);

CREATE TABLE appointments (
	id INT AUTO_INCREMENT PRIMARY KEY,
	client_id INT,
	stylist_id INT,
	treatment_id INT,
	appt_date DATE NOT NULL,
	appt_time TIME NOT NULL,
	FOREIGN KEY (client_id) REFERENCES clients(id),
	FOREIGN KEY (stylist_id) REFERENCES stylists(id),
	FOREIGN KEY (treatment_id) REFERENCES treatments(id)
);

-- insert data into tables:

INSERT INTO clients (first_name, last_name, mobile, email)
VALUES
    ('Jane', 'Smith', '07763518723', 'jane.smith@email.com');
    
INSERT INTO stylists (first_name, last_name, mobile)
VALUES
	('Sophie', 'Jackson', '0798865432');
    
INSERT INTO salon_info (salon_name, telephone, email, address)
VALUES
	('THE CUT', '0208988652' 'info@thecut.co.uk', '52 Archer Street, Soho, London, W1 4HG');

INSERT INTO opening_hours (day_of_week, opening_time, closing_time)
VALUES
	('Monday', NULL, NULL),
    ('Tuesday', NULL, NULL),
    ('Wednesday', '09:00:00', '18:00:00'),
    ('Thursday', '09:00:00', '20:00:00'),
    ('Friday', '09:00:00', '18:00:00'),
    ('Saturday', '10:00:00', '18:00:00'),
    ('Sunday', '12:00:00', '17:00:00');

INSERT INTO treatments (name, description, price, duration)
VALUES
	('Blowdry', 'Blowdry styling only', 30.00, '00:25:00'),
	('Dry Cut', 'Dry cut on clean hair', 50.00, '00:30:00'),
	('Wash & Blowdry', 'Hair wash, and blowdry styling', 40.00, '00:30:00'),
    ('Cut & Blowdry', 'Dry cut and blowdry styling', 60.00, '00:45:00'),
    ('Wash, Cut & Blowdry', 'Hair wash, scalp massage, cut and blowdry/heat styling', 70.00, '01:00:00'),
    ('Colour - Full head', 'Hair colour dying - whole head', 150.00, '02:00:00'),
	('Colour - Roots', 'Top of of colour on roots', 75.00, '01:15:00'),
    ('Highlights', 'Whole head of highlights', 120.00, '01:45:00'),
    ('Perm - Wavy', 'Dry cut on short - medium length hair', 200.00, '02:00:00'),
    ('Perm - Straight', 'Dry cut on short - medium length hair', 200.00, '02:00:00');
    
    
    