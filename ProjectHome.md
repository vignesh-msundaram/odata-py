## Overview ##
There is a vast amount of data available today and data is now being collected and stored at a rate never seen before. Much of this data is managed by Java server applications and difficult to access or integrate into new uses.

The [Open Data Protocol (OData)](http://www.odata.org/) is a Web protocol for querying and updating data that provides a way to unlock this data and free it from silos that exist in applications today. OData does this by applying and building upon Web technologies such as HTTP, [Atom Publishing Protocol (AtomPub)](http://www.ietf.org/rfc/rfc4287.txt) and [JSON](http://json.org/) to provide access to information from a variety of applications, services, and stores.

## Project info ##
odata-py is an open-source OData provider for Google App Engine Datastore, written in python.

### Status ###
Due to the particularity and [restrictions](http://code.google.com/appengine/docs/python/datastore/gqlreference.html) ([NoSQL](http://en.wikipedia.org/wiki/NoSQL_(concept))) on the AppEngine's datastore, some functionalities of OData are not supported.

### Supported functionalities ###
  * Service document
  * Service Metadata Document (CSDL)
  * HTTP GET (read entities)
    * $top operator
    * $skip operator
    * $format operator (only atom is fully supported, JSON is partially supported)
    * $filter operator
      * Eq (=) operator
      * Ne (!=) operator
      * Gt (>=) operator
      * Ge (>) operator
      * Lt (<) operator
      * Le (<=) operator
      * logical 'And' operator
    * $orderby operator
  * HTTP MERGE (update entities)
  * HTTP POST (create entities)

### Limitations due to Google App Engine Datastore ###
  * the logical operator 'Or' is not supported
  * all HTTP POST/MERGE/PUT requests must be [tunnelled](http://www.odata.org/developers/protocols/operations#MethodTunnelingthroughPOST) through POST
  * more limitations listed [here](http://code.google.com/appengine/docs/python/datastore/queries.html#Restrictions_on_Queries), especially :
    * Inequality Filters Are Allowed on One Property Only
    * Properties in Inequality Filters Must Be Sorted before Other Sort Orders
    * Sort Orders Are Ignored on Properties With Equality Filters
    * Filtering Or Sorting On a Property Requires That the Property Exists
    * No Use of Filters That Match Entities Missing a Property

### Roadmap (in order of priority) ###
  * $expand operator
  * $inlinecount operator
  * $select operator
  * Support Expandos
  * Complete JSON support

## Want to contribute ? ##
  * [Submit an issue](http://code.google.com/p/odata-py/issues/list)
  * submit code fixes/evolution : [ask to be member](mailto:andriniaina@gmail.com) and i'll add your login to the project members

## Downloads & Releases ##
The project is still in its early stages: there is no official release yet. You can get a glimpse preview by downloading the source code and unit tests [here](http://code.google.com/p/odata-py/source/checkout)