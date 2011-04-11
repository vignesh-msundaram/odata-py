import core


class _factory(list):
	def append(self, value):
		if value in self:
			pass
		else:
			list.append(self, value)

INSTANCE = _factory()


def getClassName_fromInstance(o, fullName):
	name = o.__class__.__name__
	if fullName:
		name = o.__module__ + "." + name
	return name 


def guess_module(class_name):
	for m in INSTANCE:
		if m.__name__== class_name:
			return m.__module__


def get_class_by_name(class_name):
	# this could be much faster if we directly used the factory INSTANCE
	module = guess_module(class_name)
	python_module = __import__(module, globals(), locals(), [class_name])
	entityClass = getattr(python_module, class_name)
	return entityClass


def create_entity_from_atomEntry(entry):
	category = entry.category[0].term
	i = category.rfind('.')+1
	class_name = category[i:]
	entityClass = get_class_by_name(class_name)

	props = core.get_edmProperties_from_entry(entry);
		
	return apply(entityClass, (), props)

