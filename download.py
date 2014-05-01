''''
    The download function to go accross all the search terms, login with different users
    and store the result on the disk
'''
import getpass
import os
import sys
import urllib

from pyGoogleTrendsCsvDownloader import pyGoogleTrendsCsvDownloader, QuotaExceededException
from searchTerms import list_of_geo_terms, list_of_periods_of_time, list_of_search_terms


# in case we need more that 1 user to download all the data,
# we keep here all the connexions
google_connexions = []

def mkdirp(directory):
    if not os.path.isdir(directory):
        os.makedirs(directory)

def download():
    pass

def main():
    print 'Starting process'
    number_of_files_to_download = len(list_of_geo_terms) * len(list_of_periods_of_time) * len(list_of_search_terms)
    print 'We are about to download %d csv files' % number_of_files_to_download

    number_of_required_users = number_of_files_to_download/500 + 1
    print 'You will need: %d Google users (1 user = 500 queries)' % number_of_required_users

    for i in range(number_of_required_users):
        login = raw_input("Please enter your email address: ")
        pwd = getpass.getpass("Enter your password: ")
        connexion = pyGoogleTrendsCsvDownloader(login, pwd)
        google_connexions.append(connexion)


    DATA_DIR = 'data'
    mkdirp(DATA_DIR)

    for disease in list_of_search_terms:
        mkdirp(os.path.join(DATA_DIR, disease))

        for timeframe in list_of_periods_of_time:
            time_dir = str(timeframe[2:6])
            mkdirp(os.path.join(DATA_DIR, disease, time_dir))

            for geo in list_of_geo_terms:
                print 'Fetching %s %s %s' % (disease, timeframe, geo)

                data = ''
                while not data:
                    try:
                        connexion = google_connexions[0]
                        data = connexion.get_csv_data(q=disease, geo=geo, date=timeframe)
                    except QuotaExceededException:
                        google_connexions.pop(0)
                    except IndexError:
                        print 'All users have exceeded their quotas'
                        sys.exit(1)

                current_file = open(os.path.join(DATA_DIR, disease, time_dir, '%s.csv' % geo), "wb")
                current_file.write(data)
                current_file.close()




if __name__ == "__main__":
    main()
    print 'Completed without errors.'
