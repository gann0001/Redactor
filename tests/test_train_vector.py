import redactor
from redactor import unredactor

def test_train_entity():
	text_list = "****** ********* is enrolled into text analytics"
	d,n  = unredactor.test(text_list)
	print(d,n)
	assert len(n) == 1

