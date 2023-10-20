import mysql.connector
from config import HOST, USER, PASSWORD


def _connect_to_db(db_name):
    cnx = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        auth_plugin='mysql_native_password',
        database=db_name
    )

    return cnx


def get_stylist_availability(stylist_id, booking_date):
    availability = []
    try:
        db_name = 'hair_salon'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        print(f"Connected to database {db_name}")

        args = [stylist_id, booking_date]
        cur.callproc('GetStylistSchedule', args)

        for result in cur.stored_results():
            print(result.fetchall())

        cur.close()

    except Exception as exc:
        print(exc)

    finally:
        if db_connection:
            db_connection.close()
            print("Connection closed")


def add_booking(customer_id, stylist_id, treatment_id, booking_date, booking_time):
    try:
        db_name = 'hair_salon'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        print(f"Connected to database {db_name}")

        args = [customer_id, stylist_id, treatment_id, booking_date, booking_time]
        cur.callproc('AddNewBooking', args)

        db_connection.commit()
        cur.close()

    except Exception as exc:
        print(exc)

    finally:
        if db_connection:
            db_connection.close()
            print("Connection closed")


# add_booking(5, 1, 2, '2023-11-01', '10:00:00')
get_stylist_availability(1, '2023-11-01')
