# Import BeautifulSoup library
from bs4 import BeautifulSoup

# Import URL parser library
import urllib.request as urllib

# Import Pandas
import pandas as pd

# Import date time
from datetime import datetime

# Amend pandas settings
pd.set_option("display.max_colwidth",1000)

# Import Regex
import re

# Define Cheong Wa Dae briefings function
def cheong_wa_dae_speeches(date_last_accessed):
    ''' This function takes the date the user last accessed the news and returns a df containing the latest
    speeches from the Cheong Wa Dae after that date.'''

    # Set url of speeches page
    cwds_url = 'https://english1.president.go.kr/BriefingSpeeches/Speeches'

    # Create table_fully_updated variable
    table_fully_updated = False

    # Save HTML of CWD-B
    cwdb_pr = urllib.urlopen(cwds_url)

    # Save soup of CWD-S story
    soup = BeautifulSoup(cwdb_pr, 'html.parser')

    # Find first news story_url
    link_junk = str(soup.find('div', attrs={'class':'sub_board_title'}).contents[1])
    start_of_link =  link_junk.find('"')+1
    end_of_link =  link_junk.find('"',start_of_link)
    first_story = 'https://english1.president.go.kr' + link_junk[start_of_link:end_of_link]

    # Set url as first story link
    url = first_story

    # Create empty news df
    df = pd.DataFrame(data=None)

    while table_fully_updated is False:

        # Save HTML of CWD-S
        news_story = urllib.urlopen(url)

        # Save soup of CWD-S
        cwdb_soup = BeautifulSoup(news_story, 'html.parser')

        # Find title
        title = cwdb_soup.find('title').contents[0]

        # Find date
        date = cwdb_soup.find('div',attrs={'class':'view_date_sns'}).p.string
        date = datetime.strptime(date,'%B %d, %Y')
        print('Running CWD SPEECHES '+str(date))

        # Create dictionary for story
        story_dictionary = {'Story title':title, 'Date':date, 'Language': 'English', 'Author':'Republic of Korea  Cheong Wa Dae', 'URL':url}

        # Create dataframe for story
        story_dataframe = pd.DataFrame(data = story_dictionary, index = [0])

        # Concat
        df = pd.concat([df,story_dataframe])

        # Set next url as url
        story_number = int(url[-2:])
        story_number = story_number - 1
        url = url[:-3] + str(story_number)

        # Check if table fully updated
        table_fully_updated = date_last_accessed > df['Date'].min()

    return df

import time
from datetime import date
date = 'June 1, 2018'
date_last_accessed = datetime.strptime(date,'%B %d, %Y')
df = cheong_wa_dae_speeches(date_last_accessed)
print (df)
