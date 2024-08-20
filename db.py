import sqlite3 as sl
from request import check_availability

def init_db(): #CRUD init
    con = sl.connect('main_database.db') 
    with con:
        con.execute("""
        CREATE TABLE IF NOT EXISTS links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            name TEXT,
            availability STRING
        );
        """)
    con.close()


def delete_link(id): #CRUD DELETE
    con = sl.connect('main_database.db')
    sql = 'DELETE FROM links WHERE id = ?'
    data = (id)
    with con:
        con.execute(sql, data)
    con.close()

def insert_link(url, name, availability):
    con = sl.connect('main_database.db')
    try:
        sql = 'INSERT INTO links (url, name, availability) VALUES (?, ?, ?)'
        data = (url, name, availability)
        cursor = con.cursor()
        cursor.execute(sql, data)
        link_id = cursor.lastrowid
        con.commit()
    
    finally:
        con.close()
    return link_id
    
def insert_user(tg_id, username): #CRUD INSERT
    con = sl.connect('main_database.db')
    try:
        sql = 'INSERT INTO users (id, username) VALUES (?, ?)'
        data = (tg_id, username)
        with con:
            con.execute(sql, data)
    except Exception as e:
        print('user is already into db')
    finally:
        con.close()

def insert_links_to_users(user_id, link_id): #CRUD INSERT
    con = sl.connect('main_database.db')
    sql = 'INSERT INTO links_to_users (user_id, link_id) VALUES (?, ?)'
    data = (user_id, link_id)
    with con:
        con.execute(sql, data)
    con.close()

def delete_links_to_users(id): #CRUD DELETE
    con = sl.connect('main_database.db')
    sql = 'DELETE FROM links_to_users WHERE link_id = ?'
    data = (id)
    with con:
        con.execute(sql, data)
    con.close()

def update_availability(id, availability): #CRUD
    con = sl.connect('main_database.db')
    sql = 'UPDATE links SET availability = ? WHERE id = ?'
    data = (availability, id)
    with con:
        con.execute(sql, data)
    con.close()

def update_record(id, name): #CRUD подумать как сделать одно действие для всех
    con = sl.connect('main_database.db')
    sql = 'UPDATE links SET name = ? WHERE id = ?'
    data = (name, id)
    with con:
        con.execute(sql, data)
    con.close()

def update_every_morning():
    try:
        with sl.connect('main_database.db') as con:
            cursor = con.cursor()
            cursor.execute('SELECT id, url FROM links')
            for row in cursor.fetchall():
                id = row[0]
                url = row[1]
                availability = check_availability(url)
                update_availability(id, availability)
                print(url, id, availability)
    except Exception as e:
        print(f"An error occurred: {e}")