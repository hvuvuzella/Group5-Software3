import requests # import module for requesting API
import json # import module to work with json data

# Define a function that sends request to the endpoint to get stylist schedule for specific date

def get_stylist_schedule_by_date(stylist, date):
    result = requests.get(
        'http://127.0.0.1:5000/schedule/{}/{}'.format(stylist, date),
        headers={'content-type': 'application/json'}
    )
    return result.json()


# Define a function that send request to endpoint to add new client by sending an HTTP POST request with client information

def add_client(first_name, last_name, mobile, email):
    client_info = {
        "first_name": first_name,
        "last_name": last_name,
        "mobile": mobile,
        "email": email,
    }

    result = requests.post(
        'http://127.0.0.1:5000/add_new_client',
        headers={'content-type': 'application/json'},
        data=json.dumps(client_info)
    )

    return result.json()



def get_bookings(first_name, last_name):
    user_bookings = requests.get(
        'http://127.0.0.1:5000/bookings/{}/{}'.format(first_name, last_name),
        headers={'content-type': 'application/json'}
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
        'http://127.0.0.1:5000/add_new_booking',
        headers={'content-type': 'application/json'},
        data=json.dumps(booking)
    )

    return result.json()

# Sending request to endpoint to cancel appointment
def cancel_booking(booking_id):
    result = requests.delete(
        'http://127.0.0.1:5000/cancel_booking/{}'.format(booking_id),
        headers={'content-type': 'application/json'},
    )
    print('Success')

    return result

# Main function that runs all the requests depending on user's choice

def run():
    stylist_or_customer = input("Welcome to our hair salon where you can get everything you need for your hair.\nPrint "
                                "s if you want to log in as a stylist and c if you want to log in as a customer.")
    
    # If the user logs in as a stylist, they can check their schedule for a specific date
    if stylist_or_customer == "s":
        stylist_to_check_schedule = input("Type 1 if you want to check schedule for Erika Tatchyn,"
                                          " 2 for Hannah Magee and 3 for Kate Losyeva.")
        date_to_check_schedule = input("What date do you want to check your schedule for?(YYYY-MM-DD)")
        stylist_schedule = get_stylist_schedule_by_date(stylist_to_check_schedule, date_to_check_schedule)
        if len(stylist_schedule['data']) == 0:
            print("You have no appointments booked")
        else:
            stylist_bookings = []
            for booking in stylist_schedule["data"]:
                stylist_bookings.append(
                    f"{booking['name']} {booking['last_name']} (phone {booking['phone']}) - booking for {booking['treatment']}, time slot: {booking['time']}.\n")
            print(f'You have the following bookings:\n{"".join(stylist_bookings)}')
    # If the user logs in as a customer, they are prompted to register by providing their information
    if stylist_or_customer == "c":
        registered_user = input("Are you a registered user?(y/n)")
        if registered_user == "n":
            client_name = input(
                "To continue with your appointments you will be asked to register. Enter your first name")
            client_last_name = (input("Enter your last name"))
            client_mobile = (input("Enter your mobile number"))
            client_email = (input("Enter your email"))
            client_id = add_client(client_name, client_last_name, client_mobile, client_email)

            print(
                f"Congratulations! You are registered with an id {client_id['customer_id']}. Use this id to make, update and delete your appointments.")
        elif registered_user == "y":
            reg_user_name = input("Enter your first name, please")
            reg_user_last_name = input("Enter your last name, please")
            bookings = get_bookings(reg_user_name, reg_user_last_name)

            all_bookings = []
            for booking in bookings["data"]:
                all_bookings.append(f"{booking['name']} {booking['last_name']} (customer id {booking['app_id']}) - booking for {booking['treatment']} with booking id {booking['app_id']} for {booking['date']} at {booking['time']}")
            print(f'Your bookings are:\n{". ".join(all_bookings)}')


        customer_choice = input("Type a if you want to add appointment,"
                                " d if you want to cancel appointment.")
        if customer_choice == "d":
          booking_id = input("Enter your appointment id: ")
          result = cancel_booking(booking_id)
          print(result)
        elif customer_choice == "a":
            customer_id = int(input("Enter your customer id: "))
            stylist_id = int(input("Type 1 if you want to check schedule for Erika Tatchyn, 2 for Hannah Magee and 3 for Kate Losyeva: "))
            treatment_id = int(input("Enter the id of treatment (from 1 to 10: "))
            booking_date = input("Enter the date in format YYYY-MM-DD: ")
            booking_time = input("Enter the time to book in format hh:mm ")
            booking_time = booking_time + ':00'
            add_booking(customer_id, stylist_id, treatment_id, booking_date, booking_time)
            print("Congratulations! You are registered with an id {booking_id}. Use this id to make, update and delete your appointments.")


if __name__ == '__main__':
    run()
    #add_booking(2, 1, 2, '2023-10-23', '09:00')
