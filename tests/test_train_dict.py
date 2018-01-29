import redactor
from redactor import unredactor

def test_train_dict():
	count = 0
	text_list = "****** ********* is enrolled into text analytics"
	d,n  = unredactor.test(text_list)
	print(d,n)
	for each in d:
		count = count+1
	assert count == 1

