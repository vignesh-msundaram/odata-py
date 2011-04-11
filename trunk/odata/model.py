
from google.appengine.ext import db

class Pet(db.Model):
    name = db.StringProperty(required=True)
    type = db.StringProperty(required=True, choices=set(["cat", "dog", "bird"]))
    birthdate = db.DateProperty()
    weight_in_pounds = db.IntegerProperty()
    spayed_or_neutered = db.BooleanProperty()
#    owner = db.UserProperty()



class SecondModel(db.Model):
    myPet = db.ReferenceProperty(Pet)
	
