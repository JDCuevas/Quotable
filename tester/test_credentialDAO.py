import unittest
import csv
import tester.context
from dao.credentialDAO import CredentialDAO


class TestCredentialDAO(unittest.TestCase):

    def setUp(self):
        self.collection_1 = CredentialDAO()
        self.collection_2 = CredentialDAO()

    def tearDown(self):
        pass

    def test_getAllCredentials(self):
        print('Test GetAllCredentials')
        read = []
        # Check the files are being read well.
        with open('dao/credentialData.csv') as file:
            reader = csv.DictReader(file)

            for row in reader:
                read.append(row)

        self.assertEqual(self.collection_1.getAllCredentials(), self.collection_2.getAllCredentials())
        self.assertEqual(self.collection_1.getAllCredentials(), read)
        self.assertEqual(self.collection_2.getAllCredentials(), read)


    def test_getCredentialsByUsername(self):
        print('Test CredentialsByUsername')
        self.assertEqual(self.collection_1.getCredentialsByUsername('msaffar'), self.collection_2.getCredentialsByUsername('msaffar'))
        self.assertNotEqual(self.collection_1.getCredentialsByUsername('msaffar'),self.collection_2.getCredentialsByUsername('jdcuevas'))

    def test_getCredentialsByName(self):
        print('Test CredentialsByName')
        self.assertNotEqual(self.collection_1.getCredentialsByName('Julian Cuevas'), self.collection_1.getCredentialsByName('Mariam Saffar'))
        self.assertEqual(self.collection_1.getCredentialsByName('Julian Cuevas'), self.collection_1.getCredentialsByName('Julian Cuevas'))

    def test_mergeUserWithCredentials(self):
        print('Test MergeUserWithCredentials')
        print(self.collection_1.mergeUserWithCredentials())



