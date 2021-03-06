import sqlite3

conn = sqlite3.connect('emaildb.sqlite')
cur = conn.cursor()

cur.execute('''
DROP TABLE IF EXISTS Counts''')

cur.execute('''
CREATE TABLE Counts (org TEXT, count INTEGER)''')

fname = 'mbox.txt'
fh = open(fname)
for line in fh:
    if not line.startswith('From: '):
        continue
    pieces = line.split()
    email = pieces[1]
    org = email[email.index('@')+1:]
    print(org)
    sql = "SELECT count FROM Counts WHERE org = '{org}'"
    cur.execute(sql.format(org=org))
    row = cur.fetchone()
    if row is None:
        sql = (
            "INSERT INTO Counts (org, count)"
            "VALUES ( '{org}', 1 )"
            )
        cur.execute(sql.format(org=org))
    else:
        sql = "UPDATE Counts SET count=count+1 WHERE org = '{org}'"
        cur.execute(sql.format(org=org))

    conn.commit()

sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'

print("Counts:")
for row in cur.execute(sqlstr):
    print(str(row[0]), row[1])

cur.close()
print('org check finish!')
