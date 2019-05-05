import csv
from config.dbconfig import pg_config
import psycopg2
import psycopg2.extras

class ContactDao:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                pg_config['user'],
                                                pg_config['passwd'])

        self.conn = psycopg2._connect(connection_url)

    def addContact(self, uid, cid):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "INSERT INTO contacts(uid, cid) VALUES (%s, %s) RETURNING clid;"
        cursor.execute(query, (uid, cid))
        clid = cursor.fetchone()['clid']
        self.conn.commit()
        cursor.close()

        return clid

    def removeContact(self, uid, cid):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "DELETE FROM contacts WHERE uid=%s and cid=%s RETURNING clid;"
        cursor.execute(query, (uid, cid))
        clid = cursor.fetchone()['clid']
        self.conn.commit()
        cursor.close()

        return clid

    def checkForContact(self, uid, cid):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT * FROM contacts WHERE uid=%s and cid=%s"
        
        cursor.execute(query, (uid, cid))
        result = cursor.fetchone()
        cursor.close()

        return result

    def getAllContacts(self, uid):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT U.uid, U.name, U.username, U.email FROM users as U, contacts as C WHERE C.uid = %s and U.uid = C.cid"
        cursor.execute(query, (uid,))
        result = cursor.fetchall()
        cursor.close()

        return result