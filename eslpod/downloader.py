#!/bin/python

import re
import http.client
import urllib.request

# Find links

website = http.client.HTTPConnection('www.eslpod.com')
pattern = re.compile('http://(?:media.)?libsyn.com/media/eslpod/.*.mp3')

def findLinks(offset):
	website.request('GET', '/website/show_all.php?cat_id=-59456&low_rec=' + str(offset))
	page = website.getresponse().read().decode('ISO-8859-1')
	return pattern.findall(page)

links = []

offset = 0
while True:
	pageLinks = findLinks(offset);
	if len(pageLinks) == 0:
		break
	links += pageLinks
	offset += 20

# Transfer files

def filename(url):
	return url[url.rfind('/') + 1:]

def download(url):
	stream = urllib.request.urlopen(url)
	outputFile = open(filename(url), 'wb')
	outputFile.write(stream.read())
	outputFile.close()
	stream.close()

for link in links:
	download(link)