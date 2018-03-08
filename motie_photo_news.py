# Import BeautifulSoup library
from bs4 import BeautifulSoup

# Import URL parser library
import urllib2

# Import Pandas
import pandas as pd

# Define first motie_photo_news_story function
def first_motie_photo_news_story(motie_photo_news_url):

    ''' This function takes the url of the MOTIE photo news page and returns the URL of the most
    recent photo news piece.'''

    # Save HTML of MOTIE URL
    motie_photo_news = urllib2.urlopen(motie_photo_news_url)

    # Create empty list of headlines_code
    list_of_headlines = []

    # Save soup of MOTIE photo news page
    soup = BeautifulSoup(motie_photo_news, 'html.parser')

    # Get first link
    link = soup.find('a', attrs={'title':'Detail View'})

    # Create empty list of empty list_of_links
    url = str('http://english.motie.go.kr/en/pc/photonews/bbs/'+link['href'])

    return url

# Define motie_photo_news_story function
def motie_photo_news_story(story_url):

    '''# This function takes a URL of a page from the MOTIE photo news section
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

# Define produce_motie_df function
def produce_motie_df(date_last_accessed):

    ''' This function takes the'''

    # Define MOTIE photo news URL
    motie_photo_news_url = 'http://english.motie.go.kr/en/pc/photonews/bbs/bbsList.do?bbs_cd_n=1'

    # Run first_motie_photo_news_story + save first story url as string
    first_story_url = first_motie_photo_news_story(motie_photo_news_url)

    # Run motie_photo_news_story on first url
    motie_photo_news = motie_photo_news_story(first_story_url)

    # Create variable that if true if motie news story table fully updated
    fully_updated = date_last_accessed > motie_photo_news['Date'].min()

    # Take news story number from first story
    last_story_number = first_story_url[68:71]

    # create while loop to run if table not fully updated from newest 8 stories
    while fully_updated is False:

        # save next news story number
        last_story_number = int(last_story_number) - 1

        # save url for next news story
        next_story_url = "http://english.motie.go.kr/en/pc/photonews/bbs/bbsList.do?bbs_seq_n={}&bbs_cd_n=1&currentPage=1&search_key_n=&search_val_v=&cate_n=".format(last_story_number)

        # run motie_photo_news_Story on next news story
        next_story_df = motie_photo_news_story(next_story_url)

        #  add next news story to motie_photo_news
        motie_photo_news = pd.concat([motie_photo_news,next_story_df])

        # check whether table fully updated yet
        fully_updated = date_last_accessed > motie_photo_news['Date'].min()

    return motie_photo_news
