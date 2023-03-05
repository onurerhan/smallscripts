import requests
import csv


user_mail = "goxtju+c5m9lluz1ggqg@sharklasers.com"
user_password = "password1"
host_search_facets = "app,device,service,os,ip,port,country,city"
web_search_facets = "webapp,component,framework,frontend,server,waf,os,country,city"
max_pages = 2


class ZoomEye(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.access_token = "JWT "
        self.r = None

    def requestisok(self):
        if self.r.status_code == requests.codes.ok:
            return True
        else:
            return False

    def error(self):
        json = self.r.json()
        return "Error:" + str(self.r.status_code) + "\t" + json['error'] + "\n" + json['message'] + "\n" + json['url'] + "\n"

    def payload(self, query, page, facets):
        return {'query': query, 'page': page, 'facets': facets}

    def login(self):
        self.r = requests.post('https://api.zoomeye.org/user/login',
                               json={"username": self.username, "password": self.password})
        if self.requestisok():
            self.access_token += self.r.json()['access_token']
            return True
        else:
            return False

    def resourcesinfo(self):
        headers = {'Authorization': self.access_token}
        self.r = requests.get('https://api.zoomeye.org/resources-info', headers=headers)
        return self.requestisok()

    def hostsearch(self, query, page=1, facets=host_search_facets):
        headers = {'Authorization': self.access_token}
        payload = self.payload(query, page, facets)
        self.r = requests.get("https://api.zoomeye.org/host/search", headers=headers, params=payload)
        return self.requestisok()

    def websearch(self, query, page=1, facets=web_search_facets):
        headers = {'Authorization': self.access_token}
        payload = self.payload(query, page, facets)
        self.r = requests.get("https://api.zoomeye.org/web/search", headers=headers, params=payload)
        return self.requestisok()

    def response(self):
        return self.r.json()


def check_api(obj):
    if obj.resourcesinfo():
        print("resouresinfo:")
        print(obj.response())
    else:
        print(obj.error())


def search_keyword_in_host(obj, keyword, csv_file, page=1):
    if obj.hostsearch(keyword, page):
        response = obj.response()
        for result in response['matches']:
            ip = result['ip']
            port = result['portinfo']['port']
            extrainfo = result['portinfo']['extrainfo']
            service = result['portinfo']['service']
            hostname = result['portinfo']['hostname']
            version = result['portinfo']['version']
            device = result['portinfo']['device']
            os = result['portinfo']['os']
            banner = result['portinfo']['banner']
            app = result['portinfo']['app']
            country = result['geoinfo']['country']['names']['en']
            latitude = result['geoinfo']['location']['lat']
            longtitude = result['geoinfo']['location']['lon']
            isp = result['geoinfo']['isp']
            organization = result['geoinfo']['organization']
            aso = result['geoinfo']['aso']
            asn = result['geoinfo']['asn']
            csv_file.writerow([ip, port, extrainfo, service, hostname, version, device, os, app, country,
                               latitude, longtitude, isp, organization, aso, asn])
    else:
        print(obj.error())
        return 'Error'


def main(query='app:"nginx" +os:"linux" + port:5001'):
    with open('output.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',')
        header = "ip,port,extrainfo,service,hostname,version,device,os,app,country,latitude,longtitude,isp,organization,aso,asn"
        print(header)
        zoomeye = ZoomEye(user_mail, user_password)
        if zoomeye.login():
            check_api(zoomeye)

            for page_number in range(1, max_pages):
                if search_keyword_in_host(zoomeye, query, csv_writer, page_number) == 'Error':
                    return 0
        else:
            print(zoomeye.error())


if __name__ == '__main__':
    main()
