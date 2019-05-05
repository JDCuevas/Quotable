import unittest
import csv
import tester.context 
from dao.userDAO import UserDao


class TestUserDao(unittest.TestCase):

	def setUp(self):
		self.userDAO_1 = UserDao()
		self.userDAO_2 = UserDao()
		self.fakeEntry = len(self.userDAO_1.getAllUsers()) + 1
		self.dbData = []

		with open('dao/userData.csv') as file:
			reader = csv.DictReader(file)
			for row in reader:
				self.dbData.append(row)

	def tearDown(self):
		pass

	def test_getAllUsers(self):
		self.assertEqual(self.userDAO_1.userData, self.userDAO_1.getAllUsers())
		self.assertEqual(self.userDAO_1.getAllUsers(), self.userDAO_2.getAllUsers())
		self.assertEqual(self.userDAO_1.getAllUsers(), self.dbData)

	def test_getUserById(self):
		uid = 0
		target = {}

		# Skips test if no data is available, if there is, targets first row.
		if len(self.dbData) > 0:
			uid = 1
		else:
			pass
		
		# Obtain target from test load of data.
		for row in self.dbData:
			if int(row['uid']) == uid:
				target = row

		# Compare method output to target.
		self.assertEqual(self.userDAO_1.getUserById(uid), target)

	def test_getUsersByFirstName(self):
		name = ""
		target = []

		# Skips test if no data is available, if there is, targets first row.
		if len(self.dbData) > 0:
			name = self.dbData[0]['firstName']
		else:
			pass

		# Obtain target from test load of data.
		for row in self.dbData:
			if row['firstName'] == name:
				target.append(row)

		# Compare method output to target.
		self.assertEqual(self.userDAO_1.getUsersByFirstName(name), target)

	def test_getUsersByLastName(self):
		name = ""
		target = []

		# Skips test if no data is available, if there is, targets first row.
		if len(self.dbData) > 0:
			name = self.dbData[0]['lastName']
		else:
			pass

		# Obtain target from test load of data.
		for row in self.dbData:
			if row['lastName'] == name:
				target.append(row)

		# Compare method output to target.
		self.assertEqual(self.userDAO_1.getUsersByLastName(name), target)

	def test_getUserByName(self):
		name = ""
		target = {}

		# Skips test if no data is available, if there is, targets first row.
		if len(self.dbData) > 0:
			name = self.dbData[0]['name']
		else:
			pass

		# Obtain target from test load of data.
		for row in self.dbData:
			if row['name'] == name:
				target = row

		# Compare method output to target.
		self.assertEqual(self.userDAO_1.getUserByName(name), target)

	def test_getUserByUsername(self):
		target = {}
		target_username = ''

		# Skips test if no data is available, if there is, targets first row.
		if len(self.dbData) > 0:
			uid = 1
		else:
			pass
		
		# Obtain target from test load of data.
		for row in self.dbData:
			if int(row['uid']) == uid:
				target = row
				target_username = self.userDAO_1.getUserCredentials(uid)['username']

		# Compare method output to target.
		self.assertEqual(self.userDAO_1.getUserByUsername(target_username), target)

	def test_getUserByEmail(self):
		email = ""
		target = {}

		# Skips test if no data is available, if there is, targets first row.
		if len(self.dbData) > 0:
			email = self.dbData[0]['email']
		else:
			pass

		# Obtain target from test load of data.
		for row in self.dbData:
			if row['email'] == email:
				target = row

		# Compare method output to target.
		self.assertEqual(self.userDAO_1.getUserByEmail(email), target)

	def test_getUserCredentials(self):
		pass

	def test_getUserContacts(self):
		pass
