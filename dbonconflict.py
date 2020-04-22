import sqlite3

conn = sqlite3.connect('example1.db')
c = conn.cursor()
c.execute('''CREATE TABLE if not exists 
vocabulary(
    word TEXT PRIMARY KEY, 
    count INT DEFAULT 1, 
    test1 text DEFAULT te ,
    test2 text)
    ''')
c.execute('''INSERT INTO vocabulary(
    word,
    test1
    ) 
    VALUES(
        'jovial123',
        'tes'
        ) 
        ON CONFLICT(word) DO UPDATE SET 
        count = count+1, 
        test1 = 'te2';
        ''')
conn.commit()

for i in conn.execute('''select * from vocabulary'''):
    print(i)