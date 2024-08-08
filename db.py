import sqlite3 as sl

con = sl.connect('links.db')

with con: 
    data = con.execute("select count(*) from sqlite_master where type='table' and name='links")
    for row in data:
        if row[0] == 0:
            with con: 
                con.execute( """
                CREATE TABLE links (
                    id INT PRIMARY KEY,
                    url VARCHAR(200),
                    name VARCHAR(200),
                    availability INT          
                    );
                """
                )

def func(message):
    con=sl.connect('links.db')
    sql = 'INSERT INTO links (id, url, name, availability) VALUES (?, ?, ?, ?)'
    data = [
        # id + 1 каждый раз, юрл ссылки, краткое название если нужно но может быть нулевым, считывание доступности товара
    ]
    with con: 
        con.executemany(sql, data)