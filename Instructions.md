# Welcome to our API

## What our API does
We have created a hair salon booking system/schedule viewing API for a salon called "THE CUT".

This API allows users to do a few things:

- Both stylists and Customers can use the API
- For Stylists, the API allows them to view their own booking schedules on a given date
- For Customers, the API allows them to register an account, make new bookings, view existing bookings, and cancel existing bookings as well
- For each Customer who signs up, a customer ID is created, and their full names, mobile numbers and email addresses are stored in the DB
- For every booking made, a booking ID is created, and the information for the customer's name, stylist's name, treatment, 
booking date and time are saved to the DB.



Please see the information below for details on how to run our API:

---

First, in your terminal, navigate to a folder on your machine where you would like to clone this project's GitHub repository to.
Go ahead and clone the repository by using the terminal command `git clone <SSH KEY>`. Now open up the repository in PyCharm CE.

## Files you will need

After you have opened the project in PyCharm CE, the files you will be using are:
- app.py
- main.py
- db_utils.py
- config.py

Please run the following file in MySQL Workbench:
- hair_salon.sql

---

## Set Up
You will need to have Python 3.11 installed.

You will also need pipenv installed.

In PyCharm CE, make sure the Project Interpreter is set to Python 3.11 in Pycharm settings.

You will require the following packages to run our API:
- flask
- requests
- json
- mysql.connector

To install the packages, open the terminal in **PyCharm**. 
Make sure you are in your `pipenv` by typing `pipenv shell`.

Type `pip install <package name>`

Alternatively, you can install packages through Python Interpreter in your Settings menu.

You can find more information on installing packages [here](https://packaging.python.org/en/latest/tutorials/installing-packages/).

---

## Getting Started

Before you can run the API, you need to connect the python code to the hair_salon.sql database using a Host, User and Password. 

To find these, open Workbench and under the **Administration** tab, click **Users and Privileges**. You will see a list of users that you can use. 

Next, go to the config.py file in PyCharm:
1. Insert your user from Workbench into the " " next to USER.
2. Insert the password associated with this user between the " " next to PASSWORD

> **NOTE** The value in HOST does not need to be changed and should be left as "localhost" for this API

---

## Almost there, but before you begin...

You must create the database before going any further, by going to MySQL Workbench and running the hair_salon.sql file.

Next, run the db_utils.py file to establish a connection between our Python code and the hair_salon.sql database. And in
this file, a number of SQL queries with exception handling are demonstrated.

Next, you need to run the app.py file in PyCharm CE to: initialise the Flask application, start up an HTTP server,
and set up our API endpoint routes via URL extensions. Running this file allows requests to be made to the API.

Once you have completed these steps, navigate to the Main.py file in PyCharm CE, right-click the code and click "Run Main.py".
You are now ready to interact with our API in the PyCharm console by following the on-screen prompts!

If you want to check how your interaction with the API has changed the data in the hair_salon.SQL database, feel free to run the relevant queries 
from within the SQL file. Enjoy!

## What to expect
As you navigate the API, there are a number of outcomes you should expect. See the flowchart below:
![Final API Workflow](https://github.com/hvuvuzella/Group5-Software3/assets/145285143/704ccc9f-d33b-499e-90c6-b8f63f2826b9)

--- 
### Thank you for using our API, we hope you enjoy it! 😁