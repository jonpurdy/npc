#!/usr/bin/env python

import requests
import xml.etree.ElementTree as etree 

# original curl command:
# curl 'http://nikeid.nike.com/services/is_profane' -H 'Content-Type: application/x-www-form-urlencoded' --data 'appFlag=Nike_ID&levelCode=is_blocked&xml=%3Croot%3E%3Cword%3E'"hello"'%3C%2Fword%3E%3C%2Froot%3E'

def main():
	
	word_to_be_checked = input("Enter the word to be checked: ")

	headers = {
	    'Content-Type': 'application/x-www-form-urlencoded',
	}

	data = {
	  'appFlag': 'Nike_ID',
	  'levelCode': 'is_blocked',
	  'xml': '<root><word>%s</word></root>' % word_to_be_checked
	}

	result = requests.post('http://nikeid.nike.com/services/is_profane', headers=headers, data=data)

	tree = etree.fromstring(result.text)

	for element in tree:
		if element.tag == 'rs':
			for thing in element.attrib:
				if thing == 'isAllowed':
					is_allowed = element.attrib[thing]

	if is_allowed == "true":
		print("Nike considers the word '%s' to be clean." % word_to_be_checked)
	else:
		print("Nike considers the word '%s' to be profane." % word_to_be_checked)

if __name__ == '__main__':
	main()