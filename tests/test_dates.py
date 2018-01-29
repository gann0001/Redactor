import redactor
from redactor import redactor

def test_dates():
	dates = ['Sunday','January']
	dates_len = 2
	text = "Sumith Gannarapu is enrolled into text analytics on January under the professor is Dr. Grant and he is going to meet professor on Sunday"
	d  = redactor.dates(text)
	assert len(d) == dates_len

