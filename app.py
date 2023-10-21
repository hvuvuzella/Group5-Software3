from flask import Flask, jsonify, request
from db_utils import get_stylist_schedule, add_new_customer, show_user_appointments

app = Flask(__name__)


# Getting information about stylist appointments for the day

# getting user's bookings
@app.route('/bookings/<name>/<lastname>')
def get_bookings(name, lastname):
    res = show_user_appointments(name, lastname)
    return jsonify({"data": res})


@app.route('/schedule/<stylist_id>/<date>')
def get_schedule(stylist_id, date):
    res = get_stylist_schedule(stylist_id, date)
    return jsonify({"data": res})



# Creating a new user in a database
@app.route('/add_new_client', methods=['POST'])
def add_client():
    client = request.get_json()
    client_id = add_new_customer(
        first_name=client['first_name'],
        last_name=client['last_name'],
        mobile=client['mobile'],
        email=client['email'],
    )

    return jsonify(client_id)


if __name__ == '__main__':
   app.run(debug=True)
