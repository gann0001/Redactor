import redactor
from redactor import redactor
#from redactor import dates
def test_plaes():
	text = "The City of New York, Dallas, California are the most populous city in the United States."
	entity_places  = redactor.places(text)
	places = ['New York','Dallas','California', 'United States']
	len_places = 4
	for key in entity_places.keys():
		print(entity_places[key])
		length = len(entity_places[key])
	assert length == len_places
