def motie_photo_news():

    # Import BeautifulSoup library
    from bs4 import BeautifulSoup

    # Import URL parser library
    import urllib2

    # Import Pandas
    import pandas as pd

    # Save URL of MOTIE website
    motie_photo_news_url = 'http://english.motie.go.kr/en/pc/photonews/bbs/bbsList.do?bbs_cd_n=1'

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
    dictionary = {'Story title':list_of_headlines, 'Links':list_of_links}

    # Create empty dataframe
    headlines_urls = pd.DataFrame(data = dictionary)

    return headlines_urls.to_html()

motie_photo_news()
