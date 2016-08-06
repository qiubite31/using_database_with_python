import sqlite3

conn = sqlite3.connect('emaildb.sqlite')
cur = conn.cursor()

cur.execute('''
DROP TABLE IF EXISTS Counts''')

cur.execute('''
CREATE TABLE Counts (email TEXT, count INTEGER)''')

fname = 'mbox.txt'
fh = open(fname)
for line in fh:
    if not line.startswith('From: '):
        continue
    pieces = line.split()
    email = pieces[1]
    print(email)
    sql = "SELECT count FROM Counts WHERE email = '{mail}'"
    cur.execute(sql.format(mail=email))
    row = cur.fetchone()
    if row is None:
        sql = (
            "INSERT INTO Counts (email, count)"
            "VALUES ( '{mail}', 1 )"
            )
        cur.execute(sql.format(mail=email))
    else:
        sql = "UPDATE Counts SET count=count+1 WHERE email = '{mail}'"
        cur.execute(sql.format(mail=email))

    conn.commit()

sqlstr = 'SELECT email, count FROM Counts ORDER BY count DESC LIMIT 10'

print("Counts:")
for row in cur.execute(sqlstr):
    print(str(row[0]), row[1])

cur.close()
print('email check finish!')
