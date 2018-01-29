import redactor
from redactor import unredactor

def test_dates():
	count = 0
	text_list = ["Sumith Gannarapu is enrolled into text analytics"]
	d,n  = unredactor.entities(text_list)
	print(d,n)
	for each in d:
		count = count+1
	assert count == 3
	assert len(n) == 3

