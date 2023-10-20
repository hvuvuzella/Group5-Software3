import requests
import json

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
def run():
    print("Welcome to our hair salon where you can get everything you need for your hair")
    register_agree = input("To continue with your appointments you will be asked to register(y/n)")
    if register_agree == "y":
        client_name = (input("Enter your first name"))
        client_last_name = (input("Enter your last name"))
        client_mobile = (input("Enter your mobile number"))
        client_email = (input("Enter your email"))
    client_id = add_client(client_name, client_last_name, client_mobile, client_email)
    print(f"Congratulations! You are registered with an id {client_id['client_id']}. Use this id to make, update and delete your appointments.")

if __name__ == '__main__':
    run()