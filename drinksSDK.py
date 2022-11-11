
import sqlite3
import datetime

database_name = 'tenderbot.db'

def add_drink(drinkName, portions, buttonLink):

    if not type(portions) == int:
        raise Exception('[Portions] needs to be of integer type')
    
    date = datetime.datetime.now()

    try:
        conx = sqlite3.connect(database_name)
        cursor = conx.cursor()

        sql = f"SELECT id FROM drinks WHERE buttonLink=?"
        cursor.execute(sql, (buttonLink,))
        drinkID = cursor.fetchall()

        if drinkID:
            for ids in drinkID:
                sql = f"UPDATE drinks SET buttonLink=0 WHERE id=?"
                cursor.execute(sql, (ids[0], ))
                conx.commit()

        new_drink = (buttonLink, drinkName, portions, date)
        sql = "INSERT INTO drinks (buttonLink, name, portions, lastUsed) VALUES (?, ?, ?, ?)"

        cursor.execute(sql, new_drink)
        conx.commit()
        print('Drink successfully added')
        return True
    except sqlite3.Error as error:
        print("Failed to add drink: ", error)
        return False
    finally:
        conx.close()


def decrement_portion(loc, specifier='name'):
    try:
        conx = sqlite3.connect(database_name)
        cursor = conx.cursor()

        sql = f"SELECT portions FROM drinks WHERE {specifier}=?"
        cursor.execute(sql, (loc,))
        try:
            portions = cursor.fetchall()[0][0]
        except IndexError:
            return False
        if portions == 0:
            return False
        else:
            portions -= 1

        sql = f"UPDATE drinks SET portions=? WHERE {specifier}=?"
        cursor.execute(sql, (portions, loc))
        conx.commit()
        print("Drink successfully decremented")
        return True
    except sqlite3.Error as error:
        print("Failed to delete drink: ", error)
    finally:
        conx.close()

def check_portion(loc, specifier='name'):
    try:
        conx = sqlite3.connect(database_name)
        cursor = conx.cursor()

        sql = f"SELECT portions FROM drinks WHERE {specifier}=?"
        cursor.execute(sql, (loc,))
        try:
            portions = cursor.fetchall()[0][0]
        except IndexError:
            return False
        if portions == 0:
            return False
        else:
            return True
    except sqlite3.Error as error:
        print("Something happend: ", error)
    finally:
        conx.close()

def refill_portion(loc, refill_amount, specifier='name'):
    try:
        conx = sqlite3.connect(database_name)
        cursor = conx.cursor()

        sql = f"SELECT portions FROM drinks WHERE {specifier}=?"
        cursor.execute(sql, (loc,))

        portions = cursor.fetchall()
        if portions:
            portions = portions[0][0] + refill_amount
        else:
            return False
        
        sql = f"UPDATE drinks SET portions=? WHERE {specifier}=?"
        cursor.execute(sql, (portions, loc))
        conx.commit()
        print(f"{loc} successfully refilled")
        return True
    except sqlite3.Error as error:
        print(f"Failed to refill {loc}: ", error)
    finally:
        conx.close()

def update_buttonlink(loc, buttonlink, specifier='name'):
    try:
        conx = sqlite3.connect(database_name)
        cursor = conx.cursor()

        sql = f"SELECT id FROM drinks WHERE buttonLink=?"
        cursor.execute(sql, (buttonlink,))
        drinkID = cursor.fetchall()

        if drinkID:
            for ids in drinkID:
                sql = f"UPDATE drinks SET buttonLink=0 WHERE id=?"
                cursor.execute(sql, (ids[0], ))
                conx.commit()

        
        sql = f"UPDATE drinks SET buttonLink=? WHERE {specifier}=?"
        cursor.execute(sql, (buttonlink, loc))
        conx.commit()
        print(f"{loc} successfully changed")
        return True
    except sqlite3.Error as error:
        print(f"Failed to change {loc}: ", error)
        return False
    finally:
        conx.close()


def delete_drink(loc, specifier='id'):

    try:
        conx = sqlite3.connect(database_name)
        cursor = conx.cursor()

        if specifier == 'id':
            loc = int(loc)

        sql = f"DELETE FROM drinks WHERE {specifier}=?"
        cursor.execute(sql, (loc,))
        conx.commit()
        print("Drink successfully deleted")
    except sqlite3.Error as error:
        print("Failed to delete drink: ", error)
    finally:
        conx.close()

def get_drinks(in_use=False):
    try:
        conx = sqlite3.connect(database_name)
        cursor = conx.cursor()

        sql = '''SELECT * FROM drinks 
        WHERE buttonLink=1 
        OR buttonLink=2 OR buttonLink=3''' if in_use else 'SELECT * FROM drinks'
        cursor.execute(sql)
        drinks = cursor.fetchall()
        return drinks

    except sqlite3.Error as error:
        print("Failed to get drinks from table: ", error)
    finally:
        conx.close()