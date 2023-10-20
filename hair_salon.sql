DROP DATABASE IF EXISTS hair_salon;
-- create database:
CREATE DATABASE hair_salon;

USE hair_salon;

-- create normalised tables:
CREATE TABLE customers (
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

CREATE TABLE opening_times (
    id INT AUTO_INCREMENT PRIMARY KEY,
    week_day VARCHAR(20),
    open_time TIME,
    close_time TIME
);

CREATE TABLE bookings (
	id INT AUTO_INCREMENT PRIMARY KEY,
	customer_id INT,
	stylist_id INT,
	treatment_id INT,
	booking_date DATE NOT NULL,
	booking_time TIME NOT NULL,
	FOREIGN KEY (customer_id) REFERENCES customers(id),
	FOREIGN KEY (stylist_id) REFERENCES stylists(id),
	FOREIGN KEY (treatment_id) REFERENCES treatments(id)
);

/* STORED PROCEDURE TO MAKE NEW BOOKINGS */
DELIMITER //
CREATE PROCEDURE AddNewBooking(  -- input parameters for stored procedure
    IN a_customer_id INT,
    IN a_stylist_id INT,
    IN a_treatment_id INT,
    IN a_booking_date DATE,
    IN a_booking_time TIME
)
BEGIN
	-- local variables to use in procedure:
    DECLARE b_open_time TIME;
    DECLARE b_close_time TIME; 
    DECLARE treatment_duration TIME; 
    DECLARE booking_time_finish TIME; 

	-- retrieve salon opening times for the booking date
    SELECT open_time, close_time
    INTO b_open_time, b_close_time
    FROM opening_times
    WHERE week_day = DAYNAME(a_booking_date);

	-- get duration of the treatment:
	SELECT duration
    INTO treatment_duration
    FROM treatments
    WHERE id = a_treatment_id;
    
    -- add booking start time and the duration of treatment to work out what time the booking will finish:
	SET booking_time_finish = ADDTIME(a_booking_time, treatment_duration);
    
    -- check: if customer does not exist, then throw error:
    IF a_customer_id IS NOT NULL AND NOT EXISTS (
        SELECT 1
        FROM customers
        WHERE id = a_customer_id
    ) THEN
        SIGNAL SQLSTATE 'NOCST' -- unique error code
        SET MESSAGE_TEXT = 'Error: Customer id does not exist; enter a valid id, or go back and add new customer details to the customer table first.';
    ELSE    

		IF b_open_time IS NOT NULL AND b_close_time IS NOT NULL AND -- check that the salon is not closed
			TIME(a_booking_time) BETWEEN b_open_time AND b_close_time THEN -- check that the booking start time is between open and close time
			
			IF booking_time_finish > b_close_time THEN -- check if the booking finishes after the salon is closed
				SIGNAL SQLSTATE '2LATE' -- unique error code
				SET MESSAGE_TEXT = 'Error: the booking will finish after the salon is closed, please choose an earlier time';
			ELSE
				
				IF EXISTS ( -- if not, see if the booking clashes with an exisitng booking:
					SELECT 1
					FROM bookings
					WHERE stylist_id = a_stylist_id
					AND booking_date = a_booking_date
					AND (
						(a_booking_time BETWEEN booking_time AND ADDTIME(booking_time, (SELECT duration FROM treatments WHERE id = treatment_id)))
						OR (booking_time_finish BETWEEN booking_time AND ADDTIME(booking_time, (SELECT duration FROM treatments WHERE id = treatment_id)))
					)
				) THEN
					SIGNAL SQLSTATE 'CLASH' -- unique error code
					SET MESSAGE_TEXT = 'Error: This booking will clash with an already exisiting booking Please choose another time';
				ELSE
					-- If no errors are found, then insert new booking to bookings table:
					INSERT INTO bookings (customer_id, stylist_id, treatment_id, booking_date, booking_time)
					VALUES (a_customer_id, a_stylist_id, a_treatment_id, a_booking_date, a_booking_time);
				END IF;
			END IF;
		ELSE -- In case there are any other conditions that don't meet the criteria, do not allow to book:
			SIGNAL SQLSTATE 'ERUNK'
			SET MESSAGE_TEXT = 'Error: This booking failed for errors: unknown, please try again';
		END IF;
	END IF;
END;
//
DELIMITER ;


/* STORED PROCEDURE TO UPDATE/CHANGE EXISITNG BOOKINGS: */

DELIMITER //
CREATE PROCEDURE UpdateBooking( -- input parameters for stored procedure:
    IN a_booking_id INT,
    IN a_customer_id INT,
    IN a_stylist_id INT,
    IN a_treatment_id INT,
    IN a_booking_date DATE,
    IN a_booking_time TIME
)
BEGIN -- local variables to use in procedure:
    DECLARE booking_exists INT;
    DECLARE new_booking_finish_time TIME;
	DECLARE b_open_time TIME;
	DECLARE b_close_time TIME;
    DECLARE treatment_duration TIME;
    
	-- retrieve salon opening times for the booking date
	SELECT open_time, close_time
	INTO b_open_time, b_close_time
	FROM opening_times
	WHERE week_day = DAYNAME(a_booking_date);
    
	-- get duration of the treatment for the updated booking:
	SELECT duration
    INTO treatment_duration
    FROM treatments
    WHERE id = (SELECT treatment_id FROM bookings WHERE id = a_booking_id);
    
	-- add booking start time and the duration of treatment to work out what time the booking will finish:
    SET new_booking_finish_time = ADDTIME(a_booking_time, treatment_duration);
    
	-- Check if the booking exists by counting how many bookings there are for the booking_id in question:
    SELECT COUNT(*) 
    INTO booking_exists 
    FROM bookings
    WHERE id = a_booking_id;
    
    -- If the booking does not exist (count returned 0 rows of data), then throw an error:
    IF booking_exists = 0 THEN
        SIGNAL SQLSTATE 'UPAT1' -- unique error code
        SET MESSAGE_TEXT = 'Error: Booking not found. Please provide a valid booking ID';
    ELSE
        -- Check if the new booking time falls within salon opening hours:
        IF b_open_time IS NOT NULL AND b_close_time IS NOT NULL AND -- check that the salon is not closed
           TIME(a_booking_time) BETWEEN b_open_time AND b_close_time THEN -- check that the booking start time is between open and close time
           
           -- check if the booking finishes after the salon is closed
			IF new_booking_finish_time > b_close_time THEN
				SIGNAL SQLSTATE '2LATE' -- unique error code
				SET MESSAGE_TEXT = 'Error: the booking will finish after the salon is closed, please choose an earlier time';
			ELSE
				-- if not, see if the booking clashes with an exisitng booking:
				IF EXISTS (
					SELECT 1
					FROM bookings
					WHERE stylist_id = a_stylist_id
                    AND booking_date = a_booking_date
					AND (
						(a_booking_time BETWEEN booking_time AND ADDTIME(booking_time, treatment_duration))
						OR (new_booking_finish_time BETWEEN booking_time AND ADDTIME(booking_time, treatment_duration))
					)
				) THEN
					SIGNAL SQLSTATE 'CLASH' -- unique error code
					SET MESSAGE_TEXT = 'Error: This booking will clash with an already exisiting booking Please choose another time';
				ELSE
					-- If no errors are found, then update exisitng booking in bookings table:
					UPDATE bookings
					SET id = a_booking_id,
						customer_id = a_customer_id,
						stylist_id = a_stylist_id,
                        treatment_id = a_treatment_id,
						booking_date = a_booking_date,
						booking_time = a_booking_time
					WHERE id = a_booking_id;
                    
                    SET a_booking_id = LAST_INSERT_ID(); -- Retrieve the last inserted ID - for use in Python later
				END IF;
			END IF;
		ELSE -- In case there are any other conditions that don't meet the criteria, do not allow to update booking:
			SIGNAL SQLSTATE 'ERUNK'
			SET MESSAGE_TEXT = 'Error: This booking failed for errors: unknown, please try again';
        END IF;
    END IF;
END;
//
DELIMITER ;


/* STORED PROCEDURE TO CANCEL BOOKINGS: bookings can only be cancelled if the booking exists in the first place */

DELIMITER //
CREATE PROCEDURE CancelBooking( -- input parameters
	IN a_booking_id INT
)
BEGIN
	-- check if bookings exists:
    DECLARE booking_exists INT;
    SELECT COUNT(*) INTO booking_exists FROM bookings WHERE id = a_booking_id;
    
    -- if booking does not exist, then throw error:
    IF booking_exists = 0 THEN
        SIGNAL SQLSTATE 'UPAT1' -- unique error code
        SET MESSAGE_TEXT = 'Error: Booking not found. Please provide a valid booking ID';
    ELSE
    
		-- otherwise, if booking does exist, then allow to delete data (i.e. cancel booking):
		DELETE FROM bookings WHERE id = a_booking_id;
	END IF;
END;
//
DELIMITER ;

/* STORED PROCEDURE TO SEE ALL OF A STYLIST'S SCHEDULED BOOKINGS FOR A GIVEN DAY, 
displaying customers's full name, mobile, the treatment they are having and their booking start and finish time:  */

DELIMITER //
CREATE PROCEDURE GetStylistSchedule( -- arguments for procedure when calling it:
    IN stylist_id INT,
    IN booking_date DATE
)
BEGIN
	-- select relevant data from bookings to display
    SELECT 
		a.id, 
        c.first_name AS customer_first_name, 
        c.last_name AS customer_last_name, 
        c.mobile AS customer_mobile, 
        t.name AS treatment_name, 
        a.booking_time, ADDTIME(a.booking_time, t.duration) AS booking_end_time -- calculate booking finish time
	-- Join the 'bookings' table with the 'customers' and 'treatments' tables
    FROM bookings AS a
    JOIN customers AS c ON a.customer_id = c.id
    JOIN treatments AS t ON a.treatment_id = t.id
    WHERE a.stylist_id = stylist_id
    AND a.booking_date = booking_date;
END;
//
DELIMITER ;



-- POPULATE TABLES WITH DATA:

INSERT INTO customers (first_name, last_name, mobile, email)
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

INSERT INTO opening_times (week_day, open_time, close_time)
VALUES
	('Monday', NULL, NULL),
    ('Tuesday', NULL, NULL),
    ('Wednesday', '09:00:00', '18:00:00'),
    ('Thursday', '09:00:00', '18:00:00'),
    ('Friday', '09:00:00', '18:00:00'),
    ('Saturday', '10:00:00', '18:00:00'),
    ('Sunday', '12:00:00', '17:00:00');

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

/* ADD NEW BOOKINGS - add data into bookings table by calling stored procedure created above,
in the format: CALL AddNewBooking(customer_id, stylist_id, treatment_id, booking_date, booking_time);  */
CALL AddNewBooking(1, 1, 1, '2023-11-01', '09:00:00');
CALL AddNewBooking(2, 1, 3, '2023-11-01', '11:00:00');
CALL AddNewBooking(3, 1, 5, '2023-11-02', '13:30:00');
CALL AddNewBooking(4, 1, 6, '2023-11-02', '11:00:00');
CALL AddNewBooking(5, 2, 7, '2023-11-03', '14:00:00');
CALL AddNewBooking(6, 2, 10, '2023-11-03', '16:00:00');
CALL AddNewBooking(7, 3, 9, '2023-11-04', '10:30:00');
CALL AddNewBooking(8, 3, 4, '2023-11-05', '14:00:00');
CALL AddNewBooking(9, 2, 7, '2023-11-08', '15:30:00');
CALL AddNewBooking(10, 3, 8, '2023-11-09', '12:30:00');
-- These queries underneath will not work as they fail coniditions set in procedure. Uncomment to try:
-- CALL AddNewBooking(100, 2, 1, '2023-11-09', '16:00:00'); -- custeomer id does not exist, either enter a valid id or create new customer
-- CALL AddNewBooking(1, 1, 5, '2023-10-31', '20:00:00'); -- outside salon opening times
-- CALL AddNewBooking(1, 1, 5, '2023-10-31', '07:00:00'); -- booking time is before the salon opens
-- CALL AddNewBooking(1, 1, 5, '2023-11-01', '09:15:00'); -- clashes with an existing booking
-- CALL AddNewBooking(1, 2, 7, '2023-11-06', '12:30:00'); -- salon is closed on Mondays
-- CALL AddNewBooking(1, 2, 7, '2023-11-03', '17:55:00'); -- booking will run over close time



/* UPDATE EXISTING BOOKINGS - update existing data in bookings table by calling stored procedure created above,
in the format: CALL UpdateBooking(booking_id, customer_id, stylist_id, treatment_id, booking_date, booking_time); */

-- see all bookings BEFORE updating booking:

CREATE VIEW booking_list_by_id AS
SELECT * FROM bookings
ORDER BY id;
SELECT * FROM booking_list_by_id; 

-- now update bookings:
CALL UpdateBooking(1, 1, 1, 1, '2023-11-01', '09:30:00'); 
-- These queries underneath will not work as they fail coniditions set in procedure. Uncomment to try:
-- CALL UpdateBooking(2, 2, 1, 3, '2023-11-01', '11:05:00');  -- clashes with an existing booking
-- CALL UpdateBooking(3, 3, 1, 5, '2023-11-02', '14:15:00'); -- clashes with an existing booking
-- CALL UpdateBooking(5, 5, 1, 7, '2023-11-02', '13:15:00'); -- cclashes with an existing booking
-- CALL UpdateBooking(5, 5, 2, 1, '2023-11-06', '14:00:00'); -- booking time isn't within open and close time
-- CALL UpdateBooking(6, 6, 2, 10, '2023-11-04', '17:45:00'); -- booking will run over close time

-- finally, see all bookings AFTER updating booking:
SELECT * FROM booking_list_by_id; 


/* CANCEL(DELETE) EXISTING BOOKINGS - delete existing data in bookings table by calling stored procedure created above,
in the format: CALL CancelBooking(booking_id); */

-- see all bookings BEFORE cancellation
SELECT * FROM booking_list_by_id; -- see the VIEW

CALL CancelBooking(10);
-- These queries underneath will not work as they fail coniditions set in procedure. Uncomment to try:
-- CALL CancelBooking(50); -- booking does not exist

-- see all bookings AFTER cancellation
SELECT * FROM booking_list_by_id;-- see the VIEW


/* SEE ALL OF A STYLIST'S SCHEDULED BOOKINGS FOR A GIVEN DAY */
CALL GetStylistSchedule(1, '2023-11-01'); -- has two bookings
CALL GetStylistSchedule(2, '2023-11-03'); -- has two bookings
CALL GetStylistSchedule(2, '2023-11-02'); -- has no bookings for this day, so result is empty

-- See all data from tables:
SELECT * FROM customers;
SELECT * FROM stylists;
SELECT * FROM treatments;
SELECT * FROM salon_info;
SELECT * FROM opening_times;
SELECT * FROM bookings;

    