# Import BeautifulSoup library
from bs4 import BeautifulSoup

# Import URL parser library
import urllib2

# Import Pandas
import pandas as pd

def motie_headlines(motie_photo_news_url):

    ''' This function takes the url of the MOTIE photo news page and returns a
    Pandas dataframe containing the headlines and urls of the stories on the
    page.'''

    # Save HTML of MOTIE URL
    motie_photo_news = urllib2.urlopen(motie_photo_news_url)

    # Create empty list of headlines_code
    list_of_headlines = []

    # Save soup of MOTIE photo news page
    soup = BeautifulSoup(motie_photo_news, 'html.parser')

    # Save headlines of MOTIE photo news page
    headlines_code = soup.find_all('span', attrs={'class':'tit'})

    # Save each headline from MOTIE soup as item in list_of_headlines
    for headline in headlines_code:

        list_of_headlines.append(str(headline.get_text()))

    # Get links
    links = soup.find_all('a', attrs={'title':'Detail View'})

    # Create empty list of empty list_of_links
    list_of_links = []

    # Save each link in list_of_links
    for link in links:

        list_of_links.append(str('http://english.motie.go.kr/en/pc/photonews/'+link['href']))

    # Create dictionary of headlines and links
    dictionary = {'Story title':list_of_headlines, 'URL':list_of_links}

    # Create empty dataframe
    headlines_urls = pd.DataFrame(data = dictionary)

    return headlines_urls

def motie_photo_news_story(story_url):

    # Save HTML of MOTIE story
    MOTIE_photo_story = urllib2.urlopen(story_url)

    # Save soup of MOTIE story
    soup = BeautifulSoup(MOTIE_photo_story, 'html.parser')

    # Save story headline
    story_headline = str(soup.find('h3').get_text())

    # Save story date
    story_date = str(soup.find('span', attrs={'class':'date'}).get_text())

    # Save story author
    story_author = 'Republic of Korea Ministry of Trade, Industry and Energy'

    # Create dictionary for story
    story_dictionary = {'Headline':story_headline, 'Date':story_date, 'Author':story_author, 'URL':story_url}

    # Create dataframe for story
    story_dataframe = pd.DataFrame(data = story_dictionary, index = [0])

    print story_dataframe

motie_photo_news_story('http://english.motie.go.kr/en/pc/photonews/bbs/bbsList.do?bbs_seq_n=671&bbs_cd_n=1&currentPage=1&search_key_n=&search_val_v=&cate_n=')
