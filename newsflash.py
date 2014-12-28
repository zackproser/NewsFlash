import alchemyapi
alchemyapi = alchemyapi.AlchemyAPI()
from bs4 import BeautifulSoup
import urllib3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#Dictionaries to Hold Final Report
report_headlines = [];
report_keywords = [];

def send_email_report():
	#Set up Email Config
	myaddr = 'YOUR-GMAIL-ADDRESS'
	msg = MIMEMultipart('alternative')
	msg['Subject'] = "Newsflash Report"
	msg['From'] = 'me'
	msg['To'] = 'me'
	
	prepared_headlines = []
	for d in report_headlines: 
		prepared_headlines.append('<li>From ' + d['source'] + ' <a href="' + d['href'].encode('utf-8') + '">' + d['title'] + '</a><br>\n')

	html = '<h2>Newsflash: Headlines</h2>'
	html += '<ul style="max-height:300px;overflow-y:scroll;border:1px solid grey;">'
	#Insert headline links
	for link in prepared_headlines:
		html+= link
	html += '</ul><hr><br><br>'

	#Begin Keywords Section
	html += '<h2>Newsflash: Keywords</h2>'
	html += '<ul style="max-height:300px;overflow-y:scroll;border:1px solid grey;">'
	#Insert Keywords
	for keyword in report_keywords:
		html += '<li>' + keyword + '</li>'
	html += '</ul>'

	#Prepare Plaintext & HTML E-mail Sections
	text = "Newsflash Report"
	part1 = MIMEText(text, 'plain')
	part2 = MIMEText(html, 'html')

	msg.attach(part1)
	msg.attach(part2)

	username = 'YOUR-GMAIL-USERNAME'
	password = 'YOUR-GMAIL-PASSWORD'

	#Send E-mail
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.starttls()
	server.login(username, password)
	server.sendmail(myaddr, myaddr, msg.as_string()); 
	print "NewsFlash Report Sent!"
	server.quit()

def get_page(target_address):
	http = urllib3.PoolManager()
	r = http.request('GET', target_address)
	print "NewsFlash Running..."
	if r.status == 200: 
		print "Successfully retrieved: " + target_address
		page_html = r.data
		return page_html
	else:
		print "Error retrieving: " + target_address

def get_nytimes_headlines():
	target_address = "http://www.nytimes.com"
	content = get_page(target_address)
	soup = BeautifulSoup(content)
	data = []
	for h2 in soup.findAll("h2", {"class":"story-heading"}):
		a_element = h2.find("a", href=True)
		if a_element:
		   data.append({ 'title': a_element.get_text(), 'href': a_element['href'], 'source': 'NYTimes'})
	#Clean NoneTypes from Titles Array
	data = filter_titles(data)
	keywords_string = ''; 
	for item in data:
		keywords_string += item['title']
		report_headlines.append(item)
	extract_keywords(keywords_string)

def get_bbc_world_headlines():
	target_address = "http://www.bbc.com/news/world/"
	content = get_page(target_address)
	soup = BeautifulSoup(content)
	data = []
	for a in soup.findAll("a", {"class":"story"}, href=True):
		data.append({ 'title': a.get_text(), 'href': a['href'], 'source': 'BBC World'})
	#Clean NoneTypes from Titles Array
	data = filter_titles(data)
	keywords_string = '';
	for item in data:
		keywords_string += item['title']
		report_headlines.append(item)
	extract_keywords(keywords_string)

def extract_keywords(content):
	response = alchemyapi.keywords('text', content, {'sentiment':1})
	if response['status'] == 'OK':
		text_keywords = []
		for keyword in response['keywords']:
			text_keywords.append(keyword['text'].encode('utf-8'))
		for keyword in text_keywords:
			report_keywords.append(keyword);
	else: 
		print('Error in keyword extraction call: ', response['statusInfo'])


def filter_keywords(data):
	clean_data = []
	for d in data: 
		if d is not None: 
			if type(d == 'str'):
				clean_data.append(d)
	return clean_data

def filter_titles(data):
	clean_data = []
	for d in data:
		if d['title'] is not None:
			if type(d['title']=='unicode'):
				d['title'] = d['title'].encode('utf-8')
				d['title'] = d['title'].replace('\xe2\x80\x99',"'")
				d['title'] = d['title'].decode('string_escape')
				d['title'] = d['title'].strip()
				d['href'] = d['href'].encode('utf-8')
				d['href'] = d['href'].strip()
				#BBC Uses Mixture of Relative Links - Build Them Out
				if d['href'].startswith('/news',0,5):
					d['href'] = "http://news.bbc.co.uk" + d['href']
				clean_data.append(d)
	return clean_data

#I'm Ron Burgundy?
def read_the_news():
	get_nytimes_headlines()
	get_bbc_world_headlines() 
	send_email_report()

read_the_news()