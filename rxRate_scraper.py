# rxrate_scraper.py
# Patrick Ye

# import libraries
import requests
from bs4 import BeautifulSoup


years = range(2006, 2017)

for p in range(len(years)):

	print years[p]
	page_name = 'https://www.cdc.gov/drugoverdose/maps/rxcounty' + str(years[p]) + '.html'

	page = requests.get(page_name)
	soup = BeautifulSoup(page.content, 'html.parser')

	table_list = soup.find_all('table')

	data_table = table_list[0]

	county_list = data_table.find_all('tr')

	county_name_all = []
	state_all = []
	county_code_all = []
	rx_rate_all = []

	for i in range(1, len(county_list)):
		this_county = county_list[i]
	
		td_list = this_county.find_all('td')
	
		#county_name_all.append(td_list[0].get_text())
	
		state_all.append(td_list[1].get_text())
		county_code_all.append(td_list[2].get_text())

		rx_rate = td_list[3].get_text()

		if rx_rate.encode('ascii', 'replace') == '?':
			rx_rate_all.append('NaN')
		else:
			rx_rate_all.append(rx_rate)


	## save to csv
	import csv

	filename = 'rxrate_' + str(years[p]) + '.csv'
	with open(filename, 'w') as f:
		data_writer = csv.writer(f)
		for j in range(len(state_all)):
	#		row = [county_code_all[j], 'kk']
			row = [state_all[j], county_code_all[j], rx_rate_all[j]]
		
			data_writer.writerow(row)
	