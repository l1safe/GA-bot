import sqlite3 as sl

def init_db(): #CRUD init
    con = sl.connect('links.db') 
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
    con = sl.connect('links.db')
    sql = 'DELETE FROM links WHERE id = ?'
    data = (id)
    with con:
        con.execute(sql, data)
    con.close()

def insert_link(url, name, availability): #CRUD INSERT
    con = sl.connect('links.db')
    sql = 'INSERT INTO links (url, name, availability) VALUES (?, ?, ?)'
    data = (url, name, availability)
    with con:
        con.execute(sql, data)
    con.close()

def update_availability(id, availability): #CRUD
    con = sl.connect('links.db')
    sql = 'UPDATE links SET availability = ? WHERE id = ?'
    data = (availability, id)
    with con:
        con.execute(sql, data)
    con.close()

def update_record(id, name): #CRUD подумать как сделать одно действие для всех
    con = sl.connect('links.db')
    sql = 'UPDATE links SET name = ? WHERE id = ?'
    data = (name, id)
    with con:
        con.execute(sql, data)
    con.close()
