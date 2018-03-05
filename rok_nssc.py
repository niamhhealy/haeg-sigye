# Import BeautifulSoup library
from bs4 import BeautifulSoup

# Import URL parser library
import urllib2

# Import Pandas
import pandas as pd

date_last_accessed = '2017-02-01'

# Define motie headlines function
def motie_headlines(motie_photo_news_url):

    ''' This function takes the url of the MOTIE photo news page and returns a
    Pandas dataframe containing the urls of the stories on the
    page.'''

    # Save HTML of MOTIE URL
    motie_photo_news = urllib2.urlopen(motie_photo_news_url)

    # Create empty list of headlines_code
    list_of_headlines = []

    # Save soup of MOTIE photo news page
    soup = BeautifulSoup(motie_photo_news, 'html.parser')

    # Get links
    links = soup.find_all('a', attrs={'title':'Detail View'})

    # Create empty list of empty list_of_links
    list_of_links = []

    # Save each link in list_of_links
    for link in links:

        list_of_links.append(str('http://english.motie.go.kr/en/pc/photonews/bbs/'+link['href']))

    # Create dictionary of headlines and links
    dictionary = {'URL':list_of_links}

    # Create empty dataframe
    headlines_urls = pd.DataFrame(data = dictionary)

    return headlines_urls

# Define motie photo news story
def motie_photo_news_story(story_url):

    ''' This function takes a URL of a page from the MOTIE photo news section
    and returns a dataframe containing key information about that story.'''

    # Save HTML of MOTIE story
    MOTIE_photo_story = urllib2.urlopen(story_url)

    # Save soup of MOTIE story
    soup = BeautifulSoup(MOTIE_photo_story, 'html.parser')

    # Save story headline
    story_headline = soup.find('h3').get_text()

    # Save story date
    story_date = list(soup.find('h3').children)[1].get_text()

    # Save story author
    story_author = 'Republic of Korea Ministry of Trade, Industry and Energy'

    # Save language
    story_language = 'English'

    # Create dictionary for story
    story_dictionary = {'Headline':story_headline, 'Date':story_date, 'Language': story_language, 'Author':story_author, 'URL':story_url}

    # Create dataframe for story
    story_dataframe = pd.DataFrame(data = story_dictionary, index = [0])

    return story_dataframe

# Define MOTIE photo news URL
motie_photo_news_url = 'http://english.motie.go.kr/en/pc/photonews/bbs/bbsList.do?bbs_cd_n=1'

# Run MOTIE headlines function on URL + save as new dataframe
motie_photo_news = motie_headlines(motie_photo_news_url)

# Create list of URLs to find more info on
story_URLs = motie_photo_news['URL'].tolist()

# Create empty dataframe to contain further information
stories = pd.DataFrame(data = None)

# Create stories dataframe containing more information for each headline page
for url in story_URLs:
    story_dataframe = motie_photo_news_story(url)
    stories = pd.concat([stories, story_dataframe])

# Tidy up stories dataframe
stories = stories.reset_index().drop(labels = 'index', axis = 1)

# Merge headlines dataframe with stories dataframe
motie_photo_news = pd.merge(stories, motie_photo_news, left_on='URL', right_on='URL')

# Create variable that if true if motie news story table fully updated
fully_updated = date_last_accessed > motie_photo_news['Date'].min()

# Save news story with oldest URL as string
last_url = story_URLs[-1]

# Take news story number from oldest URL
last_story_number = (story_URLs[-1])[68:71]

# create while loop to run if table not fully updated from newest 8 stories
while fully_updated is False:

    # save next news story number
    last_story_number = int(last_story_number) - 1

    # save url for next news story
    next_story_url = "http://english.motie.go.kr/en/pc/photonews/bbs/bbsList.do?bbs_seq_n={}&bbs_cd_n=1&currentPage=1&search_key_n=&search_val_v=&cate_n=".format(last_story_number)

    # run motie_photo_news_Story on next news story
    next_story_df = motie_photo_news_story(next_story_url)

    # add next news story to motie_photo_news
    motie_photo_news = pd.concat([motie_photo_news,next_story_df])

    # check whether table fully updated yet
    fully_updated = date_last_accessed > motie_photo_news['Date'].min()
