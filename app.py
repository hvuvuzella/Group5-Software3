from flask import Flask, jsonify, request
from db_utils import get_stylist_schedule, add_new_client

app = Flask(__name__)

# Sending user data for registration, returning user id
@app.route('/add_new_client', methods=['POST'])
def add_client():
    client = request.get_json()
    client_id = add_new_client(
        first_name=client['first_name'],
        last_name=client['last_name'],
        mobile=client['mobile'],
        email=client['email'],
    )

    return jsonify(client_id)


if __name__ == '__main__':
    app.run(debug=True)