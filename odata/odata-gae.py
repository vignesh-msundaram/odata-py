from google.appengine.ext import webapp
from google.appengine.ext.webapp import util



import odata.core
import odata.wsgi





# supported operators:
#  fetch by KEY
#  /Description
#  $top
#  $skip
#  $orderby
#  $format=json

# roadmap:
#   faster reflection and imports (import the types only once)
#   support key_name non-system-assigned key names
#   try to not call getClassName_fromInstance too many times

def main():
# rendre cet URL configurable
	import model
	odata.entityFactory.INSTANCE.append(model.Pet)
	odata.entityFactory.INSTANCE.append(model.SecondModel)

	odata_application = webapp.WSGIApplication(
			[
				(r'/%s/\$metadata'      % odata.core.BASE_SVC_URL, odata.wsgi.OData_metadata_handler),
				(r'/%s/%%24metadata'    % odata.core.BASE_SVC_URL, odata.wsgi.OData_metadata_handler),
				(r'/%s/\$metadata/.*'   % odata.core.BASE_SVC_URL, odata.wsgi.OData_metadata_handler),
				(r'/%s/%%24metadata/.*' % odata.core.BASE_SVC_URL, odata.wsgi.OData_metadata_handler),

				(r'/%s/$' % odata.core.BASE_SVC_URL, odata.wsgi.OData_discovery_handler),

				(r'/%s/.*' % odata.core.BASE_SVC_URL, odata.wsgi.OData_handler),

			],
			debug=True
			)
	util.run_wsgi_app(odata_application)


if __name__ == '__main__':
	main()

