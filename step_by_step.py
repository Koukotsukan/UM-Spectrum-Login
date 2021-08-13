import requests
import re

account = "#YOUR ACCOUNT WITHOUT EMAIL SUFFIX"
password = "#YOUR PASSWORD"
url = "https://spectrum.um.edu.my"
casvURL = "https://casv.um.edu.my/cas/loginAllType?service=https://spectrum.um.edu.my/login/index.php"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:90.0) Gecko/20100101 Firefox/90.0"
}
# Get the original cookies
getCookie = requests.get(url, headers=headers)
cookieJar = getCookie.cookies
cookieDict = requests.utils.dict_from_cookiejar(cookieJar)
cookies = cookieDict["MoodleSession"]
print("cookies: " + cookies)

# Get Lt for captcha evaluation
getLt = requests.get(casvURL, headers=headers)
lt = re.findall("<input type=\"hidden\" name=\"lt\" value=\"(.*)\" />", getLt.text)[0]
print("lt: " + lt)
casvCOOKIEJAR = getLt.cookies
casvCOOKIEDICT = requests.utils.dict_from_cookiejar(casvCOOKIEJAR)
casvCOOKIES = casvCOOKIEDICT["JSESSIONID"]
print("casv: " + casvCOOKIES)

data = {
    "uname": account,
    "password": password,
    "domain": "@perdana.um.edu.my",
    "lt": lt,
    "_eventId": "submit",
    "username": account + "@perdana.um.edu.my"
}
# Get location from header to register your original cookies
getLocation = requests.post(
    url="https://casv.um.edu.my/cas/loginAllType;jsessionid=" + casvCOOKIES + "?service=https://spectrum.um.edu.my/login/index.php",
    headers=headers, data=data, allow_redirects=False)
location = getLocation.headers['location']
print("location: " + location)

# Register your cookies
registerHeaders = {
    "Cookie": "MoodleSession=" + cookies,
}
registerCookie = requests.get(location, headers=registerHeaders)
getNewCookieURL = "https://spectrum.um.edu.my/login/index.php"
getNewCookieHeaders = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:90.0) Gecko/20100101 Firefox/90.0",
    "Cookie": "MoodleSession=" + cookies
}
getNewCookie = requests.get(getNewCookieURL, headers=getNewCookieHeaders)
# Test if we are logged in
print("logged in: " + str(re.findall("Niu Zhaohang", getNewCookie.text)))

loginHeaders = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:90.0) Gecko/20100101 Firefox/90.0",
    "Cookie": "MoodleSession=" + cookies
}
login = requests.get(url, headers=loginHeaders)
# Test activated cookie
print("activated cookie: " + str(re.findall("'Set-Cookie': 'MoodleSession=(.*); path=", str(login.headers))))
