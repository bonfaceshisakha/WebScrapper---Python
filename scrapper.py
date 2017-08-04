from bs4 import BeautifulSoup as soup
import urllib.request as urlRequest

# Variables i.e. url & client header
myUrl = 'https://www.bettingexpert.com/clash/all-matches-today'
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
rootUrl = 'https://www.bettingexpert.com'

# Pretends to be a browser in order to establish connection
req = urlRequest.Request(myUrl, headers=headers)
uClient = urlRequest.urlopen(req)

# While connected, save content of the page to a text file
raw_html = uClient.read()

# html parsing
pretify_html = soup(raw_html, "html.parser")

containers = pretify_html.findAll("li",{"class":"row"})

# Save result in csv
filename = "todayMatches.csv"
f = open(filename, "w")

# CSV headers
headers = "date, start_time, country, competition, home_team, home_score,away_team, away_score,url,\n "
f.write(headers)

for container in containers:
	
	raw_data = container.div.text.split("\n")

	raw_time = raw_data[0].split(",")

	# Date and time of match
	start_time = raw_time[0]
	date = raw_time[1]

	# Teams
	home_team = raw_data[3]
	away_team = raw_data[7]

	# Competition
	raw_competition = raw_data[9].split(",")
	competition = raw_competition[0]
	country_data = raw_competition[1].split("-")
	country = country_data[0]

	# Scores
	home_score = raw_data[1]
	away_score = raw_data[5]

	# Individual urlRequest
	url_raw = container.find("a")
	url = url_raw.get('href')

	finalUrl = rootUrl + url
	
	f.write(date + "," + start_time + "," + country + "," + competition + "," + home_team + "," + home_score + "," + away_team + "," + away_score + "," + finalUrl +"\n")

 
f.close()
	