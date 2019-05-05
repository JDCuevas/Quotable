import csv
from config.dbconfig import pg_config
import psycopg2
import psycopg2.extras

class SharedDao:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                pg_config['user'],
                                                pg_config['passwd'])

        self.conn = psycopg2._connect(connection_url)

    def shareQuote(self, uid, qid, cid):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "INSERT INTO shared(uid, cid, qid) VALUES (%s, %s, %s) RETURNING sid;"
        cursor.execute(query, (uid, cid, qid))
        clid = cursor.fetchone()['sid']
        self.conn.commit()
        cursor.close()

        return clid

    def sharedWithMe(self, uid):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT U.username as shared_by, U.uid as shared_by_id, Q.qid, Q.firstName, Q.lastName, Q.text, UP.username as uploader FROM users as U, shared as S, quotes as Q, users as UP WHERE S.cid=%s and Q.qid=S.qid and U.uid=S.uid and UP.uid=Q.uploader"
        cursor.execute(query, (uid,))

        result = cursor.fetchall()
        cursor.close()

        return result
        
    def removeShared(self, shared_with, shared_by, qid):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "DELETE FROM shared WHERE uid=%s and cid=%s and qid=%s RETURNING sid"
        cursor.execute(query, (shared_by, shared_with, qid))

        result = cursor.fetchone()['sid']
        self.conn.commit()
        cursor.close()

        return result

    def countShared(self, shared_with):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT count(*) as shared FROM shared WHERE cid=%s"
        cursor.execute(query, (shared_with,))

        result = cursor.fetchone()
        cursor.close()

        return result
