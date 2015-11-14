#!/usr/bin/env python
import requests, urlparse, sys
""" Pemburu by @Zigoo0 - http://www.Sec-Down.com/ """
""" Specially created for Bug Bounty Hunting! """

headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; rv:30.0) Gecko/20100101 Firefox/33.0',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Accept-Language': 'en-US,en;q=0.5',
			'Accept-Encoding': 'gzip, deflate',
			'Connection': 'keep-alive',
			'Referer': 'http://www.sec-down.com/wordpress/'
			}

class colors:
        def __init__(self):
                self.green = "\033[92m"
                self.blue = "\033[94m"
                self.bold = "\033[1m"
                self.yellow = "\033[93m"
                self.red = "\033[91m"
                self.end = "\033[0m"
color = colors()

#url_parser() parses a domain name and return the domain name + the file path
def url_parser(url):
	parser = urlparse.urlparse(url)
	path = parser.path
	full_domain = parser.netloc
	return path, full_domain


def alter_filename(url):
	file_name = url.split('/')[-1] #Getting the file name from the url
	file_ext = file_name.split('.')[1] #This parameter contains the file extension only.
	file_noext = file_name.split('.')[0] #This parameter contains the file name without extension
	return file_name, file_ext, file_noext


def Filename_Handler(url):
	""" This function will handle the file extension manipulation """
	""" Like adding .tar, .zip etc to the file name """
	file_name, file_ext, file_noext = alter_filename(url)
	#Below is a list of extensions to be used for the filename brute-forcing.
	files = [file_name, "%s.tar"%(file_noext), "%s.rar"%(file_noext), "%s.zip"%(file_noext), "%s.txt"%(file_noext)]
	files += ["%s.old"%(file_name), "%s~"%(file_name),"%s.bak"%(file_name), "%s.tar.gz"%(file_noext)]
	files += ["%s-backup.%s"%(file_noext, file_ext), "%s-bkp.%s"%(file_noext, file_ext), "backup-%s.%s"%(file_noext, file_ext)]
	files += [".%s.%s.swp"%(file_noext, file_ext), "%s.%s"%(file_noext, file_ext)+"s", "_%s.%s"%(file_noext, file_ext)]
	files += ["%s2.%s"%(file_noext, file_ext), "%s.%s_"%(file_noext, file_ext), "%s.%s.gz"%(file_noext, file_ext)]
	files += ["%s_old.%s"%(file_noext, file_ext)]
	return files #returning the list of created files.
	""" Assume that you submitted upload.php, here is the output then: """
	#['upload.php', 'upload.tar', 'upload.rar', 'upload.zip', 'upload.txt', 'upload.php.old', 'upload.php~',
	# 'upload.php.bak', 'upload.tar.gz', 'upload-backup.php', 'upload-bkp.php', 'backup-upload.php']

def Domain_Handler(url):
	""" This function will handle the domain manipulation, """
	""" Like adding .dev, domain1, domain2 etc """
	path, domain_name = url_parser(url)
	#Concatenate the domain name with the domain LTD
	name = domain_name.split('.')[0] #reading the actual domain name
	#Below list will contain the manipulated domains list.
	domains = ['{0}dev'.format(name), '{0}.dev'.format(name), '{0}-dev'.format(name)]
	domains += ['dev{0}'.format(name), 'dev.{0}'.format(name), 'dev-{0}'.format(name)]
	for i in range(1,11):
	#domains += ['{0}1'.format(name), '{0}2'.format(name), '{0}3'.format(name)]
		domains += ['{0}{1}'.format(name, i)]
	return domains
	""" Assume that you submitted portal.domain.com, here is the output then: """
	#['portaldev', 'portal.dev', 'portal-dev', 'devportal', 'dev.portal', 'dev-portal','portal1',
	#'portal2', 'portal3', 'portal4', 'portal5', 'portal6', 'portal7', 'portal8', 'portal9', 'portal10']

def Domains_Hunter(url, headers):
	path, domain_name = url_parser(url) #Handling the URL with url parse
	domains = Domain_Handler(url)
	protocols = ['http://', 'https://'] #Some domains might be using https Only!
	for domain in domains:
		for protocol in protocols:
			try:
				name = domain_name.split('.')[0] #reading the first block in the domain to be replaced.
				new_domain = domain_name.replace(name, domain)
				full_url = protocol + new_domain + path
				print "  [*] Testing %s"%full_url
				requesting = requests.get(full_url, headers=headers, verify=False, timeout=3)
				if requesting:
					print color.green+"  [*] Seems I Hunted below url: %s"%full_url + color.end
			except Exception:
				#print e
				continue

def Files_Hunter(url, headers):
	#headers = headers.headers #this is the headers after reading it from the headers class.
	link_main = url.split('/')[-1] #will replace the file name with the new list of file names.
	files = Filename_Handler(url)
	for filename in files:
		try:
			new_url = url.replace(link_main, filename) #This will replace the filename in the original url
			print "  [*] Testing %s"%new_url
			request = requests.get(new_url, headers=headers, verify=False, timeout=3)
			if request:
				print color.green+"  [*] Seems I Hunted below url: %s"%new_url + color.end
		except Exception:
			#print e
			continue

def link_tester(url):
	#Making sure that the intial request is not 404!
	try:
		request = requests.get(url, headers=headers, verify=False, timeout=3)
		if request.status_code != 200: #keep in mind that python will treat 301 & 302 as 200!
			print "[*] The page is not even there! check your link again."
			exit()
		else:
			pass
	except Exception:
		print "[*] The URL seems to be dead or page is not found!"
		exit()

def execute_with_colors():
	"""
	People using windows will get a lot of errors when running the application because of the coloring class,
	So I created this function to solve this issue, Hopefully!
	"""
	print color.green+""" \n\t\ttPemburu By @Zigoo0 - http://www.Sec-Down.com/ """+color.end
	print color.green+""" \t\tSpecially created for Bug Bounty Hunting! \n"""+color.end
	url = raw_input(color.red+'[*] Enter the URL: '+color.end)
	print color.green+"[*] Testing the provided url ..."+color.end
	link_tester(url)
	print color.blue+"[*] URL seems Ok, Moving to the next phase ... "+color.end
	print color.green+"[*] Hunting for files Started ....."+color.end
	Files_Hunter(url, headers)
	print color.green+"[*] Hunting for domains Started ....."+color.end
	Domains_Hunter(url, headers)	

def execute_no_colors():
	"""
	People using windows will get a lot of errors when running the application because of the coloring class,
	So I created this function to solve this issue, Hopefully!
	"""
	print """ \n\t\tPemburu By @Zigoo0 - http://www.Sec-Down.com/ """
	print """ \t\tSpecially created for Bug Bounty Hunting! \n"""
	url = raw_input('[*] Enter the URL: ')
	print "[*] Testing the provided url ..."
	link_tester(url)
	print "[*] URL seems Ok, Moving to the next phase ... "
	print "[*] Hunting for files Started ....."
	Files_Hunter(url, headers)
	print "[*] Hunting for domains Started ....."
	Domains_Hunter(url, headers)


if __name__ == "__main__":
	os = sys.platform
	if "darwin" in os or "linux" in os:
		execute_with_colors()
	else:
		execute_no_colors()





