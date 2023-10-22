# Welcome to our API

Please see the information below for details on how to run our API.

---

## Files you will need

Please open the following files in PyCharm:
- app.py
- main.py
- db_utils.py
- config.py

Please open the following files in MySQL Workbench:
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

Type `pip install <packge name>`

Alternatively, you can install packages through Python Interpreter in your Settings menu.

You can find more information on installing packages [here](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax).

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
![API Workflow](https://github.com/hvuvuzella/Group5-Software3/assets/145285143/ee6d784e-b531-46ca-a3bb-5457f9b380c5)

--- 
## Thank you for using our API, we hope you enjoy it! 😁