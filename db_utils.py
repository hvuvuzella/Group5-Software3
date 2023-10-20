import mysql.connector

from config import USER, PASSWORD, HOST


class DbConnectionError(Exception):
    pass


def _connect_to_db(db_name):
    connection = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        auth_plugin='mysql_native_password',
        database=db_name
    )
    return connection


def add_new_customer(first_name, last_name, mobile, email):
    try:
        db_name = 'hair_salon'
        db_connection = _connect_to_db(db_name)
        cursor = db_connection.cursor()
        print(f'Connected to database: {db_name}')

        # execute query
        insert_query = "INSERT INTO customers (first_name, last_name, mobile, email) VALUES (%s, %s, %s, %s)"
        customer_data = (first_name, last_name, mobile, email)

        cursor.execute(insert_query, customer_data)
        db_connection.commit()

        # Get the last inserted ID
        customer_id = cursor.lastrowid

        cursor.close()

        print(f"Customer added to the database successfully. Customer ID: {customer_id}")
        print("Please make note of your customer ID, so you can make bookings!")

    except Exception:
        raise DbConnectionError("Failed to insert data to DB")

    finally:
        if db_connection:
            db_connection.close()
            print("DB connection is closed")


def add_new_booking(customer_id, stylist_id, treatment_id, booking_date, booking_time):
    try:
        db_name = 'hair_salon'
        db_connection = _connect_to_db(db_name)
        cursor = db_connection.cursor()
        print(f'Connected to database: {db_name}')

        # Define the SQL query to call the stored procedure
        procedure_call = "CALL AddNewBooking(%s %s %s %s %s)"
        booking_data = (customer_id, stylist_id, treatment_id, booking_date, booking_time)

        cursor.callproc("AddNewBooking", booking_data)
        db_connection.commit()

        # Fetch the last inserted ID using LAST_INSERT_ID()
        cursor.execute("SELECT LAST_INSERT_ID()")
        booking_id = cursor.fetchone()[0]

        cursor.close()

        if booking_id is not None:
            print(f"New booking added successfully. Booking ID: {booking_id}")
            print("Please make note of your booking ID in case you want to update/cancel your bookings!")
        else:
            print("Failed to retrieve booking ID. Please check your database and stored procedure.")

    except Exception:
        raise DbConnectionError("Failed insert data to DB")

    finally:
        if db_connection:
            db_connection.close()
            print("DB connection is closed")


def update_booking(booking_id, customer_id, stylist_id, treatment_id, booking_date, booking_time):
    try:
        db_name = 'hair_salon'
        db_connection = _connect_to_db(db_name)
        cursor = db_connection.cursor()
        print(f'Connected to database: {db_name}')

        # Define the SQL query to call the stored procedure
        procedure_call = "CALL UpdateBooking(%s, %s, %s, %s, %s, %s)"
        booking_data = (booking_id, customer_id, stylist_id, treatment_id, booking_date, booking_time)

        cursor.callproc("UpdateBooking", booking_data)
        db_connection.commit()

        print("Booking updated successfully.")

    except Exception:
        raise DbConnectionError("Failed insert data to DB")

    finally:
        if db_connection:
            db_connection.close()
            print("DB connection is closed")


def cancel_booking(booking_id):
    try:
        db_name = 'hair_salon'
        db_connection = _connect_to_db(db_name)
        cursor = db_connection.cursor()
        print(f'Connected to database: {db_name}')

        # Define the SQL query to call the stored procedure
        procedure_call = "CALL CancelBooking(%s)"
        booking_data = (booking_id,)

        cursor.callproc("CancelBooking", booking_data)
        db_connection.commit()

        cursor.close()

        print("Booking cancelled successfully.")

    except Exception:
        raise DbConnectionError("Failed to cancel booking")

    finally:
        if db_connection:
            db_connection.close()
            print("DB connection is closed")


# THIS WORKS!
def get_stylist_schedule(stylist_id, booking_date):
    try:
        db_name = 'hair_salon'
        db_connection = _connect_to_db(db_name)
        cursor = db_connection.cursor()
        print(f'Connected to database: {db_name}')

        # Call the stored procedure
        cursor.callproc('GetStylistSchedule', [stylist_id, booking_date])

        cursor.nextset()
        results = cursor.stored_results()
        result = results.__next__()
        rows = result.fetchall()

        cursor.close()

        if rows:
            for row in rows:
                print(row)
        else:
            print("No bookings found for the given date.")

    except Exception:
        raise DbConnectionError("Failed to read data from database")

    finally:
        if db_connection:
            db_connection.close()
            print("DB connection is closed")


def main():
    add_new_customer("Helen", "Vu", "07772365887", "helen.vu@email.com")
    add_new_booking(11, 3, 3, '2023-12-06', '09:00:00')
    update_booking(11, 11, 3, 3, '2023-12-06', '12:00:00')
    cancel_booking(11)
    get_stylist_schedule(1, '2023-11-01')


if __name__ == '__main__':
    main()