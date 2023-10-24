# Welcome to our API

Please see the information below for details on how to run our API.

---

## Files you will need

Please import the project into PyCharm. The files you will be using are:
- app.py
- main.py
- db_utils.py
- config.py

Please run the following file in MySQL Workbench:
- hair_salon.sql

---

## Set Up

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

To find these, open Workbench and under the **Administration** tab, click **Users and Privilages**. You will see a list of users that you can use. 

Next, go to the config.py file in PyCharm:
1. Insert your user from Workbench into the " " next to USER.
2. Insert the password associated with this user between the " " next to PASSSWORD

> **NOTE** The value in HOST does not need to be changed and should be left as "localhost" for this API

---

## Almost there, but before you begin...

You must create the database before going any further, by going to MySQL Workbench and running the hair_salon.sql file.

Next, you need to run the app.py file in PyCharm.

Once you have completed these steps, you are now ready to run the code and use the API!

## What to expect
As you navigate the API, there are a number of outcomes you should expect. See the flowchart below:
![Final Workflow](https://github.com/hvuvuzella/Group5-Software3/assets/145285143/8cd0f6f5-5ed4-4bcf-a068-5ba41b03fa18)

--- 
### Thank you for using our API, we hope you enjoy it! 😁