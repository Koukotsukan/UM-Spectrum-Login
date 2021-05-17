import requests
import re

def login():
	uname = "YOUR USER NAME"
	password = "YOUR PASSWORD"
	s = requests.session()
	url = "https://casv.um.edu.my/cas/loginAllType?service=https%3A%2F%2Fspectrum.um.edu.my%2Flogin%2Findex.php"
	sourceCode = s.get(url)
	lt = re.findall('value="(.*)"', str(re.findall('<input type="hidden" name="lt" value=".*" />', sourceCode.text)))[0]
	print(lt)
	data = {
		"uname": uname,
		"password": password,
		"domain": "@perdana.um.edu.my",
		"lt": lt,
		"_eventId": "submit",
		"username": uname + "@perdana.um.edu.my",
	}
	spectrumHomepage = s.post(url, data=data)
	cookie = s.cookies.get_dict()
	print(cookie)
	try:
		if cookie["MoodleSession"]:
			print("login success")
	except:
		print("login failed")

if __name__ == '__main__':
	login()
	
