import redactor
from redactor import unredactor

def test_dict():
	count = 0
	text_list = ["Trump sent a powerful message to those who doubt his will to fight anti-Semitism — and to his own supporters in the white nationalist movement — during an annual Holocaust remembrance ceremony at the Capitol on Tuesday"]
	d,n  = unredactor.entities(text_list)
	print(d,n)
	for each in d:
		count = count+1
	assert count == 3

