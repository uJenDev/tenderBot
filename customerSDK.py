
import sqlite3
import datetime

database_name = 'tenderbot.db'

def add_customer(drinkType, xPos, yPos):

    date = datetime.datetime.now()

    try:
        conx = sqlite3.connect(database_name)
        cursor = conx.cursor()

        new_customer = (drinkType, xPos, yPos, date)
        sql = "INSERT INTO customers (drinkType, xPos, yPos, date) VALUES (?, ?, ?, ?)"

        cursor.execute(sql, new_customer)
        conx.commit()
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        conx.close()

def delete_customer(id):

    try:
        conx = sqlite3.connect(database_name)
        cursor = conx.cursor()

        sql = "DELETE FROM customers WHERE id=?"
        cursor.execute(sql, (id,))
        conx.commit()
        print("Customer successfully deleted")
    except sqlite3.Error as error:
        print("Failed to delete customer", error)
    finally:
        conx.close()

def get_customers():
    try:
        conx = sqlite3.connect(database_name)
        cursor = conx.cursor()

        sql = "SELECT * FROM customers"
        cursor.execute(sql)
        customers = cursor.fetchall()
        return customers

    except sqlite3.Error as error:
        print("Failed to get data from sqlite table", error)
    finally:
        conx.close()