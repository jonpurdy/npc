#!/usr/bin/env python

import requests
import xml.etree.ElementTree as etree 
import sys

# original curl command:
# curl 'http://nikeid.nike.com/services/is_profane' -H 'Content-Type: application/x-www-form-urlencoded' --data 'appFlag=Nike_ID&levelCode=is_blocked&xml=%3Croot%3E%3Cword%3E'"hello"'%3C%2Fword%3E%3C%2Froot%3E'

def main():

	# get the user's input for the word to be checked
	word_to_be_checked = input("Enter the word to be checked: ")

	# submits the word and returns back true or false
	is_allowed = get_result_from_nike(word_to_be_checked)

	# cleanly print the result
	if is_allowed:
		print("Nike considers the word '%s' to be clean." % word_to_be_checked)
	else:
		print("Nike considers the word '%s' to be profane." % word_to_be_checked)


def get_result_from_nike(word_to_be_checked):

	headers = {
	    'Content-Type': 'application/x-www-form-urlencoded',
	}

	data = {
	  'appFlag': 'Nike_ID',
	  'levelCode': 'is_blocked',
	  'xml': '<root><word>%s</word></root>' % word_to_be_checked
	}

	try:
		print("Submitting request to Nike...")
		result = requests.post('http://nikeid.nike.com/services/is_profane', headers=headers, data=data)
	except Exception as e:
		print(e)
		sys.exit()

	tree = etree.fromstring(result.text)

	for element in tree:
		if element.tag == 'rs':
			for thing in element.attrib:
				if thing == 'isAllowed':
					is_allowed = element.attrib[thing]

	if is_allowed == "true":
		is_allowed = True
	else:
		is_allowed = False

	return is_allowed

if __name__ == '__main__':
	main()