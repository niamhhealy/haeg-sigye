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

# Define first motie_photo_news_story function
def first_motie_photo_news_story(motie_photo_news_url):

    ''' This function takes the url of the MOTIE photo news page and returns the URL of the most
    recent photo news piece.'''

    # Save HTML of MOTIE URL
    motie_photo_news = urllib.urlopen(motie_photo_news_url)

    # Save soup of MOTIE photo news page
    soup = BeautifulSoup(motie_photo_news, 'html.parser')

    # Get first link
    link = soup.find('a', attrs={'title':'Detail View'})

    # Create empty list of empty list_of_links
    url = str('http://english.motie.go.kr/en/pc/photonews/bbs/'+link['href'])

    return url

# Define motie_photo_news_story function
def motie_photo_news_story(story_url):

    ''' This function takes a URL of a page from the MOTIE photo news section
    and returns a dataframe containing key information about that story.'''

    # Save HTML of MOTIE story
    MOTIE_photo_story = urllib.urlopen(story_url)

    # Save soup of MOTIE story
    soup = BeautifulSoup(MOTIE_photo_story, 'html.parser')

    # Save story headline
    story_headline = (soup.find('h3').get_text())[:-11]

    # Save story date
    story_date = list(soup.find('h3').children)[1].get_text()

    # Save story date as datetime
    story_date = datetime.strptime(story_date,'%Y-%m-%d')

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

    ''' This function takes the date the user last accessed the news and returns a dataframe containing
    all the MOTIE photo news stories since that date. '''

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

# Define NSSCR PR df function
def produce_ROK_NSSC_PR_df(date_last_accessed):

    ''' This function takes the date the user last accessed the news and returns a dataframe
    containing all the stories since this date. '''

    # Define ROK NSSC press releases URL
    rok_nssc_url = 'http://www.nssc.go.kr/nssc/english/release/list.jsp'

    # Save HTML of ROK NSSC press releases
    rok_nssc_pr = urllib.urlopen(rok_nssc_url)

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
            'Aor':'04',
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
        pr_date = '{}-{}-{}'.format(pr_year,pr_month,pr_day)

        # Save pr date as date time object
        clean_pr_date = datetime.strptime(pr_date,'%Y-%m-%d')

        return clean_pr_date

    # create while loop
    while fully_updated is False:

        # Save HTML of the press release we're looking at
        pr_html = urllib.urlopen(url)

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

# Define first_MOTIE_pr function
def first_MOTIE_pr(motie_pr_url):

    ''' This function takes the URL of the MOTIE PRs and returns the URL of the most recent
    PR. '''

    # Save HTML of MOTIE URL
    motie_photo_news = urllib.urlopen(motie_pr_url)

    # Save soup of MOTIE photo news page
    soup = BeautifulSoup(motie_photo_news, 'html.parser')

    # Get first link
    link = soup.find('dd',attrs={'class':"w100"}).contents[1].contents[0]

    # Create empty list of empty list_of_links
    url = str('http://english.motie.go.kr/en/pc/pressreleases/bbs/'+link['href'])

    return url

# Define MOTIE PR
def motie_pr(pr_url):

    ''' This function takes the URL of a MOTIE PR and returns key information about that PR.'''

    # Save HTML of MOTIE story
    MOTIE_pr = urllib.urlopen(pr_url)

    # Save soup of MOTIE story
    soup = BeautifulSoup(MOTIE_pr, 'html.parser')

    # Save story headline
    story_headline = (soup.find_all('dt'))[5].contents[0]

    # Save story date
    story_date = (soup.find_all('dt'))[5].contents[1].get_text()

    # Save story date as date time object
    story_date = datetime.strptime(story_date,'%Y-%m-%d')

    # Save story author
    story_author = 'Republic of Korea Ministry of Trade, Industry and Energy'

    # Save language
    story_language = 'English'

    # Create dictionary for story
    story_dictionary = {'Story title':story_headline, 'Date':story_date, 'Language': story_language, 'Author':story_author, 'URL':pr_url}

    # Create dataframe for story
    story_dataframe = pd.DataFrame(data = story_dictionary, index = [0])

    return story_dataframe

# Def MOTIE pr function
def motie_pr_df(date_last_accessed):

    ''' This function takes the date the user last accessed the news and returns a dataframe containing
    all the MOTIE pr since that date. '''

    # Define MOTIE photo news URL
    motie_pr_url = 'http://english.motie.go.kr/en/pc/pressreleases/bbs/bbsList.do?bbs_cd_n=2'

    # Run first_MOTIE_pr + save first story url as string
    first_story_url = first_MOTIE_pr(motie_pr_url)

    # Run motie_photo_news_story on first url
    motie_pr_data = motie_pr(first_story_url)

    # Create variable that if true if motie news story table fully updated
    fully_updated = date_last_accessed > motie_pr_data['Date'].min()

    # Take news story number from first story
    last_story_number = first_story_url[72:75]

    # define problematic story number
    problematic_story_number = 622

    # create while loop to run if table not fully updated from newest stories
    while fully_updated is False or last_story_number >= 622:

        # save next news story number
        last_story_number = int(last_story_number) - 1

        # save url for next news story
        next_story_url = "http://english.motie.go.kr/en/pc/pressreleases/bbs/bbsView.do?bbs_seq_n={}&bbs_cd_n=2&currentPage=1&search_key_n=&search_val_v=&cate_n=".format(last_story_number)

        # run motie_pr on next news story
        next_story_df = motie_pr(next_story_url)

        #  add next news story to motie_photo_news
        motie_pr_data = pd.concat([motie_pr_data,next_story_df])

        # check whether table fully updated yet
        fully_updated = date_last_accessed > motie_pr_data['Date'].min()

    return motie_pr_data

# Define MFA news story function
def rok_mfa(date_last_accessed):

    ''' This function takes the date the user last accessed the news and returns a dataframe containing
    all the MFA pr since that date. '''

    # Define URL of MFA
    mfa_url = 'http://www.mofa.go.kr/eng/brd/m_5676/list.do'

    # Create table_fully_updated variable
    table_fully_updated = False

    # Save HTML of MFA
    mfa_pr = urllib.urlopen(mfa_url)

    # Save soup of MFA story
    soup = BeautifulSoup(mfa_pr, 'html.parser')

    # Find first news story_url
    end_of_link =  soup.find('td', attrs={'class':'tal'}).contents[0]['href']
    first_news_story_url  = 'http://www.mofa.go.kr/eng/brd/m_5676' + end_of_link[1:]

    # Set url as first_news_story_url
    url = first_news_story_url

    # Create empty news df
    df = pd.DataFrame(data=None)

    # Create while loop
    while table_fully_updated is False:

            # Save HTML of MFA
            news_story = urllib.urlopen(url)

            # Save soup of MFA story
            mfa_soup = BeautifulSoup(news_story, 'html.parser')

            # Find title of news story
            title = mfa_soup.find('title').contents[0]
            end_of_title = title.find('View|')-1
            title = title[:end_of_title]

            # Find date of news story
            string_date =  (mfa_soup.find('em').contents[0])[1:11]

            # Save story date as date time
            date = datetime.strptime(string_date,'%Y-%m-%d')

            # Set author variable
            author = 'Republic of Korea Ministry of Foreign Affairs'

            # Set language variable
            language = 'English'

            # Create dictionary with story info
            story_data = {'Story title':title, 'Date':date, 'Author':author, 'URL':url, 'Language':language}

            # Create df with story data
            story_df = pd.DataFrame(data = story_data, index=[0])

            # Concat DFs
            df = pd.concat([df,story_df])

            # Find new URL link
            new_url = mfa_soup.find_all('td', attrs={'class':'bro_link'})[1]
            new_url = str(new_url.contents[0])
            start_of_url = new_url.find( '"' )
            end_of_url = new_url.find('"', start_of_url+1)
            new_url = new_url[start_of_url+2:end_of_url]
            new_url = 'http://www.mofa.go.kr/eng/brd/m_5676' + new_url

            # Set url as new_url
            url = new_url

            # Check if df fully updated
            table_fully_updated = date_last_accessed > df['Date'].min()

    return df

# Define Cheong Wa Dae briefings function
def cheong_wa_dae_briefings(date_last_accessed):
    ''' This function takes the date the user last accessed the news and returns a df containing the latest
    briefings from the Cheong Wa Dae after that date.'''

    # Set url of briefings page
    cwdb_url = 'https://english1.president.go.kr/BriefingSpeeches/Briefings'

    # Create table_fully_updated variable
    table_fully_updated = False

    # Save HTML of CWD-B
    cwdb_pr = urllib.urlopen(cwdb_url)

    # Save soup of CWD-B story
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

        # Save HTML of CWD-B
        news_story = urllib.urlopen(url)

        # Save soup of CWD-B
        cwdb_soup = BeautifulSoup(news_story, 'html.parser')

        # Find title
        title = cwdb_soup.find('title').contents[0]

        # Find date
        date = cwdb_soup.find('div',attrs={'class':'view_date_sns'}).p.string
        date = datetime.strptime(date,'%B %d, %Y')
        print('Running CWD' + str(date))

        # Create dictionary for story
        story_dictionary = {'Story title':title, 'Date':date, 'Language': 'English', 'Author':'Republic of Korea  Cheong Wa Dae', 'URL':url}

        # Create dataframe for story
        story_dataframe = pd.DataFrame(data = story_dictionary, index = [0])

        # Concat
        df = pd.concat([df,story_dataframe])

        # Set next url as url
        story_number = int(url[-3:])
        story_number = story_number - 1
        url = url[:-3] + str(story_number)

        # Check if table fully updated
        table_fully_updated = date_last_accessed > df['Date'].min()

    return df

# Define news_df_producer function
def news_df_producer(date):

    '''This function produces an amalgamated news dictionary.'''

    # Produce NSSC PR df
    ROK_NSSC_PR_df = produce_ROK_NSSC_PR_df(date)

    # Produce MOTIE photo news DF
    motie_photo_df = produce_motie_df(date)

    print('motie pr time')

    # Produce MOTIE PR DF
    motie_pr_data = motie_pr_df(date)

    print('now onto mfa')
    # Produce MFA df
    mfa_df = rok_mfa(date)

    print('ok starting CWD')
    # Produce CWD-B df
    cwdb_df = cheong_wa_dae_briefings(date)

    print("now it's speech time!")

    # Concatenate DFs
    news_df = pd.concat([ROK_NSSC_PR_df,motie_photo_df])

    # Concatenate more DFs
    news_df = pd.concat([news_df ,motie_pr_data])

    # Concatenate yet more DFs
    news_df = pd.concat([news_df,mfa_df])

    # and another DF....
    news_df = pd.concat([news_df,cwdb_df])

    # Reset index
    news_df.reset_index(inplace = True)

    # Drop old index column
    news_df.drop(columns='index',inplace=True)

    # Create blank list of rows to drop based on date
    list_of_rows = []

    # Create list of old stories to drop
    for row_index in range(len(news_df.index)):
        if news_df['Date'][row_index] < date:
            list_of_rows.append(row_index)

    # Drop old stories
    news_df.drop(labels=list_of_rows, axis = 0, inplace=True)

    # Reset index
    news_df.reset_index(inplace = True)

    # Drop old index column
    news_df.drop(columns='index',inplace=True)

    # Sort df
    news_df.sort_values(by='Date',inplace=True,axis=0)

    # Reset index
    news_df.reset_index(inplace = True)

    # Drop old index column
    news_df.drop(columns='index',inplace=True)

    # Store df as news_dictionary
    news_dictionary = news_df.to_dict()

    return news_dictionary
