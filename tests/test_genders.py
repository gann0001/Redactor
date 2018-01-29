import redactor
from redactor import redactor

def test_genders():
	text = "He is enrolled into text analytics on January under the professor is Dr. Grant and he is going to meet professor on Sunday. he is also met one girl in the campus. she is also studying in Oklahoma"
	x,d  = redactor.genders(text)
	print(d)
	assert len(d) == 4

