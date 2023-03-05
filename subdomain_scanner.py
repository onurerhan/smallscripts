import tools.subdomain_scanner.censys_sub as censys_sub
import tools.subdomain_scanner.subbrute as subbrute
import tools.subdomain_scanner.ctfr as ctfr
import tools.subdomain_scanner.sublist3r as sublist3r
from datetime import datetime

# 250 queries a month in free version
censys_id = "f2ba0491-0a8a-4b85-8ea2-9bf9cec7fca1"
censys_secret = "xfgaAbFIMlMihC55dv2zrjSmOJIzlLnj"


def subdomain_filter(domain, subdomains):  # If subdomain has *.domain.com It will filter out from list of subdomains.
	subdomains = list(subdomains)
	returnlist = []
	for subdomain in subdomains:
		if subdomain not in returnlist and '*.' + domain not in subdomain and subdomain.endswith(domain):
			returnlist.append(subdomain)
	return returnlist


def write_list_to_file(domain, subdomains, output_file):
	if len(subdomains) is 0:
		print('[-] Did not find any subdomain in ' + domain)
		return

	print('[*] Found %d unique subdomain' % (len(subdomains)))
	output = open(output_file, 'w')
	for subdomain in subdomains:
		output.write(str(subdomain) + '\n')
	output.close()


def main(domain, output_file, ctfr_toggle=True, censys_toggle=True, subbrute_toggle=True, sublist3r_toggle=True):
	start = datetime.now()
	subdomains = []
	if ctfr_toggle:  # finds subdomains using Certificate Transparency logs
		start_ctfr = datetime.now()
		try:
			print("Trying ctfr")
			ctfr_result = ctfr.get_crt_data(domain, subdomains)
			print("\tFound %d subdomains" % len(ctfr_result))
			subdomains.extend(ctfr_result)
		except Exception as e:
			print("Failed ctfr")
			print(e)
		finish_ctfr = datetime.now()
		print("Ctfr run time: " + str(finish_ctfr - start_ctfr))

	if censys_toggle:  # finds subdomains with censys api. Free version gives error on more than ~50 subdomains
		start_censys = datetime.now()
		try:
			print("Trying censys")
			censys_result = censys_sub.subdomain_find(domain, censys_id, censys_secret)
			subdomains.extend(censys_result)
			print('\tFound %d subdomains' % (len(censys_result)))
		except Exception as e:
			print("Failed censys")
			print(e)
		finish_censys = datetime.now()
		print("Censys run time: " + str(finish_censys - start_censys))

	if subbrute_toggle:  # finds a lot more subdomains with bruteforce but takes ~30mins with my internet
		start_subbrute = datetime.now()
		try:
			print("Trying subbrute")
			subbrute_result = []
			for x in subbrute.run(domain):
				if x[0] not in subbrute_result:
					subbrute_result.append(x[0])
			print('\tFound %d subdomains' % (len(subbrute_result)))
			subdomains.extend(subbrute_result)
		except Exception as e:
			print("Failed subbrute")
			print(e)
		finish_subbrute = datetime.now()
		print("Subbrute run time: " + str(finish_subbrute - start_subbrute))

	if sublist3r_toggle:  # finds subdomains from search engines
		start_sublist3r = datetime.now()
		try:
			print("Trying sublist3r")
			sublist3r_result = sublist3r.main(domain, 40, savefile=False, ports=None, silent=True, verbose=False,
												enable_bruteforce=False, engines=None)
			subdomains.extend(sublist3r_result)
			print('\tFound %d subdomains' % (len(sublist3r_result)))
		except Exception as e:
			print("Failed sublist3r")
			print(e)
		finish_sublist3r = datetime.now()
		print("Subbrute run time: " + str(finish_sublist3r - start_sublist3r))

	subdomains = subdomain_filter(domain, subdomains)
	write_list_to_file(domain, subdomains, output_file)
	finish = datetime.now()
	print("Total runtime: " + str(finish - start))


if __name__ == "__main__":
	url = 'dijitalsaha.com'
	main(url, url + '.txt', subbrute_toggle=False)
