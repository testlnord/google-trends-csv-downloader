''''
    A script that goes through 3 list of search queries and downloads CSV files from
    Google Trends.

    The structure of the directories created will be
    data/
      - search (what)/
           - timeframe (when)/
               - geo.csv (where)
'''

import getpass
import os
import sys
import urllib

from pyGoogleTrendsCsvDownloader import pyGoogleTrendsCsvDownloader, QuotaExceededException
from searchTerms import list_of_geo_terms, list_of_periods_of_time, list_of_search_terms

# where the CSV will be downloaded too
DATA_DIR = 'data'


def mkdirp(directory):
    if not os.path.isdir(directory):
        os.makedirs(directory)

def login():
    login = raw_input("Please enter your email address: ")
    pwd = getpass.getpass("Enter your password: ")
    return  pyGoogleTrendsCsvDownloader(login, pwd)

def main():
    print 'Starting process'
    number_of_files_to_download = len(list_of_geo_terms) * len(list_of_periods_of_time) * len(list_of_search_terms)
    print 'We are about to download %d csv files' % number_of_files_to_download

    number_of_required_users = number_of_files_to_download/500 + 1
    print 'You are going to need: %d Google users (1 user = 500 queries)' % number_of_required_users

    connexion = login()

    mkdirp(DATA_DIR)

    for disease in list_of_search_terms:
        mkdirp(os.path.join(DATA_DIR, disease))
        print 'Fetching [%s]...' % disease

        for timeframe in list_of_periods_of_time:
            time_dir = str(timeframe[2:6])
            mkdirp(os.path.join(DATA_DIR, disease, time_dir))

            for geo in list_of_geo_terms:
                data = ''
                while not data:
                    try:
                        data = connexion.get_csv_data(q=disease, geo=geo, date=timeframe)
                    except QuotaExceededException:
                        print 'User %s has exceeded quotas. Please login with a new user...'
                        connexion = login()

                current_file = open(os.path.join(DATA_DIR, disease, time_dir, '%s.csv' % geo), "wb")
                current_file.write(data)
                current_file.close()

        print 'Finished downloading [%s].' % disease


if __name__ == "__main__":
    main()
    print 'Completed without errors.'
