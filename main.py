import requests  # import module for requesting API
import json  # import module to work with json data
from db_utils import get_all_treatments  # import the module


# Sending request to the endpoint to get stylist schedule for specific date
def get_stylist_schedule_by_date(stylist, date):
    result = requests.get(
        "http://127.0.0.1:5000/schedule/{}/{}".format(stylist, date),
        headers={"content-type": "application/json"}
    )
    return result.json()


# Sending request to endpoint to add new client by sending an HTTP POST request with client information
def add_client(first_name, last_name, mobile, email):
    client_info = {
        "first_name": first_name,
        "last_name": last_name,
        "mobile": mobile,
        "email": email,
    }

    result = requests.post(
        "http://127.0.0.1:5000/add_new_client",
        headers={"content-type": "application/json"},
        data=json.dumps(client_info)
    )

    return result.json()


# Sending request to endpoint to get information about the customer's booking
def get_bookings(customer_id):
    user_bookings = requests.get(
        "http://127.0.0.1:5000/bookings/{}".format(customer_id),
        headers={"content-type": "application/json"}
    )
    return user_bookings.json()


# Sending request to endpoint to add new appointment
def add_booking(customer_id, stylist_id, treatment_id, booking_date, booking_time):
    booking = {
        "customer_id": customer_id,
        "stylist_id": stylist_id,
        "treatment_id": treatment_id,
        "booking_date": booking_date,
        "booking_time": booking_time
    }

    result = requests.post(
        "http://127.0.0.1:5000/add_new_booking",
        headers={"content-type": "application/json"},
        data=json.dumps(booking)
    )

    return result.json()


# Sending request to endpoint to cancel appointment
def cancel_booking(booking_id):
    result = requests.delete(
        "http://127.0.0.1:5000/cancel_booking/{}".format(booking_id),
        headers={"content-type": "application/json"},
    )
    print("Success")

    return result


# Main function that runs all the requests depending on user's choice
def run():
    stylist_or_customer = input("\n*************************************************************************"
                                "\nWelcome to THE CUT, where you can get all of your hair needs in one place"
                                "\n*************************************************************************"
                                "\n\nTo start, you can log in as a STYLIST to view your booking schedules by date,"
                                "\nOR log in as a CUSTOMER to create an account, and create or cancel your bookings."
                                "\n\nPlease choose one of the following options: type S for STYLIST, or C for "
                                "CUSTOMER: ")

    # If the user logs in as a stylist, they can check their schedule for a specific date
    if stylist_or_customer == "S" or stylist_or_customer == "s":
        stylist_to_check_schedule = input("Please choose whose booking schedule you'd like to see:\n"
                                          "Type 1 for Erika, 2 for Hannah, or 3 for Kate's schedule. ")
        date_to_check_schedule = input("Please enter the date of the bookings you'd like to see in YYYY-MM-DD format"
                                       "\n p.s. the salon is closed on Mondays and Tuesdays: ")
        stylist_schedule = get_stylist_schedule_by_date(stylist_to_check_schedule, date_to_check_schedule)
        if len(stylist_schedule["data"]) == 0:
            print("There are currently no bookings scheduled for this date.")
        else:
            stylist_bookings = []
            for booking in stylist_schedule["data"]:
                stylist_bookings.append(
                    f"Customer name: {booking['name']} {booking['last_name']}, Mobile: {booking['phone']}, Treatment: {booking['treatment']}, Time slot: {booking['time']}.\n"
                )
            print(f"You have the following bookings for this date:\n{''.join(stylist_bookings)}")

    # If the user logs in as a customer, they are prompted to register by providing their information
    if stylist_or_customer == "C" or stylist_or_customer == "c":
        registered_user = input("Are you a registered customer?(Y/N): ")
        if registered_user == "N" or registered_user == "n":
            client_name = input(
                "No worries! To register, we'll just need a few details from you. What's your first name? ")
            client_last_name = (input("Your last name? "))
            client_mobile = (input("You mobile number? "))
            client_email = (input("And lastly, you email address? "))
            customer_id = add_client(client_name, client_last_name, client_mobile, client_email)
            print(
                f"Fab! You are now signed up, with a customer ID of: {customer_id['customer_id']}. "
                f"\nPlease mate note of this customer ID so that you can view, create and cancel your bookings :)")
        elif registered_user == "Y" or registered_user == "y":
            customer_choice = input(
                "\nWelcome back! Would you like to view your bookings (view), make a new booking (book), or cancel an "
                "existing booking (cancel)?"
                "\nChoose by typing 'view', 'book' or cancel' ")
            if customer_choice == "view":
                reg_customer_id = input("\nPlease enter your CUSTOMER ID: ")
                bookings = get_bookings(reg_customer_id)
                all_bookings = []
                for booking in bookings["data"]:
                    all_bookings.append(
                        f"<Name: {booking['name']} {booking['last_name']} - "
                        f"Treatment: {booking['treatment']} - Date: {booking['date']} - Time: {booking['time']}>"
                        f" || <CUSTOMER ID: {booking['app_id']}, BOOKING ID: {booking['app_id']}>"
                        f"\n\np.s. Please make note of your customer & booking IDs for future use! (e.g. to make or "
                        f"cancel bookings)")
                print(f'\nYOUR BOOKINGS:\n\n{". ".join(all_bookings)}')
            elif customer_choice == "book":
                customer_id = int(input("Enter your customer id: "))
                stylist_id = int(
                    input("\nInput 1 if you want to choose Erika Tatchyn, 2 - Hannah Magee and 3 - Kate Losyeva: "))
                print("\nList of treatments:")
                get_all_treatments()
                treatment_id = int(input("\nEnter the id of treatment (for example, 5): "))
                booking_date = input(
                    "\nEnter the desirable date in format YYYY-MM-DD (we are off on Mondays and Tuesdays): ")
                stylist_schedule = get_stylist_schedule_by_date(stylist_id, booking_date)
                if len(stylist_schedule['data']) == 0:
                    print(f"\nThis stylist has no bookings scheduled on {booking_date}")
                else:
                    stylist_bookings = []
                    for booking in stylist_schedule["data"]:
                        stylist_bookings.append(
                            f"time slot: {booking['time']}.\n")
                    print(f'\nThis stylist has the following bookings  on {booking_date}:\n{"".join(stylist_bookings)}')
                print("""Our working hours:
                09:00 - 18:00 We, Th, Fr
                10:00 - 18:00 Sa
                12:00 - 17:00 Su""")
                booking_time = input(
                    "\nEnter the time to book in format hh:mm. (There should be at least 5 min interval between "
                    "bookings so the stylists can prepare their stations between bookings!) ")
                booking_time = booking_time + ':00'
                booking_id = add_booking(customer_id, stylist_id, treatment_id, booking_date, booking_time)
                print(f"\nCongratulations! You are registered. Your appointment is on {booking_date} at {booking_time}")
                print(
                    f"Your booking ID is {booking_id['Booking_id']}. Please make note of this booking ID so that you can cancel your booking if needed")
            elif customer_choice == "cancel":
                booking_id = input("Enter your appointment id: ")
                result = cancel_booking(booking_id)
                print(result)


if __name__ == '__main__':
    run()
    # add_booking(2, 1, 2, '2023-12-22', '09:00')
