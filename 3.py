import sqlite3

def createdb():
    conn = sqlite3.connect('music.sqlite3')
    cur = conn.cursor()

    cur.execute('DROP TABLE IF EXISTS Tracks ')
    cur.execute('CREATE TABLE Tracks (title TEXT, plays INTEGER)')

    conn.close()
    
def createandinsert():
    conn = sqlite3.connect('music.sqlite3')

    cur = conn.cursor()

    cur.execute('INSERT INTO Tracks (title, plays) VALUES (?, ?)',('Thunderstruck', 20))
    cur.execute('INSERT INTO Tracks (title, plays) VALUES (?, ?)',('My Way', 15))
    conn.commit()
    
    print('Tracks:')
    #cur.execute("UPDATE Tracks SET plays = 16 WHERE title = 'My Way'")
    #cur.execute('SELECT title, plays FROM Tracks')
    #cur.execute('SELECT title, plays FROM Tracks ORDER BY title')
    cur.execute("SELECT * FROM Tracks WHERE title = 'My Way'")
    for row in cur :
        print(row)
        
    cur.execute('DELETE FROM Tracks WHERE plays < 100')
    conn.commit()
    
    cur.close()
    

if __name__ == '__main__':
    #createdb()
    createandinsert()
