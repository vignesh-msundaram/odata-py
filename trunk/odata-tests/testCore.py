
import unittest
from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.ext import testbed

import odata.core
import odata.entityFactory

class testCore(unittest.TestCase):

	def setUp(self):
		import model

		odata.entityFactory.INSTANCE.append(model.Pet)
		odata.entityFactory.INSTANCE.append(model.SecondModel)

		# First, create an instance of the Testbed class.
		self.testbed = testbed.Testbed()
		# Then activate the testbed, which prepares the service stubs for use.
		self.testbed.activate()
		# Next, declare which service stubs you want to use.
		self.testbed.init_datastore_v3_stub()
		self.testbed.init_memcache_stub()

	def tearDown(self):
		self.testbed.deactivate()

	def test_parseDateTime(self):
		import datetime

		#parseDateTime(datatetime.datetime.now().isoformat())
		dt = odata.core.parseDateTime('2011-05-04T18:52:42.171000')
		assert dt

		self.assertEqual(datetime.datetime, dt.__class__)

		self.assertEqual(2011, dt.year)
		self.assertEqual(5, dt.month)
		self.assertEqual(4, dt.day)
		self.assertEqual(18, dt.hour)
		self.assertEqual(52, dt.minute)
		self.assertEqual(42, dt.second)

	def test_parseDate(self):
		import datetime
		
		dt = odata.core.parseDate('2011-05-04T18:52:42.171000')
		assert dt

		self.assertEqual(datetime.date, dt.__class__)

		self.assertEqual(2011, dt.year)
		self.assertEqual(5, dt.month)
		self.assertEqual(4, dt.day)

	def test_parseTime(self):
		import datetime
		
		dt = odata.core.parseTime('2011-05-04T18:52:42.171000')
		assert dt

		self.assertEqual(datetime.time, dt.__class__)

		self.assertEqual(18, dt.hour)
		self.assertEqual(52, dt.minute)
		self.assertEqual(42, dt.second)

	def test_parse_request_url_1(self):
		request_url = r"ns0.ns1.ModelName('KEY_NAME')/Description"
		dic = odata.core.parse_request_url(request_url)

		self.assertEqual('ns0.ns1', dic['namespace'])
		self.assertEqual('ModelName', dic['class_name'])
		self.assertEqual('KEY_NAME', dic['key'])
		self.assertEqual('Description', dic['description'])

	def test_parse_request_url_0(self):
		request_url = r"Pet()"
		dic = odata.core.parse_request_url(request_url)

		self.assertEqual('', dic['namespace'])
		self.assertEqual('Pet', dic['class_name'])
		self.assertEqual('', dic['key'])
		self.assertEqual(None, dic['description'])

	def testMERGE(self):
		pass

	def test_update_entity_from_atomEntry(self):
		import atom.core
		import atom.data
		import datetime

		XML = """<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<entry xmlns:d="http://schemas.microsoft.com/ado/2007/08/dataservices" xmlns:m="http://schemas.microsoft.com/ado/2007/08/dataservices/metadata" xmlns="http://www.w3.org/2005/Atom">
  <category scheme="http://schemas.microsoft.com/ado/2007/08/dataservices/scheme" term="model.Pet" />
  <title />
  <author>
    <name />
  </author>
  <updated>2011-04-07T14:53:34.6915924Z</updated>
  <id />
  <content type="application/xml">
    <m:properties>
      <d:birthdate m:type="Edm.DateTime">2011-04-07T16:53:34.6290844+02:00</d:birthdate>
      <d:key_name>xxxxx</d:key_name>
      <d:name>THE NAME HERE</d:name>
      <d:spayed_or_neutered m:type="Edm.Boolean" m:null="true" />
      <d:type>bird</d:type>
      <d:weight_in_pounds m:type="Edm.Int32" m:null="true" />
    </m:properties>
  </content>
</entry>"""
		entityClass = odata.entityFactory.get_class_by_name('Pet')
		o = apply(entityClass, (), {'type':'cat', 'name':'zerzer'})
		entry = atom.core.parse(XML, atom.data.Entry)
		odata.core.update_entity_from_atomEntry(o, entry)

		self.assertEqual(o.name, 'THE NAME HERE')
		self.assertEqual(o.birthdate, datetime.date(2011, 4, 7))
		self.assertEqual(o.spayed_or_neutered, None)
		self.assertEqual(o.type, 'bird')
		self.assertEqual(o.weight_in_pounds, None)

	def test_create_entity_from_atomEntry(self):
		import atom.core
		import atom.data
		import datetime

		XML = """<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<entry xmlns:d="http://schemas.microsoft.com/ado/2007/08/dataservices" xmlns:m="http://schemas.microsoft.com/ado/2007/08/dataservices/metadata" xmlns="http://www.w3.org/2005/Atom">
  <category scheme="http://schemas.microsoft.com/ado/2007/08/dataservices/scheme" term="model.Pet" />
  <title />
  <author>
    <name />
  </author>
  <updated>2011-04-07T14:53:34.6915924Z</updated>
  <id />
  <content type="application/xml">
    <m:properties>
      <d:birthdate m:type="Edm.DateTime">2011-04-07T16:53:34.6290844+02:00</d:birthdate>
      <d:key_name>xxxxx</d:key_name>
      <d:name>THE NAME HERE</d:name>
      <d:spayed_or_neutered m:type="Edm.Boolean" m:null="true" />
      <d:type>bird</d:type>
      <d:weight_in_pounds m:type="Edm.Int32" m:null="true" />
    </m:properties>
  </content>
</entry>"""
		
		entry = atom.core.parse(XML, atom.data.Entry)

		o = odata.entityFactory.create_entity_from_atomEntry(entry)

		self.assertEqual(o.name, 'THE NAME HERE')
		self.assertEqual(o.birthdate, datetime.date(2011, 4, 7))
		self.assertEqual(o.spayed_or_neutered, None)
		self.assertEqual(o.type, 'bird')
		self.assertEqual(o.weight_in_pounds, None)
