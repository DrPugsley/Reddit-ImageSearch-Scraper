#! /usr/bin/python3
import praw, os, sys
from bs4 import BeautifulSoup
import requests
from requests import get
import time

# Setting Variables
client_id = " "
client_secret = " "
subname = sys.argv[1]
reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent='Text Post Archiver')
searching = sys.argv[2:]
searched = ' '.join(sys.argv[2:])

if client_id == " " or client_secret == " ":
	print("You have to put your client_id and client_secret in the script or it won't work!")
	sys.exit()

print("Searching for "+searched+" in /r/"+subname)
def download(url, file_name):
    with open(file_name, "wb") as file:
        response = get(url)
        file.write(response.content)

start = time.time()
# Making directory with the title of the selected subreddit
os.makedirs(subname+' - '+searched, exist_ok=True)
os.chdir(subname+' - '+searched)
global imgnumber
imgnumber = 0
subnumber = 0
postlist = []
print("Gathering post URLs...")
for submission in reddit.subreddit(subname).search(searched, limit=None):
	postlist.append(submission.url)
	subnumber += 1
	posturls = open("Links.txt", "a")
	posturls.write(submission.url+'\n')
	posturls.close()
print("Done! Got "+str(subnumber)+" posts.")
global dled
dled = []
for postarino in postlist:
	if "imgur.com" in postarino:
		
		if ".jpg" in postarino or ".png" in postarino or ".gif" in postarino or ".jpeg" in postarino:
			if "gifv" in postarino:
				newurl = postarino.replace("gifv","mp4")
				imgnumber += 1
				print("Downloading Image #"+str(imgnumber)+" Url: "+postarino)
				filename, file_extension = os.path.splitext(newurl)
				download(newurl, str(imgnumber)+file_extension)
			else:
				imgnumber += 1
				print("Downloading Image #"+str(imgnumber)+" Url: "+postarino)
				filename, file_extension = os.path.splitext(postarino)
				download(postarino, str(imgnumber)+file_extension)
		else:
			html_page = requests.get(postarino)
			soup = BeautifulSoup(html_page.text, "html.parser")
			for img in soup.findAll('img'):
				image = img.get('src')
				fullurl = 'http:'+image
				if "imgur" in image and "s.imgur" not in image and fullurl not in dled:
					imgnumber += 1
					print("Downloading Image #"+str(imgnumber)+" Url: "+postarino)
					filename, file_extension = os.path.splitext(fullurl)
					download(fullurl, str(imgnumber)+file_extension)
					dled.append(fullurl)
				else:
					for vid in soup.findAll('source'):
						getvid = vid.get('src')
						fullurl = 'http:'+getvid
						if fullurl not in dled:
							imgnumber += 1
							print("Downloading Image #"+str(imgnumber)+" Url: "+postarino)
							filename, file_extension = os.path.splitext(fullurl)
							download(fullurl, str(imgnumber)+file_extension)
							dled.append(fullurl)
	#elif ".jpg" in postarino or ".png" in postarino or ".gif" in postarino or ".jpeg" in postarino:
		#imgnumber+= 1
		#print("Downloading image #"+str(imgnumber))
		#if "gifv" in postarino:
			#newurl = postarino.replace("gifv","mp4")
		#	urlgrab(newurl)
		#else:
		#	urlgrab(postarino)
	elif "gfycat.com" in postarino:
		html_page = requests.get(postarino)
		soup = BeautifulSoup(html_page.text, "html.parser")
		for vid in soup.findAll('source'):
			getid = vid.get('id')
			if getid == "webmSource" and postarino not in dled:
				getvid = vid.get('src')
				imgnumber += 1
				print("Downloading Image #"+str(imgnumber)+" Url: "+postarino)
				filename, file_extension = os.path.splitext(getvid)
				download(getvid, str(imgnumber)+file_extension)
				dled.append(postarino)

	elif "i.redd.it" in postarino or "i.reddituploads.com" in postarino:
		
		imgnumber += 1
		print("Downloading Image #"+str(imgnumber)+" Url: "+postarino)
		filename, file_extension = os.path.splitext(postarino)
		download(postarino, str(imgnumber)+file_extension)

	elif ".jpg" in postarino or ".png" in postarino or ".gif" in postarino or ".jpeg" in postarino or ".webm" in postarino or ".mp4" in postarino:
		
		print("Trying unrecognized link: "+postarino)
		try:
			imgnumber += 1
			print("Downloading Image #"+str(imgnumber)+" Url: "+postarino)
			filename, file_extension = os.path.splitext(postarino)
			download(postarino, str(imgnumber)+file_extension)
		except:
			print("Failed")
			pass

	elif "reddit.com/r/" in postarino or "youtu.be" in postarino or "youtube.com" in postarino:
		print("Not an image link, skipping")

	else:
		
		nondirect = open("Unsupported links", "a")
		nondirect.write(postarino+'\n')
		print("Not supported: "+postarino)
print('Finished! Downloaded '+str(imgnumber)+' files in'+' {0:0.1f} seconds'.format(time.time() - start))
