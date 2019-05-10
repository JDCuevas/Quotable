import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import urllib.request
import unittest
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from tester.userExample import UserExample
from flask_testing import LiveServerTestCase
from selenium import webdriver
from testing.postgresql import Postgresql
from tester.db import db
import time
from flask import url_for
from dao.contactDAO import ContactDao
from config.dbconfig import pg_config
from dao.collectionDAO import CollectionDao

from webdriverdownloader import GeckoDriverDownloader
user2_name = 'Jamie'
user1_name = 'Riley'
user1_username = 'riley233'
user1_email = 'riley@noplace.com'
user1_password = 'password'
user2_username = 'jamie'
user2_email = 'jamie@whatsthis.com'
user2_password = 'password'


class TestBase(unittest.TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['LIVESERVER_PORT'] = 8943
        app.config['LIVESERVER_TIMEOUT'] = 10
        connection_url = "dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['passwd'])

        self.conn = psycopg2._connect(connection_url)
        #app.config.update(SQLALCHEMY_DATABASE_URI = connection_url)
        return app

    def setUp(self):

        self.driver = webdriver.Firefox()
        self.driver.get('http://127.0.0.1:5000/')

        #db.session.commit()
        #db.drop_all()
        #db.create_all()

        p1 = UserExample(user1_name, user1_username, user1_email, user1_password)
        p2 = UserExample(user2_name, user2_username, user2_email, user2_password)

        #db.session.add(p1)
        #db.session.add(p2)
        #db.session.commit()

        ########################Views#########################################
    def test_welcome_view(self):
        response = self.driver.get('http://127.0.0.1:5000/')
        self.assertEqual(self.driver.current_url, 'http://127.0.0.1:5000/')


        #########################Registration##################################

    def test_registration_invalid_email(self):
            self.driver.find_element_by_id("register_link").click()
            time.sleep(1)

            self.driver.find_element_by_id("name").send_keys("Mariam")
            self.driver.find_element_by_id("email").send_keys("invalid")
            self.driver.find_element_by_id("username").send_keys("saffar")
            self.driver.find_element_by_id("password").send_keys("password")
            self.driver.find_element_by_id("confirm_password").send_keys("password")
            self.driver.find_element_by_id("submit").click()
            time.sleep(1)

            self.assertEqual(self.driver.current_url, 'http://127.0.0.1:5000/register')

    def test_registration_confirm_password(self):
            self.driver.find_element_by_id("register_link").click()
            time.sleep(1)

            self.driver.find_element_by_id("name").send_keys("Mariam")
            self.driver.find_element_by_id("email").send_keys("msaffar@upr.edu")
            self.driver.find_element_by_id("username").send_keys("saffar")
            self.driver.find_element_by_id("password").send_keys("password")
            self.driver.find_element_by_id("confirm_password").send_keys("wrong_password")
            self.driver.find_element_by_id("submit").click()
            time.sleep(1)

            self.assertEqual(self.driver.current_url, 'http://127.0.0.1:5000/register' )

    def test_registration(self):
            self.driver.find_element_by_id("register_link").click()
            time.sleep(1)

            self.driver.find_element_by_id("name").send_keys("Mariam")
            self.driver.find_element_by_id("email").send_keys("msaffar@upr.edu")
            self.driver.find_element_by_id("username").send_keys("saffar")
            self.driver.find_element_by_id("password").send_keys("password")
            self.driver.find_element_by_id("confirm_password").send_keys("password")
            self.driver.find_element_by_id("submit").click()
            time.sleep(1)


            self.assertEqual(self.driver.current_url, 'http://127.0.0.1:5000/' )




        ###################################Login########################################

    def test_login_wrong_username(self):

            self.driver.find_element_by_id("login_link").click()
            time.sleep(1)

            self.driver.find_element_by_id("username").send_keys("nope")
            self.driver.find_element_by_id("password").send_keys("password")
            self.driver.find_element_by_id("submit").click()
            time.sleep(1)

            self.assertEqual(self.driver.current_url, 'http://127.0.0.1:5000/login' )

    def test_login_wrong_password(self):

            self.driver.find_element_by_id("login_link").click()
            time.sleep(1)

            self.driver.find_element_by_id("username").send_keys("saffar")
            self.driver.find_element_by_id("password").send_keys("invalid")
            self.driver.find_element_by_id("submit").click()
            time.sleep(1)

            self.assertEqual(self.driver.current_url, 'http://127.0.0.1:5000/login' )

    def test_login(self):

            self.driver.find_element_by_id("login_link").click()
            time.sleep(1)

            self.driver.find_element_by_id("username").send_keys("msaffar")
            self.driver.find_element_by_id("password").send_keys("ww")
            self.driver.find_element_by_id("submit").click()
            time.sleep(1)

            self.assertEqual(self.driver.current_url, 'http://127.0.0.1:5000/')



        ##########################Search########################################

    def test_search_by_author(self):

            self.driver.find_element_by_id("quotes_link").click()
            time.sleep(1)
            self.driver.find_element_by_id("myInput").send_keys("Tyrion")
            baseTable = self.driver.find_element_by_id("searchableTable")
            tableRows = baseTable.find_element_by_tag_name("tr")
            cell = self.driver.find_element_by_xpath("//table/tbody/tr[2]/td[1]")
            author = cell.text
            time.sleep(1)
            self.assertEqual(author,"Tyrion Lannister")  # selenium to read first line in table


    def test_search_by_quote(self):
            self.driver.find_element_by_id("quotes_link").click()
            time.sleep(1)
            self.driver.find_element_by_id("myInput").send_keys("What is dead may never die")
            baseTable = self.driver.find_element_by_id("searchableTable")
            tableRows = baseTable.find_element_by_tag_name("tr")
            cell = self.driver.find_element_by_xpath("//table/tbody/tr[1]/td[2]")
            quote = cell.text
            time.sleep(3)
            self.assertEqual(quote, "What is dead may never die.")


        ####################################Edit####################################
    def test_add_own_quote(self):
        self.driver.find_element_by_id("login_link").click()
        time.sleep(1)

        self.driver.find_element_by_id("username").send_keys("msaffar")
        self.driver.find_element_by_id("password").send_keys("ww")
        self.driver.find_element_by_id("submit").click()

        self.driver.find_element_by_id("quotes_link").click()
        self.driver.find_element_by_id("add_quote").click()
        self.driver.find_element_by_id("firstName").send_keys("Mariam")
        self.driver.find_element_by_id("lastName").send_keys("Saffar")
        time.sleep(2)
        #self.driver.find_element_by_id("editor").click()
        self.driver.find_element_by_id("writeQuote").send_keys("I hope this works")
        self.driver.find_element_by_id("addQuoteSubmit").click()
        self.driver.find_element_by_id("collection_link").click()
        self.driver.find_element_by_id("myInput").send_keys("I hope this works")
        baseTable = self.driver.find_element_by_id("searchableTable")
        tableRows = baseTable.find_element_by_tag_name("tr")
        cell = self.driver.find_element_by_xpath("//table/tbody/tr[2]/td[2]")
        quote = cell.text

        self.assertEqual(quote, "I hope this works")


    def test_edit_quote(self):
        self.driver.find_element_by_id("login_link").click()
        time.sleep(1)

        self.driver.find_element_by_id("username").send_keys("msaffar")
        self.driver.find_element_by_id("password").send_keys("ww")
        self.driver.find_element_by_id("submit").click()

        self.driver.find_element_by_id("collection_link").click()
        baseTable = self.driver.find_element_by_id("searchableTable")
        cell = self.driver.find_element_by_xpath("//table/tbody/tr[2]/td[5]")
        cell.click()
        time.sleep(5)
        self.driver.find_element_by_id("writeQuote").send_keys(" 2")
        self.driver.find_element_by_id("editQuoteSubmit").click()
        self.driver.find_element_by_id("collection_link").click()
        self.driver.find_element_by_id("myInput").send_keys("I hope this works 2")
        baseTable = self.driver.find_element_by_id("searchableTable")
        cell = self.driver.find_element_by_xpath("//table/tbody/tr[2]/td[2]")
        quote = cell.text

        self.assertEqual(quote, "I hope this works 2")


        ###################################Share###################################
    def test_add_contact(self):
        self.driver.find_element_by_id("login_link").click()
        time.sleep(1)

        self.driver.find_element_by_id("username").send_keys("msaffar")
        self.driver.find_element_by_id("password").send_keys("ww")
        self.driver.find_element_by_id("submit").click()

        self.driver.find_element_by_id("contacts_link").click()
        self.driver.find_element_by_id("addContactLinkBtn").click()
        baseTable = self.driver.find_element_by_id("userTable")
        cell = self.driver.find_element_by_xpath("//table/tbody/tr[5]/td[3]")
        cell.click()
        self.driver.find_element_by_id("contacts_link").click()
        cell = self.driver.find_element_by_xpath("//table/tbody/tr[2]/td[1]")
        contact = cell.text

        self.assertEqual(contact, "Amir")
        dao = ContactDao()
        self.assertTrue(dao.checkForContact(8, 9))


    def test_share_quote(self):
        self.driver.find_element_by_id("login_link").click()
        time.sleep(1)

        self.driver.find_element_by_id("username").send_keys("msaffar")
        self.driver.find_element_by_id("password").send_keys("ww")
        self.driver.find_element_by_id("submit").click()

        self.driver.find_element_by_id("quotes_link").click()
        (self.driver.find_element_by_xpath("//table/tbody/tr[1]/td[4]")).click()

        self.driver.find_element_by_id("collection_link").click()
        cell = self.driver.find_element_by_xpath("//table/tbody/tr[1]/td[4]")
        cell.click()
        self.driver.find_element_by_id("shareBtn").click()
        self.driver.find_element_by_id("logout_link").click()

        self.driver.find_element_by_id("username").send_keys("amir")
        self.driver.find_element_by_id("password").send_keys("ww")
        self.driver.find_element_by_id("submit").click()

        self.driver.find_element_by_id("shared_link").click()

        collectionDao = CollectionDao()
        self.assertTrue(collectionDao.checkForQuote(9, 4))





    ########################################Delete#################################
    def test_remove_quote(self):
        self.driver.find_element_by_id("login_link").click()
        time.sleep(1)
        self.driver.find_element_by_id("username").send_keys("amir")
        self.driver.find_element_by_id("password").send_keys("ww")
        self.driver.find_element_by_id("submit").click()
        time.sleep(1)
        self.driver.find_element_by_id("shared_link").click()
        self.driver.find_element_by_xpath("//table/tbody/tr[1]/td[5]").click()

        self.driver.find_element_by_id("collection_link").click()
        self.driver.find_element_by_xpath("//table/tbody/tr[1]/td[6]").click()
        collectionDao = CollectionDao()
        self.assertFalse(collectionDao.checkForQuote(9, 4))


    #def test_server_is_up_and_running(self):
        #response = urllib.request.urlopen(self.get_server_url())
        #self.assertEqual(response.code, 200)

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
