import unittest
import csv
import tester.context 
from dao.collectionDAO import CollectionDao
from dao.quoteDAO import QuoteDao

class TestCollectionDao(unittest.TestCase):

	def setUp(self):
		self.collection_1 = CollectionDao()
		self.collection_2 = CollectionDao()
		self.fakeEntry = len(self.collection_1.getAllCollections()) + 1
		self.dbData = []

		with open('dao/collectionData.csv') as file:
			reader = csv.DictReader(file)
			for row in reader:
				self.dbData.append(row)

	def tearDown(self):
		pass
		
	def test_getAllCollections(self):
		self.assertEqual(self.collection_1.collectionData, self.collection_1.getAllCollections())
		self.assertEqual(self.collection_1.getAllCollections(), self.collection_2.getAllCollections())
		self.assertEqual(self.collection_1.getAllCollections(), self.dbData)


	def test_getUserCollection(self):
		uid = 0
		target = []

		# Skips test if no data is available, if there is, targets first row.
		if len(self.dbData) > 0:
			uid = '1'
		else:
			pass
		
		# Obtain target from test load of data.
		for row in self.dbData:
			if int(row['uid']) == uid:
				target.append(QuoteDao().getQuoteById(int(row['qid'])))

		# Compare method output to target.
		self.assertEqual(self.collection_1.getUserCollection(uid), target)

	def test_insert(self):
		# Keep a copy of the old data of the collection
		old_collection = self.collection_1.getAllCollections()
		self.assertEqual(self.collection_1.getAllCollections(), old_collection)

		# Insert a fake entry at the end of the list.
		self.collection_1.insert(self.fakeEntry,4,2)

		# Check that new collection data is not the same as old collection data.
		self.assertNotEqual(self.collection_1.getAllCollections(), old_collection)
		self.collection_1.delete(self.fakeEntry)

	def test_refresh(self):
		self.assertEqual(self.collection_1.collectionData, self.collection_2.collectionData)

		# Inside insert is a refresh method call. That means that collection_1 gets its instance of 
		# of the data refreshed, but collection_2 does not. 
		self.collection_1.insert(self.fakeEntry,3,2)
		self.assertNotEqual(self.collection_1.collectionData, self.collection_2.collectionData)
		self.collection_1.delete(self.fakeEntry)

		# Refresh collection_2 to reflect change in data and check.
		self.collection_2.refresh()  
		self.assertEqual(self.collection_1.collectionData, self.collection_2.collectionData)

	def test_delete(self):
		# Insert entry to be deleted and check that data is updated in csv.
		self.collection_1.insert(self.fakeEntry,3,2)
		self.collection_2.refresh()
		self.assertEqual(self.collection_1.collectionData, self.collection_2.collectionData)
		
		# Delete fake entry and check that data has changed (collection_2 hasn't refreshed, has old data)
		self.collection_1.delete(self.fakeEntry)
		self.assertNotEqual(self.collection_1.collectionData, self.collection_2.collectionData)
		
		# Refresh data and check that deletion has been reflected.
		self.collection_2.refresh()
		self.assertEqual(self.collection_1.collectionData, self.collection_2.collectionData)

		