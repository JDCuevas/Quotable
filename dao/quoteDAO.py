import csv
from config.dbconfig import pg_config
import psycopg2
import psycopg2.extras

class QuoteDao:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                pg_config['user'],
                                                pg_config['passwd'])

        self.conn = psycopg2._connect(connection_url)

    def getAllQuotes(self):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT * FROM quotes"
        cursor.execute(query)

        result = cursor.fetchall()
        cursor.close()

        return result

    def addQuote(self, firstName, lastName, text, uploader):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "INSERT INTO quotes(firstName, lastName, text, uploader) VALUES (%s, %s, %s, %s) RETURNING qid;"
        
        cursor.execute(query, (firstName, lastName, text, uploader))
        qid = cursor.fetchone()['qid']
        self.conn.commit()
        cursor.close()

        return qid

    def editQuote(self, firstName, lastName, text, uploader, qid):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "UPDATE quotes SET firstname=%s, lastname=%s, text=%s, uploader=%s WHERE qid =%s RETURNING qid"
        cursor.execute(query, (firstName, lastName, text, uploader, qid))
        qid = cursor.fetchone()['qid']
        self.conn.commit()
        cursor.close()

        return qid

    def deleteQuote(self, qid):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "DELETE FROM quotes WHERE qid=%s RETURNING qid;"
        cursor.execute(query, (qid,))
        qid = cursor.fetchone()['qid']
        self.conn.commit()
        cursor.close()

        return qid


    def getQuoteById(self, qid):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT * FROM quotes WHERE qid = %s;"
        cursor.execute(query, (qid,))

        result = cursor.fetchone()
        cursor.close()

        return result

    '''
    def insert(self, username, password, firstName, lastName):
        uid = 0
        return uid

    def delete(self, uid):
        re0turn uid

    def update(self):
        user = self.users[1]
        return user

    def getCountByUserId(self):

        result = []

        return result

    def insertUser(self):
        user = self.users[1]
        return user
    '''