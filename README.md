### Python3 port.

I've ported it to python3 and structured it as package. Now it can be installed by
```
python3 setup.py install
```

Now it fails if authentication was unsuccessful with `AuthFailedException`

## Google Trend Csv Downloader

## How to use

#### Download csv files:


A downloader for Google trends that downloads CSV data. It provides authentication to Google services.

The script will assess how many queries will be run and ask for a number of login/password since Google restricts the search quotas to 500 queries/person/day

Go to `bin` directory.

Edit `searchTerms.py` and list the queries you are interested in.

run `python download.py`

Enter your Google credentials when asked for it.

#### Using as package example

```
from googletrendscsvdownloader.pyGoogleTrendsCsvDownloader import pyGoogleTrendsCsvDownloader

# connect with proxy
# ignore last parameter if you don't need to use proxy
trendsDownloader = pyGoogleTrendsCsvDownloader("username", "password", "http://proxyuser:proxypass@proxyhost:port")

data = trendsDownloader.get_csv_data(q="python", cat="0-5-31")
```

-----
## Fork

A fork from simonavril/google-trends-csv-downloader

which is fork from pedrofaustino/google-trends-csv-downloader.

