import requests # import module for requesting API
import json # import module to work with json data
from db_utils import get_all_treatments # import the module


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
    stylist_or_customer = input("Welcome to our hair salon where you can get everything you need for your hair.\nPrint "
                                "s if you want to log in as a stylist and c if you want to log in as a customer. ")
    
    # If the user logs in as a stylist, they can check their schedule for a specific date
    if stylist_or_customer == "s":
        stylist_to_check_schedule = input("Type 1 if you want to check schedule for Erika Tatchyn,"
                                          " 2 for Hannah Magee and 3 for Kate Losyeva. ")
        date_to_check_schedule = input("What date do you want to check your schedule for?(YYYY-MM-DD) ")
        stylist_schedule = get_stylist_schedule_by_date(stylist_to_check_schedule, date_to_check_schedule)
        if len(stylist_schedule["data"]) == 0:
            print("You have no appointments booked.")
        else:
            stylist_bookings = []
            for booking in stylist_schedule["data"]:
                stylist_bookings.append(
                    f"{booking['name']} {booking['last_name']} (phone {booking['phone']}) - booking for {booking['treatment']}, time slot: {booking['time']}.\n"
                    )
            print(f"You have the following bookings:\n{''.join(stylist_bookings)}")
    
    # If the user logs in as a customer, they are prompted to register by providing their information
    if stylist_or_customer == "c":
        registered_user = input("Are you a registered user?(y/n): ")
        if registered_user == "n":
            client_name = input("To continue with your appointments you will be asked to register. Enter your first name: ")
            client_last_name = (input("Enter your last name: "))
            client_mobile = (input("Enter your mobile number: "))
            client_email = (input("Enter your email: "))
            customer_id = add_client(client_name, client_last_name, client_mobile, client_email)

            print(f"Congratulations! You are registered with an id {customer_id['customer_id']}. Use this id to make, update and delete your appointments.")
        elif registered_user == "y":
            customer_choice = input("If you want to view your bookings type 'b', if you want to add a new booking type 'n',"
                                    " if you want to delete your booking type 'd': " )
            if customer_choice == "b":
                reg_customer_id = input("Enter your customer id, please: ")
                bookings = get_bookings(reg_customer_id)
                all_bookings = []
                for booking in bookings["data"]:
                    all_bookings.append(f"{booking['name']} {booking['last_name']} (customer id {booking['app_id']}) - booking for {booking['treatment']} with booking id {booking['app_id']} for {booking['date']} at {booking['time']}")
                print(f'Your bookings are:\n{". ".join(all_bookings)}')
            elif customer_choice == "n":

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
                    print(f"\nThis stylist has no appointments booked on {booking_date}")
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
                booking_time = input("\nEnter the time to book in format hh:mm. (There should be at least 5 min interval beetween appointments to prepare your place!) ")
                booking_time = booking_time + ':00'
                add_booking(customer_id, stylist_id, treatment_id, booking_date, booking_time)
                print(f"\nCongratulations! You are registered. Your appointment is on {booking_date} at {booking_time}")
            elif customer_choice == "d":
                booking_id = input("Enter your appointment id: ")
                result = cancel_booking(booking_id)
                print(result)


if __name__ == '__main__':
    run()
    #add_booking(2, 1, 2, '2023-12-22', '09:00')
