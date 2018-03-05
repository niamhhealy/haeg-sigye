# Import BeautifulSoup library
from bs4 import BeautifulSoup

# Import Regex
import re

# Import URL parser library
import urllib2

# Import Pandas
import pandas as pd

date_last_accessed = '2017-02-01'

# Define ROK NSSC press releases URL
rok_nssc_url = 'http://www.nssc.go.kr/nssc/english/release/list.jsp'

# Save HTML of ROK NSSC press releases
rok_nssc_pr = urllib2.urlopen(rok_nssc_url)

# Save soup of ROK NSSC press releases
soup = BeautifulSoup(rok_nssc_pr, 'html.parser')

# Find first story html
first_story_html = soup.find('td', attrs={'class':'title'}).contents[1]

# Find link to first story
first_story_url = 'http://www.nssc.go.kr/nssc/english/release/list.jsp' + str(first_story_html['href'])

# Define fully updated variable
fully_updated = False

# Create empty pandas dataframe to save data
rok_nssc_pr_df = pd.DataFrame(data = {'Author':[], 'Date':[], 'Title':[], 'URL':[]})

# Set URL as first_story_url
url = first_story_url

def pr_date_cleaner(pr_date_untidy):

    '''This function cleans untidy dates from the ROK NSSC PR webpages.'''

    # Save press release year
    pr_year = pr_date_untidy[-4:]

    # Find location of date
    date_location = re.search("\d",pr_date_untidy).start()

    # Take month
    pr_month = pr_date_untidy[:date_location-1]

    # Create long to short months dictionary
    months_dictionary = {
        'January':'Jan',
        'February':'Feb',
        'Febr':'Feb',
        'March':'Mar',
        'April':'Apr',
        'May':'May',
        'June':'Jun',
        'July':'Jul',
        'August':'Aug',
        'September':'Sep',
        'October':'Oct',
        'November':'Nov',
        'December':'Dec'}

    # Standardize to short month
    for word, initial in months_dictionary.items():
        pr_month = pr_month.replace(word, initial)

    # Create numerical months dictionary
    numerical_months_dictionary = {
        'Jan':'01',
        'Feb':'02',
        'Mar':'03',
        'Apr':'04',
        'May':'05',
        'Jun':'06',
        'Jul':'07',
        'Aug':'08',
        'Sep':'09',
        'Oct':'10',
        'Nov':'11',
        'Dec':'12'}

    # Convert month to number
    for word, initial in numerical_months_dictionary.items():
        pr_month = pr_month.replace(word, initial)

    # Look up day
    if sum(c.isdigit() for c in pr_date_untidy) is 5:
        pr_day = '0' + pr_date_untidy[re.search("\d",pr_date_untidy).start()]
    else:
        pr_day = pr_date_untidy[re.search("\d",pr_date_untidy).start():re.search("\d",pr_date_untidy).start()+2]

    # Save clean press release date
    clean_pr_date = '{}-{}-{}'.format(pr_year,pr_month,pr_day)

    return clean_pr_date

    # create while loop
    
  while fully_updated is False:

      # Save HTML of the press release we're looking at
      pr_html = urllib2.urlopen(url)

      # Collect press release soup
      press_release_soup = BeautifulSoup(pr_html, 'html.parser')

      # Find press release title & date
      pr_title_date = press_release_soup.find('td', attrs={'class':'title ','colspan':'5'}).get_text()

      # Tidy press release title
      pr_title = pr_title_date[pr_title_date.find(']')+2:]

      # Save url
      pr_url = url

      # Find untidy press release date
      pr_date_untidy = pr_title_date[1:pr_title_date.rfind(']')]

      # Save clean pr_date
      pr_date = pr_date_cleaner(pr_date_untidy)

      # Save press release author
      pr_author = 'Republic of Korea Nuclear Safety and Security Commission'

      # Create dictionary for press release
      pr_data = {'Title':pr_title, 'Date':pr_date, 'Author':pr_author, 'URL':url}

      # Create dataframe for press release
      pr_df = pd.DataFrame(data = pr_data, index = [0])

      # Introduce dataframe for press release to existing dataframe
      rok_nssc_pr_df = pd.concat([pr_df,rok_nssc_pr_df])

      # Collect next URL to look-up - the html
      next_url_html = press_release_soup.find('td', attrs={'class':'next_article '}).contents[0]

      # Take url to next story
      url = 'http://www.nssc.go.kr/nssc/english/release/list.jsp' + str(next_url_html['href'])

      # Re-examine fully_updated
      fully_updated = rok_nssc_pr_df['Date'].min() < date_last_accessed
