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
    telephone VARCHAR(15),
    email VARCHAR(100),
    address VARCHAR(300)
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

/* STORED PROCEDURE to insert new appointments: new appointments can only be made if they are wtihin the salon
opening hours, if they do not run past salon closing time, and if they do no clash with an already existing appointment */
DELIMITER //
CREATE PROCEDURE InsertNewAppointment(  -- arguments for procedure when calling it:
    IN a_client_id INT,
    IN a_stylist_id INT,
    IN a_treatment_id INT,
    IN a_appt_date DATE,
    IN a_appt_time TIME
)
BEGIN
    DECLARE b_opening_time TIME;  -- local variable to store salon opening time
    DECLARE b_closing_time TIME; -- local variable to store salon closing time
    DECLARE treatment_duration TIME; -- local variable to store treatment duration
    DECLARE appointment_end_time TIME; -- local variable to store the calculated end time of appointment

	-- get salon opening hours for the day of week that appointment falls on:
    SELECT opening_time, closing_time    -- retrieve open/close times from opening_hours table
    INTO b_opening_time, b_closing_time  -- assign retrieved values to the declared local variables
    FROM opening_hours
    WHERE day_of_week = DAYNAME(a_appt_date);  -- Use of in-built function DAYNAME() to extract the appt_date's day of the week, so it matches the opening_hours' day_of_week format

	-- get treatment duration from services table:
	SELECT duration
    INTO treatment_duration
    FROM treatments
    WHERE id = a_treatment_id;
    
    -- get calculated appointment end time, by adding duration of treatment to appointment start time:
	SET appointment_end_time = ADDTIME(a_appt_time, treatment_duration);

    IF b_opening_time IS NOT NULL AND b_closing_time IS NOT NULL AND -- if salon is open,
		TIME(a_appt_time) BETWEEN b_opening_time AND b_closing_time THEN -- and appt time is during opening hours,
        
		IF appointment_end_time > b_closing_time THEN -- then check if appointment runs over salon closing time. If so, throw error:
			SIGNAL SQLSTATE 'APER1' -- New SQLSTATE code for error in appt end time
			SET MESSAGE_TEXT = 'Error: this appointment cannot be made because it will run over salon closing time';
		ELSE
			
			IF EXISTS ( -- if not, then check if appointment clashes with any existing appointments the hair stylist already has. If so, throw error:
				SELECT 1
				FROM appointments
				WHERE stylist_id = a_stylist_id
				AND appt_date = a_appt_date
				AND (
					(a_appt_time BETWEEN appt_time AND ADDTIME(appt_time, (SELECT duration FROM treatments WHERE id = treatment_id)))
					OR (appointment_end_time BETWEEN appt_time AND ADDTIME(appt_time, (SELECT duration FROM treatments WHERE id = treatment_id)))
				)
			) THEN
				SIGNAL SQLSTATE 'APER2' -- New SQLSTATE code for appointment clashing with another appt
				SET MESSAGE_TEXT = 'Error: This appointment cannot be made because it clashes with an already exisiting appointment. Please choose another time';
            ELSE
				-- If no violations are found, then allow to insert data
				INSERT INTO appointments (client_id, stylist_id, treatment_id, appt_date, appt_time)
                VALUES (a_client_id, a_stylist_id, a_treatment_id, a_appt_date, a_appt_time);
			END IF;
		END IF;
	ELSE -- BUT, if any appointments are made outside opening hours anyway(see first IF condition), then throw error:
		SIGNAL SQLSTATE 'APER3'
        SET MESSAGE_TEXT = 'Error: This appointment cannot be made because it is not within salon opening times';
	END IF;
END;
//
DELIMITER ;

-- POPULATE TABLES WITH DATA:

INSERT INTO clients (first_name, last_name, mobile, email)
VALUES
    ('Jane', 'Smith', '07763518723', 'jane.smith@email.com');
    -- please add 9 more rows of data
    
INSERT INTO stylists (first_name, last_name, mobile)
VALUES
	('Sophie', 'Jackson', '0798865432');
    -- please add 9 more rows of data
    
INSERT INTO salon_info (salon_name, telephone, email, address)
VALUES
	('THE CUT', '0208988652', 'info@thecut.co.uk', '52 Archer Street, Soho, London, W1 4HG');
    -- no more data needed for this table

INSERT INTO opening_hours (day_of_week, opening_time, closing_time)
VALUES
	('Monday', NULL, NULL),
    ('Tuesday', NULL, NULL),
    ('Wednesday', '09:00:00', '18:00:00'),
    ('Thursday', '09:00:00', '20:00:00'),
    ('Friday', '09:00:00', '18:00:00'),
    ('Saturday', '10:00:00', '18:00:00'),
    ('Sunday', '12:00:00', '17:00:00');
    -- no more data needed for this table

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
    -- add more treatments if you think necessary
    
-- insert data into appointments table by calling stored procedure created above:
CALL InsertNewAppointment(1, 1, 5, '2023-11-01', '09:00:00');
-- CALL InsertNewAppointment(1, 1, 5, '2023-10-31', '09:00:00'); -- check stored procedure works (uncomment to try): outside salon opening hours
-- CALL InsertNewAppointment(1, 1, 5, '2023-11-01', '09:30:00'); -- check stored procedure works (uncomment to try): clashes with an existing appt
-- Hopefully the Python API we build will do this part for us when end user "books" their appointment

-- need to create a stored procedure to delete appts

-- need to create a stored procedure to update appts

-- need to create a table for seeing appointment availability for each stylist?
    