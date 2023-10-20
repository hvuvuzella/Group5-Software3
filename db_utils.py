import mysql.connector
from flask import jsonify
from mysql.connector import errorcode

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


def add_new_client(first_name, last_name, mobile, email):
    try:
        db_name = 'hair_salon'
        db_connection = _connect_to_db(db_name)
        cursor = db_connection.cursor()
        print(f'Connected to database: {db_name}')

        # execute query
        insert_query = "INSERT INTO clients (first_name, last_name, mobile, email) VALUES (%s, %s, %s, %s)"
        client_data = (first_name, last_name, mobile, email)

        cursor.execute(insert_query, client_data)
        db_connection.commit()

        # Get the last inserted ID
        client_id = cursor.lastrowid

        cursor.close()

        print(f"Client added to the database successfully. Client ID: {client_id}")
        print("Please make note of your client ID, so you can make appointments!")

    except Exception:
        raise DbConnectionError("Failed to insert data to DB")

    finally:
        if db_connection:
            db_connection.close()
            print("DB connection is closed")

    return {"client_id": client_id}

def insert_new_appointment(client_id, stylist_id, treatment_id, appt_date, appt_time):
    try:
        db_name = 'hair_salon'
        db_connection = _connect_to_db(db_name)
        cursor = db_connection.cursor()
        print(f'Connected to database: {db_name}')

        # Define the SQL query to call the stored procedure
        procedure_call = "CALL InsertNewAppointment(%s %s %s %s %s)"
        appointment_data = (client_id, stylist_id, treatment_id, appt_date, appt_time)

        cursor.callproc("InsertNewAppointment", appointment_data)
        db_connection.commit()

        # Fetch the last inserted ID using LAST_INSERT_ID()
        cursor.execute("SELECT LAST_INSERT_ID()")
        appointment_id = cursor.fetchone()[0]

        cursor.close()

        if appointment_id is not None:
            print(f"New appointment added successfully. Appointment ID: {appointment_id}")
            print("Please make note of your appointment ID in case you want to update/cancel your appointments!")
        else:
            print("Failed to retrieve appointment ID. Please check your database and stored procedure.")

    except Exception:
        raise DbConnectionError("Failed insert data to DB")

    finally:
        if db_connection:
            db_connection.close()
            print("DB connection is closed")


def update_appointment(appointment_id, client_id, stylist_id, treatment_id, appt_date, appt_time):
    try:
        db_name = 'hair_salon'
        db_connection = _connect_to_db(db_name)
        cursor = db_connection.cursor()
        print(f'Connected to database: {db_name}')

        # Define the SQL query to call the stored procedure
        procedure_call = "CALL UpdateAppointment(%s, %s, %s, %s, %s, %s)"
        appointment_data = (appointment_id, client_id, stylist_id, treatment_id, appt_date, appt_time)

        cursor.callproc("UpdateAppointment", appointment_data)
        db_connection.commit()

        print("Appointment updated successfully.")

    except Exception:
        raise DbConnectionError("Failed insert data to DB")

    finally:
        if db_connection:
            db_connection.close()
            print("DB connection is closed")


def cancel_appointment(appointment_id):
    try:
        db_name = 'hair_salon'
        db_connection = _connect_to_db(db_name)
        cursor = db_connection.cursor()
        print(f'Connected to database: {db_name}')

        # Define the SQL query to call the stored procedure
        procedure_call = "CALL CancelAppointment(%s)"
        appointment_data = (appointment_id,)

        cursor.callproc("CancelAppointment", appointment_data)
        db_connection.commit()

        cursor.close()

        print("Appointment cancelled successfully.")

    except Exception:
        raise DbConnectionError("Failed to cancel appointment")

    finally:
        if db_connection:
            db_connection.close()
            print("DB connection is closed")

#THIS WORKS!
def get_stylist_schedule(stylist_id, appointment_date):
    try:
        db_name = 'hair_salon'
        db_connection = _connect_to_db(db_name)
        cursor = db_connection.cursor()
        print(f'Connected to database: {db_name}')

        # Call the stored procedure
        cursor.callproc('GetStylistSchedule', [stylist_id, appointment_date])

        cursor.nextset()
        results = cursor.stored_results()
        result = results.__next__()
        rows = result.fetchall()

        cursor.close()

        if rows:
            for row in rows:
                print(row)
        else:
            print("No appointments found for the given date.")

    except Exception:
        raise DbConnectionError("Failed to read data from database")

    finally:
        if db_connection:
            db_connection.close()
            print("DB connection is closed")


def main():
    add_new_client("Helen", "Vu", "07772365887", "helen.vu@email.com")
    insert_new_appointment(11, 3, 3, '2023-12-06', '09:00:00')
    update_appointment(11, 11, 3, 3, '2023-12-06', '12:00:00')
    cancel_appointment(11)
    get_stylist_schedule(1, '2023-11-01')


if __name__ == '__main__':
    main()