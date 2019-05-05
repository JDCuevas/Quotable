import unittest
import csv
import tester.context 
from dao.collectionDAO import CollectionDao
from dao.quoteDAO import QuoteDao


class TestQuoteDao(unittest.TestCase):

	def setUp(self):
		self.quoteDAO_1 = QuoteDao()
		self.quoteDAO_2 = QuoteDao()
		self.fakeEntry = len(self.quoteDAO_1.getAllQuotes()) + 1
		self.dbData = []

		with open('dao/quoteData.csv') as file:
			reader = csv.DictReader(file)
			for row in reader:
				self.dbData.append(row)

	def tearDown(self):
		pass

	def test_getAllQuotes(self):
		self.assertEqual(self.quoteDAO_1.quoteData, self.quoteDAO_1.getAllQuotes())
		self.assertEqual(self.quoteDAO_1.getAllQuotes(), self.quoteDAO_2.getAllQuotes())
		self.assertEqual(self.quoteDAO_1.getAllQuotes(), self.dbData)

	def test_getQuoteById(self):
		qid = 0
		target = {}

		# Skips test if no data is available, if there is, targets first row.
		if len(self.dbData) > 0:
			qid = 1
		else:
			pass
		
		# Obtain target from test load of data.
		for row in self.dbData:
			if int(row['qid']) == qid:
				target = row

		# Compare method output to target.
		self.assertEqual(self.quoteDAO_1.getQuoteById(qid), target)

	def test_getQuotesByAuthorName(self):
		author = ""
		target = []

		# Skips test if no data is available, if there is, targets first row.
		if len(self.dbData) > 0:
			author = self.dbData[0]['author']
		else:
			pass

		# Obtain target from test load of data.
		for row in self.dbData:
			if row['author'] == author:
				target.append(row)

		# Compare method output to target.
		self.assertEqual(self.quoteDAO_1.getQuotesByAuthorName(author), target)

	def test_getQuotesByAuthorFirstName(self):
		author_firstName = ""
		target_quotes = []

		# Skips test if no data is available, if there is, targets first row.
		if len(self.dbData) > 0:
			author_firstName = self.dbData[0]['firstName']
		else:
			pass

		# Obtain target from test load of data.
		for row in self.dbData:
			if row['firstName'] == author_firstName:
				target_quotes.append(row)

		# Compare method output to target.
		self.assertEqual(self.quoteDAO_1.getQuotesByAuthorFirstName(author_firstName), target_quotes)

	def test_getQuotesByAuthorLastName(self):
		author_lastName = ""
		target_quotes = []

		# Skips test if no data is available, if there is, targets first row.
		if len(self.dbData) > 0:
			author_lastName = self.dbData[0]['lastName']
		else:
			pass

		# Obtain target from test load of data.
		for row in self.dbData:
			if row['lastName'] == author_lastName:
				target_quotes.append(row)

		# Compare method output to target.
		self.assertEqual(self.quoteDAO_1.getQuotesByAuthorLastName(author_lastName), target_quotes)


	def test_getQuotesByKeywords(self):
		keywords = 'the'
		target_quotes = []

		for row in self.dbData:
			if keywords in row['text'].lower():
				target_quotes.append(row)

		self.assertEqual(self.quoteDAO_1.getQuotesByKeywords(keywords), target_quotes)

	def test_getQuotesByUploader(self):
		uploader = ''
		target_quotes = []

		# Skips test if no data is available, if there is, targets first row.
		if len(self.dbData) > 0:
			uploader = self.dbData[0]['uploader']
		else:
			pass

		for row in self.dbData:
			if int(row['uploader']) ==  uploader:
				target_quotes.append(row)

		self.assertEqual(self.quoteDAO_1.getQuotesByUploader(uploader), target_quotes)