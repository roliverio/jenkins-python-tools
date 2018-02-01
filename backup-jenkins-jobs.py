#!/usr/bin/python
import logging
import requests
import sys
import argparse


def get_jobs(SERVER,GROUP):
  url = 'http://%s/view/%s/api/json?pretty=true' % (SERVER,GROUP)
  response = requests.get(url, auth=(USER, API_TOKEN), stream=True)
  data = response.json()
  return data['jobs']

def backup_job(name, url):
  url = url + 'config.xml'
  response = requests.get(url, auth=(USER, API_TOKEN), stream=True)
  if not response.ok:
    print 'error %d getting job config: %s' % (response.status_code, url)
  else:
    print name
    with open(name + '.xml', 'w') as output:
      for block in response.iter_content(2048):
        output.write(block)



if __name__ == "__main__":
        parser = argparse.ArgumentParser(description='Backup Jenkins Jobs')
        parser.add_argument('-s', '--server', dest='SERVER', help='Jenkins Server host')
        parser.add_argument('-j', '--jobfilter', dest='JOB_FILTER', help='An string to determine wich jobs to retrieve config from')
        parser.add_argument('-t', '--token', dest='API_TOKEN', help='Your Jenkins API Token, or Password')
        parser.add_argument('-u', '--username', dest='USER', help='User to login as')
        parser.add_argument('-g', '--group', dest='GROUP', help='Group of Jenkins Jobs to search from')
        parser.add_argument('-d', '--debug', dest='DEBUG', help='Should Debug be enabled (1 = Yes, 2 = No)')
        args = parser.parse_args()

        if args.SERVER == None:
                SERVER = raw_input('Insert Jenkins Server:')
        else:
                SERVER = args.SERVER

        if args.JOB_FILTER == None:
                JOB_FILTER = raw_input('String to determine specific job(s) to retrieve config from:')
        else:
                JOB_FILTER = args.JOB_FILTER

        if args.API_TOKEN == None:
                API_TOKEN = raw_input('Insert your Jenkins API Token, or Password: ')
        else:
                API_TOKEN = args.API_TOKEN

        if args.USER == None:
                USER = raw_input('Insert user to login as: ')
        else:
                USER = arg.USER

        if args.GROUP == None:
                GROUP = raw_input('Group of Jenkins jobs to search from: ')
        else:
                GROUP = args.GROUP

        if args.DEBUG == None:
                DEBUG = 2
        else:
                logging.captureWarnings(True)

        jobs = get_jobs(SERVER = SERVER,GROUP = GROUP)
        for j in jobs:
             if j['name'].startswith(JOB_FILTER):
              backup_job(j['name'], j['url'])
             else:
              sys.exit(0)

