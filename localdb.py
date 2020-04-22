import sqlite3
conn = sqlite3.connect('example.db')
c = conn.cursor()
# Create table
c.execute('''CREATE TABLE if not exists stocks (date text, trans text, symbol text, qty real, price real)''')
#  create table if not exists TableName (col1 typ1, ..., colN typN)
# Insert a row of data
#c.execute("INSERT INTO stocks VALUES ('2022-01-05','BUY','RHAT',100,35.14)")
# Save (commit) the changes
conn.commit()
# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()


def createdb():
    with sqlite3.connect('example.db') as conn:
        c = conn.cursor()
        c.execute(
            '''CREATE TABLE if not exists stocks 
            (
            symbol text PRIMARY KEY,
            date text, 
            trans text, 
            qty real , 
            price real
            )
            ''')
        conn.commit()

def insertdatatodb(data):
    with sqlite3.connect('example.db') as conn:
        c = conn.cursor()
        for i in data:
            c.execute('''INSERT INTO
                stocks(
                date,
                trans,
                symbol,
                qty,
                price
                )
                VALUES(
                    :date,
                    :trans,
                    :symbol,
                    :qty,
                    :price
                )
                ON CONFLICT(symbol) DO UPDATE SET 
                    date="test"
                ''', i)
            conn.commit()


def searchdata():
    with sqlite3.connect('example.db') as conn:
        c = conn.cursor()
        va = c.execute('''select symbol from stocks''')
        return va


def main():
    createdb()
    ls = list()
    for i in range(10):
        da = dict()
        da['date'] = "2020-11-11"
        da['trans'] = 'test'
        da['symbol'] = 'test4'
        da['qty'] = i
        da['price'] = i+1
        ls.append(da)
    for i in ls:
        print(i)
    insertdatatodb(ls)
    for i in searchdata():
        print(i)

    
if __name__ == "__main__":
    main()
