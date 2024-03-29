from flask import Flask, jsonify, request  # imports specific objects and functions from the Flask web framework
from db_utils import get_stylist_schedule, add_new_customer, add_new_booking, cancel_booking, \
    show_user_appointments  # imports specific functions from a module db_utils

# Define a Flask web application
app = Flask(__name__)


# Getting information about customer id
@app.route("/bookings/<customer_id>")
def get_bookings(customer_id):
    res = show_user_appointments(customer_id)
    return jsonify({"data": res})


# Getting information for a chosen stylist's booking schedule on a chosen date
@app.route("/schedule/<stylist_id>/<date>")
# Calls the 'get_stylist_schedule' function with parameters stylist_id and date
# that returns result as a JSON response
def get_schedule(stylist_id, date):
    res = get_stylist_schedule(stylist_id, date)
    return jsonify({"data": res})


# Creating a new customer in the database
# Define a route to add a new customer to the database using POST method
@app.route("/add_new_customer", methods=["POST"])
def add_customer():
    # Accepts POST requests with JSON data containing customer information
    customer = request.get_json()
    # Calls  the 'add_new_customer' function with customer information and retrieves the new customer's ID
    # and returns created customer's ID as a JSON response
    customer_id = add_new_customer(
        first_name=customer["first_name"],
        last_name=customer["last_name"],
        mobile=customer["mobile"],
        email=customer["email"],
    )
    return jsonify(customer_id)


# Creating a new booking with POST method
@app.route("/add_new_booking", methods=["POST"])
def add_booking():
    booking = request.get_json()
    booking_id = add_new_booking(
        customer_id=booking["customer_id"],
        stylist_id=booking["stylist_id"],
        treatment_id=booking["treatment_id"],
        booking_date=booking["booking_date"],
        booking_time=booking["booking_time"]
    )
    return jsonify(booking_id)


# Cancelling an existing booking with DELETE method
@app.route("/cancel_booking/<customer_id>/<booking_id>", methods=["DELETE"])
def cancel_existing_booking(customer_id, booking_id):
    result = cancel_booking(customer_id, booking_id)
    return result


if __name__ == '__main__':
    app.run(debug=True)
