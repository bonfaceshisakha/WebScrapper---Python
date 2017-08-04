import csv
from bs4 import BeautifulSoup as soup
import urllib.request as urlRequest

# Open CSV file
with open('todayMatches.csv') as csvfile:
	# To read from CSV
	reader = csv.DictReader(csvfile)
	counter = 0

	# Save result in csv
	filename = "todayTips.csv"
	f = open(filename, "w")

	# CSV headers
	headers = "match, competition, tip, tipster_rating,\n "
	f.write(headers)
	
	# Traverses each url from CSV file
	for row in reader:
		
		# Variables i.e. url & client header
		url = row['url']
		headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
		

		# Pretends to be a browser in order to establish connection
		req = urlRequest.Request(url, headers=headers)
		uClient = urlRequest.urlopen(req)

		# While connected, save content of the page to a text file
		raw_html = uClient.read()

		# html parsing
		pretify_html = soup(raw_html, "html.parser")


		containers = pretify_html.findAll("li", {"class":"feed-item"})

		# Traverses each element in containers
		for container in containers:
			# Splits texts into elements in a list
			raw_data = container.text.split("\n")
			 
			# Remove white spaces from the list
			data = [x for x in raw_data if x != '']

			if container.find("span", {"class":"scope-1"}):
				p_type = " FT" 

			else:
				p_type = " HT"

			if len(data) > 9:

				# Assign values to variables
				teams = data[2]
				competition = data[3]

				ratings = 0

				if "+" in data[8]:
					ratings = data[8]				
					tip = data[4] + p_type


				if "+" in data[9]:
					ratings = data[9]

					if container.find("span", {"class":"entypo-up-dir"}):
						tip = "Over " + data[5]	+ p_type	

					if container.find("span", {"class":"entypo-down-dir"}):
						tip = "Under " + data[5] + p_type

			if ratings != 0:				
				f.write(teams + "," + competition + "," + tip + "," + ratings + "\n")
				
		counter+= 1
		print("End of Match " + str(counter))
		print("********************************************************")

	f.close()