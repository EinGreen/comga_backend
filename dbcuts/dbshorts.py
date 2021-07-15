import mariadb
import dbconnect
import traceback
import string
import random
import hashlib

# For GET
def run_selection(statement, params):
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    result = None

    try:
        cursor.execute(statement, params)
        result = cursor.fetchall()
    except mariadb.OperationalError:
        traceback.print_exc()
        print("mariadb does not understand the request")
    except IndexError:
        traceback.print_exc()
        print("could not find")
    except:
        traceback.print_exc()
        print("Some error has occured, I don't freakin know dude")
    dbconnect.close_all(cursor, conn)
    return result

# For POST
def run_insertion(statement, params):
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    result = None

    try:
        cursor.execute(statement, params)
        conn.commit()
        result = cursor.lastrowid
    except mariadb.DataError:
        print("Bad Request, Database Error")
    except FileNotFoundError:
        print("Invalid request, was not found on the server")
    except:
        traceback.print_exc()
        print("Unknown Error has occured")
    dbconnect.close_all(cursor, conn)
    return result

# For DELETE
def run_deletion(statement, params):
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    result = None

    try:
        cursor.execute(statement, params)
        conn.commit()
        result = cursor.rowcount
    except mariadb.ProgrammingError:
        print("Could not find Table")
    except:
        traceback.print_exc()
        print("Nani? Bakana, I can't delete?")
    dbconnect.close_all(cursor, conn)
    return result

# For PATCH
def run_update(statement, params):
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    result = None

    try:
        cursor.execute(statement, params)
        conn.commit()
        result = cursor.rowcount
    except:
        traceback.print_exc()
        print("Uh oh, I can't update for some reason")
    dbconnect.close_all(cursor, conn)
    return result

# For salt
def create_salt():
    letters_and_digits = string.ascii_letters + string.digits
    salt = ''.join(random.choice(letters_and_digits) for i in range(10))
    return salt

def get_salt(username):
    user = run_selection("select salt from users where username=?", [username,])
    if(len(user) == 1):
        return user[0][0]
    else:
        print("no salt")
        return ''

def create_hash_pass(salt, password):
    user_pass = salt + password
    hash_pass = hashlib.sha512(user_pass.encode()).hexdigest()
    return hash_pass

def get_hash_pass(username, password):
    salt = get_salt(username)
    user_pass = salt + password
    hash_pass = hashlib.sha512(user_pass.encode()).hexdigest()
    return hash_pass