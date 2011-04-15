from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

import odata.core

class clientaccesspolicy_handler(webapp.RequestHandler):
	def get(self):
		self.response.headers["Content-Type"] = "application/xml;charset=utf-8"


		self.response.out.write("""<?xml version="1.0" encoding="utf-8"?> 
<access-policy> 
    <cross-domain-access> 
        <policy> 
            <allow-from http-request-headers="*"> 
                <domain uri="*"/> 
            </allow-from> 
            <grant-to> 
                <resource path="/%s" include-subpaths="true"/> 
            </grant-to> 
        </policy> 
    </cross-domain-access>
</access-policy>""" % odata.core.BASE_SVC_URL)


def main():
	clientaccesspolicy_application = webapp.WSGIApplication(
			[
				(r'/clientaccesspolicy.xml' , clientaccesspolicy_handler),
				# (r'/crossdomain.xml' , clientaccesspolicy_handler),
			],
			debug=True
			)
	util.run_wsgi_app(clientaccesspolicy_application)


if __name__ == '__main__':
	main()

