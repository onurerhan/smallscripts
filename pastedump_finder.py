import re
import json
import requests
import datetime


def date_to_timestamp(string):
    return int(datetime.datetime.strptime(string, "%d/%m/%Y").timestamp())


def get_dump(query):
    url = "https://psbdmp.ws/api/dump/get/"
    response = requests.get(url + query)
    return response.json()


def get_dump_time_interval(from_date, to_date):
    url = "https://psbdmp.ws/api/dump/get/timeval/"
    response = requests.get(url + str(from_date) + '/' + str(to_date))
    return response.json()


def get_daily_dumps():
    url = "https://psbdmp.ws/api/dump/daily"
    response = requests.get(url)
    return response.json()


def general_search(query):
    url = "https://psbdmp.ws/api/search/"
    response = requests.get(url + query)
    return response.json()


def search_by_email(query):
    url = "https://psbdmp.ws/api/search/email/"
    response = requests.get(url + query)
    return response.json()


def search_by_domain(query):
    url = "https://psbdmp.ws/api/search/domain/"
    response = requests.get(url + query)
    return response.json()


def check_mail_line(string):
    result = re.findall(r'[\w.-]+@[\w.-]+\.\w+', string)
    if len(result) == 1:
        return True
    return False


def strip_line_for_mail_pass(string):
    line = string.replace(' ', '').replace('|', ':').replace(',', ':').split(':')
    if len(line) == 2 and check_mail_line(line[0]):
        line[1] = line[1][:-1]  # delete \r from end of string
        return line[0:2]


def get_todays_mails():
    daily_dump = get_daily_dumps()
    print(daily_dump)
    for pasta in daily_dump['data']:
        paste_data = get_dump(pasta['id'])
        for line in paste_data['data'].split('\n'):
            mail_pass = strip_line_for_mail_pass(line)
            if mail_pass is not None:
                print(mail_pass)


def get_mail_domain(query):
    with open("ProjectPastaBin/output.csv", "w") as output_file:
        output_file.write('username,password\n')
        search_data = general_search(query)
        for x in search_data['data']:
            paste_data = get_dump(x['id'])
            for line in paste_data['data'].split('\n'):
                if query in line:
                    mail_pass = strip_line_for_mail_pass(line)
                    if mail_pass is not None:
                        print(mail_pass)


def main(query):
    with open(query + '.json', 'w') as output:
        json.dump(get_dump(query), output)


if __name__ == "__main__":
    main('qgKUK3Wm')

