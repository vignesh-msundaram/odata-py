from google.appengine.ext import webapp
from google.appengine.ext import db

import urllib

import atom.core
import atom.data

import core
import entityFactory




class OData_handler(webapp.RequestHandler):
	def get_http_method(self):
# get the x-http-method header, in case of POST tunnelling
#        method = self.request.headers['X-Http-Method']
		method = 'POST'
		for k,v in self.request.headers.items():		# stupid _trans_name()
			if k=='X-Http-Method':
				method = v
		return method

	def merge(self):
		request_url = urllib.unquote(self.request.path).replace('/%s/' % core.BASE_SVC_URL, '')
		dic = core.parse_request_url(request_url)
		class_name = dic['class_name']
		key = dic['key']

		entityClass = entityFactory.get_class_by_name(class_name)
		o = entityClass.get(key)

		entry = atom.core.parse(self.request.body, atom.data.Entry)
		core.update_entity_from_atomEntry(o, entry)

		o.put()

	def post(self):
		method = self.get_http_method()

		if method=='PUT':
			return self.put()
		elif method=='MERGE':
			return self.merge()

		entry = atom.core.parse(self.request.body, atom.data.Entry)
		entity = entityFactory.create_entity_from_atomEntry(entry)
		entity.put()

		self.response.headers['Location'] = "%s/%s/%s('%s')" % (self.request.application_url, core.BASE_SVC_URL, entity.__class__.__name__, entity.key())

		self.response.headers["Content-Type"] = "application/atom+xml;charset=utf-8"
		self.response.out.write('<?xml version="1.0" standalone="yes"?>')
		self.response.out.write(format_atom(self.request, [entity]))


	def put(self):
		self.error(400)
		self.response.out.write('Currently not supported')

	def get(self):
		request_url = urllib.unquote(self.request.path).replace('/%s/' % core.BASE_SVC_URL, '')
		dic = core.parse_request_url(request_url)

		class_name = dic['class_name']
		key = dic['key']
		deferred_entity = dic['deferred_entity']

		entityClass = entityFactory.get_class_by_name(dic['class_name'])
		query = entityClass.all()
		
		results = []

		if key and len(key)>0:
			if deferred_entity and len(deferred_entity)>0:
				parent = entityClass.get(key)
				results = [getattr(parent, deferred_entity)]
			else:
				results = [entityClass.get(key)]
		else:
# $orderby operator
			if ('$orderby' in self.request.str_params):
				orderby_params = self.request.str_params['$orderby'].split(',')
				for orderby_param in orderby_params:
					parts = orderby_param.split(' ')
					field = parts[0]
					order = '' if (len(parts)==1 or parts[1]=='asc') else '-'
					query = query.order('%s%s' % (order, field))

# $filter operator
			if ('$filter' in self.request.str_params):
				filter = self.request.str_params['$filter']
				filter = filter.replace('(', '').replace(')', '')

				if '(' in filter or ')' in filter:	#FIXME : impossible
					self.error(400)
					self.response.out.write("Grouping operators '(' and ')' are not supported\n")
					self.response.out.write("Functions are not supported\n")
					return
				elif ' or ' in filter:
					self.error(400)
					self.response.out.write("Only the 'and' operator is supported by the App Engine Datastore")
					return
				else:
					import re
					filter_params = filter.split(' and ')
					for filter_param in filter_params:
						prop,op,val = filter_param.split(' ')

						if prop.endswith('__key__'):
							prop = prop[:-7]
							val = db.Model.get(core.TYPE_TRANSFORM_FUNCTIONS[db.StringProperty](val)).key()
						else:
							val = core.TYPE_TRANSFORM_FUNCTIONS[getattr(entityClass, prop).__class__](val)

						try:
							op = op.lower()
							OPERATOR_MAPPING = {
								'eq':'=',
								'ne':'!=',
								'gt':'>',
								'ge':'>=',
								'lt':'<',
								'le':'<=',
							}



							query.filter('%s %s'%(prop,OPERATOR_MAPPING[op]), val)
						except:
							import sys

							self.error(400)
							self.response.out.write("Unable to understand expression '%s' : "%filter_param)
							self.response.out.write(str(sys.exc_info()[1]))
							return


# fetch data and $top operator and $skip operator
			nbEntities = int(self.request.str_params['$top']) if ('$top' in self.request.str_params) else core.MAX_FETCH_COUNT
			skipEntities = int(self.request.str_params['$skip']) if ('$skip' in self.request.str_params) else 0
			results = query.fetch(nbEntities, skipEntities)

# format response in json
		response_format = self.request.str_params['$format'] if ('$format' in self.request.str_params) else 'atom'
		if response_format=='atom':
			self.response.headers["Content-Type"] = "application/atom+xml;charset=utf-8"
			self.response.out.write('<?xml version="1.0" standalone="yes"?>')
			self.response.out.write(format_atom(self.request, results))
		elif response_format=='json':
			self.response.headers["Content-Type"] = "application/json;charset=utf-8"
			self.response.out.write(json.encode(results))
		else:
			self.error(406)
			self.response.out.write('%s format is currently not supported' % response_format)


def format_atom(request, results):
	if len(results)==0:	#FIXME
		return

	className = entityFactory.getClassName_fromInstance(results[0], False)
	classFullname = entityFactory.getClassName_fromInstance(results[0], True)

	atom_document = atom.data.Feed(
		title = atom.data.Title(className, type='text'),
		id = atom.data.Id(urllib.unquote(request.url)),
		link = [atom.data.Link(rel='self', title=className, href=className)]
		)
#        atom_document.updated = atom.data.Updated(atom.data.Date(text=datetime.datetime.now().isoformat()))

# the following 2 lines will help reduce the size of the response
	atom_document.attributes['{%s}dummy_atribute'%core.EDMX_METADATA_NAMESPACE] = 'x'
	atom_document.attributes['{%s}dummy_atribute'%core.ODATA_SERVICES_NAMESPACE] = 'x'

	for o in results:
		atom_document.entry.append(core.build_atom_for_entity(o, request.application_url))

	return atom_document



class OData_metadata_handler(webapp.RequestHandler):
	def get(self):
		self.response.headers["Content-Type"] = "application/xml;charset=utf-8"
#		self.response.headers.add_header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")

		self.response.out.write(core.build_metadata_document())

class OData_discovery_handler(webapp.RequestHandler):
#    def post(self):
#        self.get()
	def get(self):
		self.response.headers["Content-Type"] = "application/atom+xml; charset=utf-8"
		self.response.out.write(core.build_discovery_document())
		
