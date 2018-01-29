import redactor
from redactor import redactor
#from redactor import dates
def test_names():
	text = "This fanciful horror flick has Vincent Price playing a mad magician that realizes his vocational talents have been sold to another. He devise ways of avenging all those that have wronged him. His master scheme seems to back fire on him. Price is a little below par compared to his masterpieces, but is still the only reason to watch this thriller. Supporting cast includes Patrick O'Neal, Mary Murphy, Eva Gabor and Jay Novello."
	names = ['Vincent', 'Mary Murphy', 'Eva Gabor', 'Jay Novello', "Patrick O'Neal"]
	names_len = 5
	entity_names  = redactor.names(text)
	for key in entity_names.keys():
		print(entity_names[key])
		length = len(entity_names[key])
	assert length == names_len

