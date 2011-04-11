
import unittest
from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.ext import testbed


class myModel42(db.Model):
	"""A model class used for testing."""
	number = db.IntegerProperty(default=42)
	text = db.StringProperty()


class testNamespaces(unittest.TestCase):

	def setUp(self):
			# First, create an instance of the Testbed class.
			self.testbed = testbed.Testbed()
			# Then activate the testbed, which prepares the service stubs for use.
			self.testbed.activate()
			# Next, declare which service stubs you want to use.
			self.testbed.init_datastore_v3_stub()
			self.testbed.init_memcache_stub()

	def tearDown(self):
		self.testbed.deactivate()

	def testInsertEntity(self):
		myModel42().put()
		myModel42().put()
		myModel42().put()


		import google.appengine.ext.db

		q = db.GqlQuery("SELECT * FROM __namespace__")
		for p in q.fetch(100):
			print "namespace: '%s'" % p.namespace_name


		self.assertEqual(1, len(myModel42.all().fetch(2)))


