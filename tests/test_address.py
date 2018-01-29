import redactor
from redactor import redactor

def test_address():
	text = "Sumith Gannarapu address is 1003 E Brooks St, Apt A Norman, OK 73071. $umith's friend Naveen's address is also 1003 E Brooks St, Apt A, Norman, OK 73071, I would like to stay in Cupertino so the address of the camp is 4201 Fanboy Lane, Cupertino CA 88421"
	d  = redactor.address(text)
	assert len(d) == 3

