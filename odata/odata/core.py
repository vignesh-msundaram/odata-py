#!/usr/bin/python
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


""" TODO Documentation
"""


__author__ = 'Andri Rakotomalala'



import datetime
import re

import edmx

import entityFactory

import atom.data
import atom.core

import StringIO

from google.appengine.api import memcache
from google.appengine.api import datastore_types
from google.appengine.ext import db


import model #FIXME
NAMESPACE = 'model'	#FIXME

TYPE_MAPPING = {
		db.IntegerProperty:  'Edm.Int32',
		db.StringProperty:   'Edm.String',
		db.LinkProperty:   'Edm.String',
		db.StringListProperty:   'Edm.String',	#FIXME
		db.TextProperty:   'Edm.String',
		db.UserProperty:     'Edm.String',		#TODO: change this to a struct complextype
		db.DateProperty:     'Edm.DateTime',
		db.DateTimeProperty: 'Edm.DateTime',
		db.TimeProperty:     'Edm.DateTime',
		db.BooleanProperty:  'Edm.Boolean',
#        db.ReferenceProperty:  'Edm.String',
}

BASE_SVC_URL = 'odata.svc'

MAX_FETCH_COUNT = 20

EDMX_METADATA_NAMESPACE = 'http://schemas.microsoft.com/ado/2007/08/dataservices/metadata'

EDMX_ANNOTATION_NAMESPACE = 'http://schemas.microsoft.com/ado/2009/02/edm/annotation'

ODATA_SERVICES_NAMESPACE = 'http://schemas.microsoft.com/ado/2007/08/dataservices'

URL_PATTERN = re.compile(r'(?P<namespace>(\w+\.)*)(?P<class_name>\w+)(\((?P<key>.*)\))?(/(?P<deferred_entity>\w+))?$')

TYPE_TRANSFORM_FUNCTIONS = {
		db.DateProperty : lambda s : parseDate(s),
		db.DateTimeProperty : lambda s : parseDateTime(s),
		db.DateProperty : lambda s : parseDate(s),
		db.TimeProperty : lambda s : parseTime(s),
		db.IntegerProperty : lambda s : int(s),
		db.StringProperty : lambda s : s[1:-1] if s.startswith("'") and s.endswith("'") else s,
		db.LinkProperty : lambda s : s[1:-1] if s.startswith("'") and s.endswith("'") else s,
		db.StringListProperty : lambda s : s.split(','),	#FIXME
		db.TextProperty : lambda s : s,
		db.BooleanProperty : lambda s : s=='true',
#        db.ReferenceProperty : lambda s : db.Model.get(TYPE_TRANSFORM_FUNCTIONS[db.StringProperty](s)).key(),  #FIXME performance
#		'Edm.Boolean': lambda s : s=='true',


datastore_types.Link: lambda link : unicode(link),
datastore_types.Text: lambda o : unicode(o),
unicode: lambda t : t,
datetime.datetime : lambda d : d.isoformat(),
long: lambda l: str(l),
str: lambda l: l,
	}

def parse_request_url(url):
	match = URL_PATTERN.match(url)

	namespace = match.group('namespace')[:-1]
	key = match.group('key')[1:-1]	# strip quotes for URLs with the form http://app/odata.svc/Model('key')

	return {
		'class_name' : match.group('class_name'),
		'namespace' : namespace,
		'key' : key,
		'deferred_entity' : match.group('deferred_entity'),
	}

def parseDate(s):
#2011-04-01T17:35:19.2580297+02:00
	d = parseDateTime(s)
	return datetime.date(d.year, d.month, d.day)

DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'
def parseDateTime(s):
#datetime'2011-04-01T17:35:19.2580297+02:00'
	if s.startswith('datetime'):
		return datetime.datetime.strptime(s[9:28], DATETIME_FORMAT)
	else:
		return datetime.datetime.strptime(s[:19], DATETIME_FORMAT)

def parseTime(s):
	d = parseDateTime(s)
	return datetime.time(d.hour, d.minute, d.second)

def get_edmProperties_from_entry(entry):
	category = entry.category[0].term
	i = category.rfind('.')+1
	class_name = category[i:]
	entityClass = entityFactory.get_class_by_name(class_name)

	dic = {}

	for property in entry.content.extension_elements[0].extension_elements:
		NULL_ATTRIBUTE_KEY = '{%s}null'%EDMX_METADATA_NAMESPACE
		if NULL_ATTRIBUTE_KEY in property.attributes and property.attributes[NULL_ATTRIBUTE_KEY]=='true':
			value = None
		else:
			field_name = property.tag

			# keys are not settable/copiable, and therefore cannot be considered as properties 
			if field_name=='key' or field_name=='key_name':
				continue

			type_attribute_key = '{%s}type'%EDMX_METADATA_NAMESPACE
			edm_type = property.attributes[type_attribute_key] if type_attribute_key in property.attributes else 'Edm.String'
			value = property.text
			db_type = getattr(entityClass, field_name).__class__


			value = TYPE_TRANSFORM_FUNCTIONS[db_type](value)

			dic[field_name] = value
	return dic


def update_entity_from_atomEntry(o, entry):
	props = get_edmProperties_from_entry(entry);
	for k in props:
		setattr(o, k, props[k])

	return o

def build_atom_for_entity(o, application_url):
	class_name = entityFactory.getClassName_fromInstance(o, False)
	class_fullname = entityFactory.getClassName_fromInstance(o, True)

	entry_key = o.key()

	properties = atom.data.ExtensionElement(tag='properties', namespace=EDMX_METADATA_NAMESPACE)

	# add field key
	prop = atom.core.XmlElement(text=str(entry_key))
	prop.tag = 'key'
	prop.namespace = ODATA_SERVICES_NAMESPACE
	prop.attributes['{%s}type'%EDMX_METADATA_NAMESPACE] = TYPE_MAPPING[db.StringProperty]
	properties.extension_elements.append(prop)

	# add field key_name
	prop = atom.core.XmlElement(text=str(entry_key.name()))
	prop.tag = 'key_name'
	prop.namespace = ODATA_SERVICES_NAMESPACE
	prop.attributes['{%s}type'%EDMX_METADATA_NAMESPACE] = TYPE_MAPPING[db.StringProperty]
	properties.extension_elements.append(prop)

	entry = atom.data.Entry(
		id = atom.data.Id(text="%s/%s/%s('%s')"  % (application_url, BASE_SVC_URL, class_name, entry_key)),
		link = [atom.data.Link(rel='edit', title=class_name, href="%s('%s')" % (class_name, o.key())) ],
		category = [atom.data.Category(term=class_fullname, scheme="http://schemas.microsoft.com/ado/2007/08/dataservices/scheme")],
		content = atom.data.Content(type='application/xml')
		)

	# add other fields
	for field in o.fields():
		value = getattr(o, field)
		prop = atom.core.XmlElement()
		prop.tag = field
		prop.namespace = ODATA_SERVICES_NAMESPACE
		if value==None:
			prop.attributes['{%s}null'%EDMX_METADATA_NAMESPACE] = 'true'	#atom.core.XmlAttribute(EDMX_METADATA_NAMESPACE, 'null'))
		else:
			field_class = o.fields()[field].__class__
			if field_class==db.ReferenceProperty:
				ref_class = o.fields()[field].reference_class.__name__
				entry.link.append(
						atom.data.Link(rel='http://schemas.microsoft.com/ado/2007/08/dataservices/related/%s'%ref_class,
						type='application/atom+xml;type=entry',
						title=ref_class,
						href="%s('%s')" % (ref_class, value.key()))
						)

				field_class = db.StringProperty
				value = str(value.key())
				prop.tag = prop.tag + '__key__'

			elif field_class==db.StringListProperty:	#FIXME
				value = ','.join(value)

			prop.attributes['{%s}type'%EDMX_METADATA_NAMESPACE] = TYPE_MAPPING[field_class]
			prop.text = TYPE_TRANSFORM_FUNCTIONS[value.__class__](value)#unicode(value)
		
		properties.extension_elements.append(prop)
		

	entry.content.extension_elements = [properties]


	return entry

def build_discovery_document():
	DOC = """<?xml version="1.0" standalone="yes"?>
<service xml:base="http://localhost:3329/WebSite1/WcfDataService.svc/" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:app="http://www.w3.org/2007/app" xmlns="http://www.w3.org/2007/app">
<workspace>
<atom:title>Default</atom:title>"""

	for klass in entityFactory.INSTANCE:
		DOC += """ <collection href="%s"> <atom:title>%s</atom:title> </collection> """ % (klass.__name__, klass.__name__)

	DOC += """ </workspace> </service>"""
	return DOC

def build_metadata_document():
	roles_index = 0
	association_index = 0

	schema = edmx.TSchema(Namespace=NAMESPACE)
	schema.EntityContainer = edmx.EntityContainer(Name='default_container')

	for store in entityFactory.INSTANCE:
# create Entity
		entityType = edmx.TEntityType()
		entityType.Name = store.__name__
		schema.add_EntityType(entityType)

# create key
		entityType.set_Key(edmx.TEntityKeyElement(PropertyRef=[edmx.TPropertyRef(Name='key')]))
		
		p = edmx.TProperty(Name='key', Type='Edm.String', Nullable=False)	# for the moment set to False because of LinqPad
		p.set_anyAttributes_({'p8:StoreGeneratedPattern': 'Identity'})
		entityType.add_Property(p)

# create key
		p = edmx.TProperty(Name='key_name', Type='Edm.String', Nullable=True)
		p.set_anyAttributes_({'p8:StoreGeneratedPattern': 'Identity'})
		entityType.add_Property(p)

# create Fields
		for name in store.fields():
			t = store.fields()[name]
			if isinstance(t, db.ReferenceProperty):
				roles_index += 1
				fromrole_name = "role_%s" % roles_index

				roles_index += 1
				torole_name = "role_%s" % roles_index

				association_index += 1
				association_name = "association_%s" % (association_index)
				association_fullname = "%s.%s" % (NAMESPACE, association_name)

				toType_fullName = NAMESPACE+'.'+t.data_type.__name__
				fromType_fullName = NAMESPACE+'.'+entityType.Name

				ref = edmx.TNavigationProperty(Name=t.name, Relationship=association_fullname, ToRole=torole_name, FromRole=fromrole_name)
				entityType.add_NavigationProperty(ref)

				schema.add_Association(edmx.TAssociation(Name=association_name, End=[
					edmx.TAssociationEnd(Role=fromrole_name, Type=fromType_fullName, Multiplicity="*"),
					edmx.TAssociationEnd(Role=torole_name, Type=toType_fullName, Multiplicity="0..1"),
					]))


# create a new field 'field__key__' from which we can directly read the entity key
				name = name + '__key__'
				t = db.StringProperty(required=t.required)

			EdmType = TYPE_MAPPING[t.__class__]
			p = edmx.TProperty(Name=name, Type=EdmType, Nullable=not(t.required))
			entityType.add_Property(p)
# add entity to EntityContainer
		entitySet = edmx.EntitySet(Name=entityType.Name, EntityType=NAMESPACE+'.'+entityType.Name)
		schema.EntityContainer.add_EntitySet(entitySet)

	output = StringIO.StringIO()

	output.write('<?xml version="1.0" encoding="utf-8" standalone="yes"?>')
	output.write('<edmx:Edmx Version="1.0" xmlns:edmx="http://schemas.microsoft.com/ado/2007/06/edmx">')
	output.write('<edmx:DataServices xmlns:m="http://schemas.microsoft.com/ado/2007/08/dataservices/metadata" m:DataServiceVersion="1.0">')
	schema.export(output, 0, name_='Schema', namespace_='edmx:', namespacedef_='xmlns:p8="%s"'%EDMX_ANNOTATION_NAMESPACE)
	output.write('</edmx:DataServices></edmx:Edmx>')

	return output.getvalue()
