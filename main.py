import requests
import json

# Sending request to endpoint to get stylist schedule
def get_stylist_schedule_by_date(stylist, date):
    result = requests.get(
        'http://127.0.0.1:5000/schedule/{}/{}'.format(stylist, date),
        headers={'content-type': 'application/json'}
    )
    return result.json()

# Sending request to endpoint to get add new user
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

# Main function that runs all the requests depending on user's choice
def run():
    stylist_or_customer = input("Welcome to our hair salon where you can get everything you need for your hair.\nPrint "
                                "s if you want to log in as a stylist and c if you want to log in as a customer.")
    if stylist_or_customer == "s":
        stylist_to_check_schedule = input("Type 1 if you want to check schedule for Erika Tatchyn,"
                                          " 2 for Hannah Magee and 3 for Kate Losyeva.")
        date_to_check_schedule = input("What date do you want to check your schedule for?(YYYY-MM-DD)")
        stylist_schedule = get_stylist_schedule_by_date(stylist_to_check_schedule, date_to_check_schedule)
        if len(stylist_schedule['booked slots']) == 0:
            print("You have no appointments booked")
        else:
            print(f"You have the following slots booked: {', '.join(stylist_schedule['booked slots'])}")
    if stylist_or_customer == "c":
        registered_user = input("Are you a registered user?(y/n)")
        if registered_user == "n":
            client_name = input("To continue with your appointments you will be asked to register. Enter your first name")
            client_last_name = (input("Enter your last name"))
            client_mobile = (input("Enter your mobile number"))
            client_email = (input("Enter your email"))
            client_id = add_client(client_name, client_last_name, client_mobile, client_email)
            print(
                f"Congratulations! You are registered with an id {client_id['client_id']}. Use this id to make, update and delete your appointments.")
        elif registered_user == "y":
            pass



if __name__ == '__main__':
    run()