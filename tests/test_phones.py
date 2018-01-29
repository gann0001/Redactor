import redactor
from redactor import redactor

def test_phones():
	text = "Sumith Gannarapu phone number is (405)-654-6354 and Naveen phone number is 405.464.2839"
	d  = redactor.phones(text)
	assert len(d) == 2

