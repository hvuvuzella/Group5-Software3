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

/* STORED PROCEDURE TO ADD NEW APPOINTMENTS: new appointments can only be made if they are wtihin the salon
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

	-- get treatment duration from treatments table:
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


/* STORED PROCEDURE TO UPDATE/CHANGE EXISTING APPOINTMENTS: appointments can only be changed if they exist, if they are wtihin the salon
opening hours, if they do not run past salon closing time, and if they do no clash with any other existing appointments */

DELIMITER //
CREATE PROCEDURE UpdateAppointment( -- arguments for procedure when calling it:
    IN a_appointment_id INT,
    IN a_client_id INT,
    IN a_stylist_id INT,
    IN a_treatment_id INT,
    IN a_appt_date DATE,
    IN a_appt_time TIME
)
BEGIN -- declare local variables:
    DECLARE appointment_exists INT;
    DECLARE new_appt_end_time TIME;
	DECLARE b_opening_time TIME;
	DECLARE b_closing_time TIME;
    DECLARE treatment_duration TIME;
    
	-- get salon opening hours for the day of week that updated appointment would fall on:
	SELECT opening_time, closing_time
	INTO b_opening_time, b_closing_time
	FROM opening_hours
	WHERE day_of_week = DAYNAME(a_appt_date);
    
	-- get treatment duration for the appointment being updated:
	SELECT duration
    INTO treatment_duration
    FROM treatments
    WHERE id = (SELECT treatment_id FROM appointments WHERE id = a_appointment_id);
    
	-- Calculate the new appointment end time, by adding duration of treatment to updated appointment start time:
    SET new_appt_end_time = ADDTIME(a_appt_time, treatment_duration);
    
	-- Check if the appointment exists by counting how many appts there are for the appointment_id in question:
    SELECT COUNT(*) 
    INTO appointment_exists 
    FROM appointments 
    WHERE id = a_appointment_id;
    
    -- If the appointment does not exist (count returned 0 rows of data), then throw an error:
    IF appointment_exists = 0 THEN
        SIGNAL SQLSTATE 'UPAT1' -- Custom SQLSTATE code for appointment not found
        SET MESSAGE_TEXT = 'Error: Appointment not found. Please provide a valid appointment ID';
    ELSE
        -- Check if the new appointment time falls within salon opening hours:
        IF b_opening_time IS NOT NULL AND b_closing_time IS NOT NULL AND -- if salon is open
           TIME(a_appt_time) BETWEEN b_opening_time AND b_closing_time THEN -- and new appt time is during open hours,
           
           -- then check if the new appointment runs over salon closing time:
			IF new_appt_end_time > b_closing_time THEN
                SIGNAL SQLSTATE 'UPAT2' -- New SQLSTATE code for error in appt end time
                SET MESSAGE_TEXT = 'Error: this appointment cannot be made because it will run over salon closing time';
			ELSE
				-- Check if the new appointment clashes with any other existing appointments:
				IF EXISTS (
					SELECT 1
					FROM appointments
					WHERE stylist_id = a_stylist_id
                    AND appt_date = a_appt_date
					AND (
						(a_appt_time BETWEEN appt_time AND ADDTIME(appt_time, treatment_duration))
						OR (new_appt_end_time BETWEEN appt_time AND ADDTIME(appt_time, treatment_duration))
					)
				) THEN
					SIGNAL SQLSTATE 'UPAT3' -- Custom SQLSTATE code for appointment clash with another appointment
					SET MESSAGE_TEXT = 'Error: The updated appointment clashes with an existing appointment. Please choose another time.';
				ELSE
					-- If no violations are found, all to update appointment data
					UPDATE appointments
					SET id = a_appointment_id,
						client_id = a_client_id,
						stylist_id = a_stylist_id,
                        treatment_id = a_treatment_id,
						appt_date = a_appt_date,
						appt_time = a_appt_time
					WHERE id = a_appointment_id;
				END IF;
			END IF;
		ELSE
			SIGNAL SQLSTATE 'UPAT4' -- Custom SQLSTATE code for appointment outside opening hours
			SET MESSAGE_TEXT = 'Error: The updated appointment is not within salon opening hours.';
        END IF;
    END IF;
END;
//
DELIMITER ;


/* STORED PROCEDURE TO CANCEL APPOINTMENTS: appointments can only be cancelled if the appointment exists in the first place*/

DELIMITER //
CREATE PROCEDURE CancelAppointment( -- arguments for procedure when calling it:
	IN a_appointment_id INT
)
BEGIN
	-- check if appt exists:
    DECLARE appointment_exists INT;
    SELECT COUNT(*) INTO appointment_exists FROM appointments WHERE id = a_appointment_id;
    
    -- if appt does not exist, then throw error:
    IF appointment_exists = 0 THEN
		SIGNAL SQLSTATE 'APER4' -- New SQLSTATE code for error appt does not exist
		SET MESSAGE_TEXT ='Error: appointment cannot be deleted because it does not exist. Please try another appointment id';
    ELSE
    
		-- otherwise, if appointment does exist, then allow to delete data (i.e. cancel appointment):
		DELETE FROM appointments WHERE id = a_appointment_id;
	END IF;
END;
//
DELIMITER ;


-- POPULATE TABLES WITH DATA:

INSERT INTO clients (first_name, last_name, mobile, email)
VALUES
    ('Michael', 'Jackson', '07763518723', 'michael.jackson@email.com'),
    ('Brody', 'Dalle', '07754896574', 'brody.dalle@email.com'),
    ('Jennie', 'Vee', '07784579521', 'jennie.vee@email.com'),
    ('Joaquin', 'Phoenix', '07747854678', 'sophie.judd@email.com'),
    ('Jesse', 'Hughes', '07958335464', 'jesse.hughes@email.com'),
    ('Ozzy', 'Osbourne', '07725143358', 'ozzy.osbourne@email.com'),
    ('Trent', 'Reznor', '07773255984', 'trent.reznor@email.com'),
    ('Jimi', 'Hendrix', '07958844687', 'jimi.hendrix@email.com'),
    ('David', 'Bowie', '07845698715', 'david.bowie@egmail.com'),
    ('Lana', 'Del Rey', '07546668745', 'lana.del.rey@email.com');
    
INSERT INTO stylists (first_name, last_name, mobile)
VALUES
	('Erika', 'Tatchyn', '0798865432'),
    ('Hannah', 'Magee', '0774566874'),
    ('Kate', 'Losyeva', '0779654478');
    -- no more stylists needed for this table
    
INSERT INTO salon_info (salon_name, telephone, email, address)
VALUES
	('THE CUT', '0208988652', 'info@thecut.co.uk', '52 Archer Street, Soho, London, W1 4HG');
	-- no more data needed for this table

INSERT INTO opening_hours (day_of_week, opening_time, closing_time)
VALUES
	('Monday', NULL, NULL),
    ('Tuesday', NULL, NULL),
    ('Wednesday', '09:00:00', '18:00:00'),
    ('Thursday', '09:00:00', '18:00:00'),
    ('Friday', '09:00:00', '18:00:00'),
    ('Saturday', '10:00:00', '18:00:00'),
    ('Sunday', '12:00:00', '17:00:00');
    -- no more data needed for this table

INSERT INTO treatments (name, description, price, duration)
VALUES
	('Blowdry', 'Blowdry styling only', 30.00, '00:25:00'),
	('Dry Cut', 'Dry cut on clean hair', 50.00, '00:30:00'),
	('Wash & Blowdry', 'Hair wash, and blowdry styling', 40.00, '00:30:00'),
    ('Dry Cut & Blowdry', 'Dry cut and blowdry styling', 60.00, '00:45:00'),
    ('Wash, Cut & Blowdry', 'Hair wash, scalp massage, cut and blowdry/heat styling', 70.00, '01:00:00'),
    ('Colour - Full head', 'Hair colour dying - whole head', 150.00, '02:00:00'),
	('Colour - Roots', 'Top of of colour on roots', 75.00, '01:15:00'),
    ('Highlights', 'Whole head of highlights', 120.00, '01:45:00'),
    ('Perm - Wavy', 'Dry cut on short - medium length hair', 200.00, '02:00:00'),
    ('Perm - Straight', 'Dry cut on short - medium length hair', 200.00, '02:00:00');

/* INSERT(ADD) NEW APPOINTMENTS - insert data into appointments table by calling stored procedure created above,
in the format: CALL InsertNewAppointment(client_id, stylist_id, treatment_id, appt_date, appt_time);  */
CALL InsertNewAppointment(1, 1, 1, '2023-11-01', '09:00:00');
CALL InsertNewAppointment(2, 1, 3, '2023-11-01', '11:00:00');
CALL InsertNewAppointment(3, 1, 5, '2023-11-02', '13:30:00');
CALL InsertNewAppointment(4, 1, 6, '2023-11-02', '11:00:00');
CALL InsertNewAppointment(5, 2, 7, '2023-11-03', '14:00:00');
CALL InsertNewAppointment(6, 2, 10, '2023-11-03', '16:00:00');
CALL InsertNewAppointment(7, 3, 9, '2023-11-04', '10:30:00');
CALL InsertNewAppointment(8, 3, 4, '2023-11-05', '14:00:00');
CALL InsertNewAppointment(9, 2, 7, '2023-11-08', '15:30:00');
CALL InsertNewAppointment(10, 3, 8, '2023-11-09', '12:30:00');
-- the below lines will throw errors as conditions/constraints are violated. Uncomment to try:
-- CALL InsertNewAppointment(1, 1, 5, '2023-10-31', '09:00:00'); -- check stored procedure works (uncomment to try): outside salon opening hours
-- CALL InsertNewAppointment(1, 1, 5, '2023-11-01', '09:15:00'); -- clashes with an existing appt
-- CALL InsertNewAppointment(1, 2, 7, '2023-11-06', '12:30:00'); -- this is a Monday, salon isn't open on Mondays



/* UPDATE EXISTING APPOINTMENTS - update existing data in appointments table by calling stored procedure created above,
in the format: CALL UpdateAppointmentDateTime(appointment_id, client_id, stylist_id, treatment_id, appt_date, appt_time); */

-- see all appts BEFORE updating appt:
CREATE VIEW before_update_appt AS
SELECT * FROM appointments
ORDER BY id;
SELECT * FROM before_update_appt; 

-- now update appointments:
CALL UpdateAppointment(1, 1, 1, 1, '2023-11-01', '09:30:00'); 
-- the below lines will throw errors as conditions/constraints are violated. Uncomment to try:
-- CALL UpdateAppointment(2, 2, 1, 3, '2023-11-01', '11:05:00');  -- clashes with another existing appt for that day with that stylist
-- CALL UpdateAppointment(3, 3, 1, 5, '2023-11-02', '14:15:00'); -- clashes with another existing appt for that day with that stylist
-- CALL UpdateAppointment(5, 5, 1, 7, '2023-11-02', '13:15:00'); -- clashes with another existing appt for that day with that stylist
-- CALL UpdateAppointment(5, 5, 2, 1, '2023-11-06', '14:00:00'); -- appt not within salon opening hours
-- CALL UpdateAppointment(6, 6, 2, 10, '2023-11-04', '17:45:00'); -- appt runs over past salon closing time

-- finally, see all appts AFTER updating appt:
CREATE VIEW after_update_appt AS 
SELECT * FROM appointments
ORDER BY id;
SELECT * FROM after_update_appt; 




/* CANCEL(DELETE) EXISTING APPOINTMENTS - delete existing data in appointments table by calling stored procedure created above,
in the format: CALL CancelAppointment(appointment_id); */

-- see all appts BEFORE cancellation
CREATE VIEW before_cancellation AS
SELECT * FROM appointments
ORDER BY id;
SELECT * FROM before_cancellation; -- see the VIEW

CALL CancelAppointment(10);
-- the below line will throw an error as conditions/constraints are violated. Uncomment to try:
-- CALL CancelAppointment(50); -- appt does not exist

-- see all appts AFTER cancellation
CREATE VIEW after_cancellation AS
SELECT * FROM appointments
ORDER by id; 
SELECT * FROM after_cancellation;-- see the VIEW


-- See all data from tables:
SELECT * FROM clients;
SELECT * FROM stylists;
SELECT * FROM treatments;
SELECT * FROM salon_info;
SELECT * FROM opening_hours;
SELECT * FROM appointments;


-- need to create a table for seeing appointment availability for each stylist? - TBC
    