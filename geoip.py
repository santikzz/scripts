import sys
import json
import requests
import os

if __name__ == '__main__':
		
	if (len(sys.argv) > 1):
		ip = sys.argv[1]
	else:
		ip = requests.get('https://api.ipify.org/').text
	
	info = json.loads(requests.get('http://ipinfo.io/'+ip).text)

	country = info['country']
	if os.path.exists('countrycodes.json'):
		with open('countrycodes.json') as f:
			countries = json.loads(f.read())
		country = countries[country]

	print(f"""
===========================================================
	   
IP ADDRESS:		{info['ip']}
LOCATION:		{info['city']} ({info['postal']}) - {info['region']} - {country}
APROX. COORDS:		{info['loc']}
TIMEZONE:		{info['timezone']}
HOSTNAME:		{info['hostname']} ({info['org']})

===========================================================
""")
