from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector
import requests
import logging
import os


def parse_url(url):
	logging.debug('Getting URL: %s', url)
	request = requests.Session()
	request.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'
	resp = request.get(url)
	http_encoding = resp.encoding if 'charset' in resp.headers.get('content-type', '').lower() else None
	html_encoding = EncodingDetector.find_declared_encoding(resp.content, is_html=True)
	encoding = html_encoding or http_encoding
	return BeautifulSoup(resp.content, from_encoding=encoding, features="html.parser")


def check_url_for_links(url):
	logging.debug("Checking URL %s for new URLs", url)
	return_array = []
	for link in parse_url(url).find_all('a', href=True):
		logging.debug("Found URL: %s", link)
		if link['href'] == '':
			continue
		elif link['href'][0:4] != 'http' and '../' not in link['href']:
			return_array.append(url + '/' + link['href'])
		elif link['href'][0:11] == 'https://cdn':
			return_array.append(link['href'])
	logging.debug("Finished checking of URLs for: %s", url)
	return return_array


def download_url(url, download_location):
	local_filename = url.split('/')[-1]
	r = requests.get(url, stream=True)
	with open(download_location + '/' + local_filename, 'wb') as f:
		response = requests.get(url, stream=True)
		total_length = response.headers.get('content-length')

		if total_length is None:
			f.write(response.content)
		else:
			dl = 0
			total_length = int(total_length)
			for data in response.iter_content(chunk_size=4096):
				dl += len(data)
				f.write(data)
				done = float(100 * dl / total_length)
				print("\r[%s%s] %.2f%% done" % ('=' * int(done/2), ' ' * (50 - int(done/2)), done), end='', flush=True)
			print('')


def main():
	directory = '/media/user/3EB47D32B47CEE31/Collection 2'
	if not os.path.exists(directory):
		os.makedirs(directory)
	files_in_directory = os.listdir(directory)
	url_list = check_url_for_links('https://cdn.databases.today/')
	for url in url_list:
		if url[-1] == '/':
			url_list.remove(url)
			url_list.extend(check_url_for_links(url))
	output = set()
	for x in url_list:
		output.add(x)
	print('found url number: ' + str(len(output)))
	output2 = set()
	for y in output:
		if y.split('/')[-1] not in files_in_directory:
			output2.add(y)
	print('found new url: ' + str(len(output2)))
	counter = 0
	for url in output2:
		counter += 1
		if url[-1] != '/' and url[-3] != 'php':
			print(str(counter) + '/' + str(len(output2)) + ' Downloading ' + url.split('/')[-1])
			download_url(url, directory)


if __name__ == '__main__':
	main()
