import csv
from dao.quoteDAO import QuoteDao
from config.dbconfig import pg_config
import psycopg2
import psycopg2.extras

class CollectionDao:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                pg_config['user'],
                                                pg_config['passwd'])
        self.conn = psycopg2._connect(connection_url)

    def getAllCollections(self):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT * FROM collections;"
        cursor.execute(query)
        result = cursor.fetchall()

        return result

    def checkForQuote(self, uid, qid):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT * FROM collections WHERE uid=%s and qid=%s"
        
        cursor.execute(query, (uid, qid))
        result = cursor.fetchone()
        cursor.close()

        return result

    def saveQuote(self, uid, qid):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "INSERT INTO collections(uid, qid) VALUES (%s, %s) RETURNING colid"
        
        cursor.execute(query, (uid, qid))
        colid = cursor.fetchone()['colid']
        self.conn.commit()
        cursor.close()

        return colid

    def removeQuote(self, uid, qid):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "DELETE FROM collections WHERE uid =%s and qid=%s RETURNING colid"
        cursor.execute(query, (uid, qid,))
        colid = cursor.fetchone()['colid']
        self.conn.commit()
        cursor.close()

        return colid

    def getUserCollection(self, uid):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "select Q.qid, Q.firstName, Q.lastName, Q.text, Q.uploader from Collections as C, Quotes as Q where C.uid = %s and C.qid = Q.qid"
        cursor.execute(query, (uid,))
        result = cursor.fetchall()

        return result