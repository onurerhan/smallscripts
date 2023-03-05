from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector
import requests
import re
import logging
import argparse

not_visited_urls = []
visited_urls = []
mail_list = []


def parse_url(url):
    logging.debug('Getting URL: %s', url)
    request = requests.Session()
    request.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'
    resp = request.get(url)
    http_encoding = resp.encoding if 'charset' in resp.headers.get('content-type', '').lower() else None
    html_encoding = EncodingDetector.find_declared_encoding(resp.content, is_html=True)
    encoding = html_encoding or http_encoding
    return BeautifulSoup(resp.content, from_encoding=encoding, features="html.parser")


def check_for_mail(string, url):
    global mail_list
    result = re.findall(r'[\w.-]+@[\w.-]+\.\w+', string)
    for mail in result:
        logging.debug('Found mail: %s in URL: %s', mail, url)
        if mail not in mail_list:
            logging.debug("Added mail: %s in URL: %s", mail, url)
            mail_list.append(mail)


def check_url_for_links(website, url, site_only=False):
    logging.debug("Checking URL %s for new URLs", url)
    return_array = []
    for link in website.find_all('a', href=True):
        logging.debug("Found URL: %s", link)
        if link['href'] == '':
            continue
        elif link['href'][0] == '/':
            return_array.append(url + link['href'])
        elif link['href'][0:4] == 'http' and not site_only:
            return_array.append(url)
    logging.debug("Finished checking of URLs for: %s", url)
    return return_array


def get_url(url, max_depth=0, depth=0, site_only=False):
    global visited_urls
    if depth <= max_depth and url not in visited_urls:
        logging.info('Scanning URL: %s', url)
        visited_urls.append(url)
        parsed_url = parse_url(url)
        check_for_mail(str(parsed_url), url)
        if depth < max_depth:
            for link in check_url_for_links(parsed_url, url=url, site_only=site_only):
                get_url(link, max_depth, depth + 1, site_only=site_only)


def write_output_to_file(outputfile):
    with open(outputfile, 'a') as file:
        logging.debug("Opened file %s", outputfile)
        for mail in mail_list:
            file.write("" + mail + "\n")


def print_output_to_console():
    for mail in mail_list:
        logging.debug("Written %s to console", mail)
        print(mail)


def load_input_from_file(inputfile):
    global not_visited_urls
    with open(inputfile) as f:
        not_visited_urls.append(f.read().splitlines())


def main(recursion_depth=0, site_only=False):
    for link in not_visited_urls:
        get_url(link, max_depth=recursion_depth, site_only=site_only)
        write_output_to_file("GetMailAddr/output.txt")
    print_output_to_console()


if __name__ == "__main__":
    logging.basicConfig(filename='GetMailAddr/MailList.log', level=logging.INFO)
    parser = argparse.ArgumentParser()

    parser.add_argument("square", type=int,
                        help="display a square of a given number")
    not_visited_urls.append("https://forum.donanimhaber.com/")
    main(recursion_depth=10)

# TODO multithreading
# TODO add command line arguments
    # verbose
    # print to console
    # log level
    # url
    # input file
    # output file
    # thread count
    # site only crawling
    # help page
# TODO error handling
