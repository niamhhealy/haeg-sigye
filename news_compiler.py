# Import BeautifulSoup library
from bs4 import BeautifulSoup

# Import URL parser library
import urllib2

# Import Pandas
import pandas as pd

# Amend pandas settings
pd.set_option("display.max_colwidth",1000)

# Import Regex
import re

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
    story_headline = (soup.find('h3').get_text())[:-11]

    # Save story date
    story_date = list(soup.find('h3').children)[1].get_text()

    # Save story author
    story_author = 'Republic of Korea Ministry of Trade, Industry and Energy'

    # Save language
    story_language = 'English'

    # Create dictionary for story
    story_dictionary = {'Story title':story_headline, 'Date':story_date, 'Language': story_language, 'Author':story_author, 'URL':story_url}

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

def produce_ROK_NSSC_PR_df(date_last_accessed):

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
    rok_nssc_pr_df = pd.DataFrame(data = {'Author':[], 'Date':[], 'Story title':[], 'URL':[]})

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
        pr_title = pr_title_date[len(pr_title_date[1:pr_title_date.rfind(']')])+3:]

        # Save url
        pr_url = url

        # Find untidy press release date
        pr_date_untidy = pr_title_date[1:pr_title_date.rfind(']')]

        # Save clean pr_date
        pr_date = pr_date_cleaner(pr_date_untidy)

        # Save press release author
        pr_author = 'Republic of Korea Nuclear Safety and Security Commission'

        # Save language
        story_language = 'English'

        # Create dictionary for press release
        pr_data = {'Story title':pr_title, 'Date':pr_date, 'Author':pr_author, 'URL':url, 'Language':story_language}

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

    return rok_nssc_pr_df

def news_df_producer(date):

    '''This function produces an amalgamated news dataframe.'''

    # Produce NSSC PR df
    ROK_NSSC_PR_df = produce_ROK_NSSC_PR_df(date)

    # Produce MOTIE photo news DF
    motie_photo_df = produce_motie_df(date)

    # Concatenate DFs
    news_df = pd.concat([ROK_NSSC_PR_df,motie_photo_df])

    # Reset index
    news_df.reset_index(inplace = True)

    # Drop old index column
    news_df.drop(columns='index',inplace=True)

    return news_df
