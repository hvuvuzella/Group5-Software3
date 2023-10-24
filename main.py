import requests  # import module for requesting API
import json  # import module to work with json data
from db_utils import get_all_treatments  # import the module


# Sending an HTTP GET request to the endpoint to get stylist schedule for specific date
def get_stylist_schedule_by_date(stylist, date):
    result = requests.get(
        "http://127.0.0.1:5000/schedule/{}/{}".format(stylist, date),
        headers={"content-type": "application/json"}
    )
    return result.json()


# Sending and HTTP POST request to endpoint to add new customer
def add_customer(first_name, last_name, mobile, email):
    customer_info = {
        "first_name": first_name,
        "last_name": last_name,
        "mobile": mobile,
        "email": email,
    }

    result = requests.post(
        "http://127.0.0.1:5000/add_new_customer",
        headers={"content-type": "application/json"},
        data=json.dumps(customer_info)
    )

    return result.json()


# Sending and HTTP GET request to endpoint to get information about the customer's booking
def get_bookings(customer_id):
    user_bookings = requests.get(
        "http://127.0.0.1:5000/bookings/{}".format(customer_id),
        headers={"content-type": "application/json"}
    )
    return user_bookings.json()


# Sending an HTTP POST request to endpoint to add new booking
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


# Sending and HTTP DELETE request to endpoint to cancel an existing booking
# def cancel_booking(customer_id, booking_id):
#     result = requests.delete(
#         "http://127.0.0.1:5000/cancel_booking/{}/{}".format(customer_id, booking_id),
#         headers={"content-type": "application/json"},
#     )
#     print("Booking cancelled successfully")
#
#     return result
def cancel_booking(customer_id, booking_id):
    url = "http://127.0.0.1:5000/cancel_booking/{}/{}".format(customer_id, booking_id)
    headers = {"content-type": "application/json"}

    try:
        result = requests.delete(url, headers=headers)
        result.raise_for_status()  # Raise an exception if the response status code indicates an error
        print("Booking canceled successfully")
        return result.text
    except requests.exceptions.RequestException as e:
        print(f"Failed to cancel booking: {e}")
        return str(e)


# Main function that runs all the requests depending on user's choice
def run():
    try:
        stylist_or_customer = input("\n*************************************************************************"
                                    "\nWelcome to THE CUT, where you can get all of your hair needs in one place"
                                    "\n*************************************************************************"
                                    "\n\nTo start, you can log in as a STYLIST to view your booking schedules by date,"
                                    "\nOR log in as a CUSTOMER to create an account, view, create or cancel your bookings."
                                    "\n\nPlease choose one of the following options: type S for STYLIST, or C for "
                                    "CUSTOMER: ")

        # If the user logs in as a stylist, they can check their schedule for a specific date
        if stylist_or_customer == "S" or stylist_or_customer == "s":
            stylist_to_check_schedule = input("Please choose whose booking schedule you'd like to see:\n"
                                              "Type 1 for Erika, 2 for Hannah, or 3 for Kate's schedule. ")
            if stylist_to_check_schedule < 1 or stylist_to_check_schedule > 3:
                exit()

            date_to_check_schedule = input("Just a reminder, we are closed on Mondays and Tuesdays!"
                                           "\nPlease enter the date of the bookings you'd like to see in YYYY-MM-DD "
                                           "format (e.g. 2023-11-01): ")
            stylist_schedule = get_stylist_schedule_by_date(stylist_to_check_schedule, date_to_check_schedule)
            if len(stylist_schedule["data"]) == 0:
                print("There are currently no bookings scheduled for this date.")
            else:
                stylist_bookings = []
                for booking in stylist_schedule["data"]:
                    stylist_bookings.append(
                        f"Customer name: {booking['name']} {booking['last_name']}, Mobile: {booking['phone']}, Treatment: {booking['treatment']}, Time slot: {booking['time']}.\n"
                    )
                print(f"\nYou have the following bookings for this date:\n\n{''.join(stylist_bookings)}")
                print("To login as a Customer, please restart and login again :)")

        # If the user logs in as a customer, they are prompted to register by providing their information
        elif stylist_or_customer == "C" or stylist_or_customer == "c":
            registered_user = input("Are you a registered customer?(Y/N): ")

            if registered_user == "N" or registered_user == "n":
                first_name = input(
                    "No worries! To register, we'll just need a few details from you. What's your first name? ")
                last_name = (input("Your last name? "))
                mobile = (input("You mobile number? "))
                email = (input("And lastly, your email address? "))
                customer_id = add_customer(first_name, last_name, mobile, email)
                print(
                    f"\nFab! You are now signed up, with a customer ID of: {customer_id['customer_id']}. "
                    f"\n\nPlease make note of this customer ID so that you can view, create and cancel your bookings."
                    f"\n\nTo view, create or cancel bookings, please restart and login again as an existing customer!")

            elif registered_user == "Y" or registered_user == "y":
                customer_choice = input(
                    "\nWelcome back! Would you like to view your bookings (view), make a new booking (book), or cancel an "
                    "existing booking (cancel)?"
                    "\nChoose by typing 'view', 'book' or cancel' ")

                if customer_choice == "view":
                    reg_customer_id = input("\nPlease enter your CUSTOMER ID: ")
                    bookings = get_bookings(reg_customer_id)

                    if len(bookings["data"]) == 0:
                        print("\nYou currently have no bookings with us. Feel free to login again to make a booking!")

                    else:
                        all_bookings = []
                        for booking in bookings["data"]:
                            all_bookings.append(
                                f"\n<Customer Name: {booking['first_name']} {booking['last_name']} - "
                                f"Treatment: {booking['treatment']} - Stylist: {booking['stylist_name']} - Date: {booking['date']} - Time: {booking['time']}>"
                                f" || <CUSTOMER ID: {reg_customer_id}, BOOKING ID: {booking['booking_id']}>")
                        print(f"\nYOUR BOOKINGS:"
                              f"\np.s. Please make note of your customer & booking IDs for future use! (e.g. to make or "
                              f"cancel bookings)"
                              f"\n{'. '.join(all_bookings)}"
                              f"\n\nTo cancel any of these bookings, please login again and follow the on-screen "
                              f"instructions")

                elif customer_choice == "book":
                    customer_id = int(input("Enter your CUSTOMER ID: "))
                    stylist_id = int(
                        input("\nPlease choose which stylist you'd like to book with. "
                              "Type 1 for Erika, 2 for Hannah, or 3 for Kate: "))
                    print("\nChoose one of the below treatments:")
                    get_all_treatments()
                    treatment_id = int(input("\nMake your choice by entering a number between 1-10 (e.g For Wash, "
                                             "Cut & Blowdry, enter 5): "))
                    booking_date = input(
                        "\nEnter the date you'd like to book, in the format YYYY-MM-DD (p.s. we are CLOSED on Mondays and "
                        "Tuesdays): ")
                    stylist_schedule = get_stylist_schedule_by_date(stylist_id, booking_date)
                    print("""\nSALON OPENING HOURS:
                    09:00 - 18:00 (Wed, Thu, Fri)
                    10:00 - 18:00 (Sat)
                    12:00 - 17:00 (Sun)""")
                    if len(stylist_schedule['data']) == 0:
                        print(
                            f"\np.s. Your chosen stylist is totally free on this date. You can choose any time during "
                            f"opening hours for {booking_date}!")
                    else:
                        stylist_bookings = []
                        for booking in stylist_schedule["data"]:
                            stylist_bookings.append(
                                f"time slot: {booking['time']}.\n")
                        print(
                            f'\np.s. Your chosen stylist is NOT available during the below time slots, on {booking_date}:\n{"".join(stylist_bookings)}')

                    booking_time = input(
                        "\nPlease enter the time you'd like to book making sure its during opening hours, and doesn't "
                        "clash with your stylist's unavailable times, in the format HH:MM ")
                    booking_time = booking_time + ':00'
                    booking_id = add_booking(customer_id, stylist_id, treatment_id, booking_date, booking_time)
                    print(f"\nCongratulations! Booking confirmed. Your booking is on {booking_date} at {booking_time}")
                    print(
                        f"\nYour BOOKING ID is {booking_id['Booking_id']}. Please make note of this booking ID so that you "
                        f"can cancel your booking if needed!"
                        f"\n\nIf you'd like to view your bookings or make another booking, or cancel existing bookings, "
                        f"please login again and follow the on-screen instructions! :)")

                elif customer_choice == "cancel":
                    customer_id = input("Enter your customer id: ")
                    booking_id = input("Enter your booking id: ")
                    result = cancel_booking(customer_id, booking_id)

                    if "Booking cancelled successfully" in result:
                        print(f"Your booking with booking ID: {booking_id} was successfully cancelled.")
                    else:
                        print("Booking doesn't exist. Please enter a valid customer and booking ID.")

                else:
                    print("Invalid choice. Please enter 'view', 'book', or 'cancel'.")

            else:
                print("Invalid choice. Please enter 'Y' or 'N'.")

        else:
            print("Invalid choice. Please enter 'S' or 'C'.")

        # After each loop ends, check if the user wants to run the script again
        user_input = input("\nWould you like to restart and login again? (Y/N): ")
        if user_input == "Y" or user_input == "y":
            run()  # Re-run the script

    except Exception:
        print("Sorry, there was an error. Please try again, and make sure you follow the on-screen instructions.")


if __name__ == '__main__':
    run()
