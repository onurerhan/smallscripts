#!/usr/bin/env python3
# https://github.com/UnaPibaGeek/ctfr
import re
import json
import requests


def clear_url(target):
    return re.sub('.*www\.', '', target, 1).split('/')[0].strip()


def save_subdomains(subdomain, output_file):
    with open(output_file, "a") as f:
        f.write(subdomain + '\n')
        f.close()


# Get data from certificate transparency logs - Only works for https
def get_crt_data(url, subs):
    req = requests.get("https://crt.sh/?q=%.{d}&output=json".format(d=url))

    if req.status_code != 200:
        print("Information not available, skipping")
        return subs

    json_data = json.loads('[{}]'.format(req.text.replace('}{', '},{')))

    for (key, value) in enumerate(json_data):
        if value['name_value'] not in subs:
            subs.append(value['name_value'])
    result = sorted(set(subs))
    return result


def main():
    subdomains = []
    target = clear_url("reddit.com")
    output = None
    subdomains = get_crt_data(target, subdomains)

    for subdomain in subdomains:
        print("{s}".format(s=subdomain))
        if output is not None:
            save_subdomains(subdomain, output)


if __name__ == '__main__':
    main()
