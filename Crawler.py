import re
import urllib2
from bs4 import BeautifulSoup

def spider(url, radius, visited):
	#print url
	#print radius
	domain = get_domain(url)
	comments = []
	try:
		page = urllib2.urlopen(url)
		soup = BeautifulSoup(page, 'html.parser')
		comments.extend(get_comments(soup))
		if (not radius ==0):
			#print "getting links"

			links = get_links_in_domain(soup, domain)
			for link in links:
				if not link in visited:
					visited.append(link)
					comments.extend(spider(link, radius-1, visited))

	except Exception as e:
		print e
		print "error visiting " + url

	return comments

def get_links(soup):
	#	soup = BeautifulSoup(page, 'html.parser')
	#print str(soup)
	
	links = re.findall(r'(?<=href=\").*?(?=\")', str(soup))
	
	return links

def get_links_in_domain(soup, domain):
	final = []
	for link in get_links(soup):
		if domain in link:
			final.append(link)
	return final

def get_comments(soup):
	#<!-- <p>I am!</p> -->
	#//
	comments = re.findall(r'(?<=<!--).*?(?=-->)', str(soup))
	comments.extend(re.findall(r'((\n| |^)(\/\/)).*', str(soup)))
	return comments
	#/**/

def get_domain(url):
	top = url
	url = url.replace("://", "|||")
	if "/" in url:
		top = url.split("/")[0]
	top = top.replace("|||", "://")
	return top

def robot(url):

	robot = get_domain(url) + "/robots.txt"
	print "------------------"
	try:
		robotpage = urllib2.urlopen(robot)
		
		print "robots found!\n"
		soup = BeautifulSoup(robotpage, 'html.parser')
		
		print str(soup)
		#print robot details
	except Exception as e:
		print e
		print "no robots found :("
	print "------------------\n"

def get_cookies(url):
	import requests
	session = requests.Session()
	response = session.get(url)
	return session.cookies.get_dict()

def print_intro():
	print "   -----------------\n"
	print "	  / _ \ "
	print "	\_\(_)/_/ "
	print "	 _//o\\_ "
	print "	  /   \ "
	print "\033[31m"
	print "	 CRAWLER\n"
	print "\033[0m"
	print "   -----------------\n"

def main():
	#visit url
	#start spidering basterds
	print_intro()
	print "Enter initial url:"
	url = raw_input()
	
	try:
		page = urllib2.urlopen(url)
	except Exception as e:
		valid = False
		while valid==False:
			valid = False
			print "invalid url, please re-enter:"
			url = raw_input()
			try:
				page = urllib2.urlopen(url)
			except Exception as e:
				valid = False

	#page and url are valid

	#check for robots
	robot(url)
	print "spidering ...\n"
	try:
		comments = spider(url,1,[])
	except e:
		print e
		print "quitting"

	print "finished!\n"

	flags = [c for c in comments if "flag" in c]
	if (not flags == []):
		print "flags found:"
		#green
		print '\033[92m'
		for comment in flags:
			print comment
		print "\033[0m"

	print "comments found:\n"

	for comment in comments:
		if not comment in flags:
			print comment
	print "------------------"

	cookies = get_cookies(url)
	print "cookies:"
	for key in cookies:
		print key + ": " + cookies[key]

main()


#TODO:
#  - look in css as well
#  - look at cookies
#  - requirements
#  - detect link in clipboard