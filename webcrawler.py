import requests, os
from bs4 import BeautifulSoup

def downloadStationLayouts():

	# make directory if already not present
	if not os.path.exists(os.getcwd() + "\\stations"):
		os.makedirs(os.getcwd() + "\\stations")

	# URL from which pdfs to be downloaded
	url = "https://www.mtr.com.hk/en/customer/services/system_map.html"

	# Requests URL and get response object
	response = requests.get(url)

	# Parse text obtained
	soup = BeautifulSoup(response.text, 'html.parser')

	# Names of all stations
	names = soup.find_all('td')
	names = names[0::3]

	# Find all hyperlinks present on webpage
	links = soup.find_all('a')
	links = links[3::2]

	i = 0

	# From all links check for pdf link and
	# if present download file

	for link in links:
		if ('.pdf' in link.get('href', [])):
			i += 1
			print("Downloading file ", i+":", str(names[i-1])[4:-5]+"....")

			# Get response object for link
			response = requests.get("https://www.mtr.com.hk"+link.get('href'))
			
			# Write content in pdf file
			with open("stations/"+str(names[i-1])[4:-5]+".pdf",'wb') as f:
				f.write(response.content)

	print("All PDF files downloaded")