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

def motie_pr():

    # Define press release page url as variable
    url = 'http://english.motie.go.kr/en/pc/pressreleases/bbs/bbsList.do?bbs_cd_n=2'

    # Save PR page
    motie_pr = urllib2.urlopen(url)

    # Save MOTIE pr as soup
    soup = BeautifulSoup(motie_pr, 'html.parser')

    # Find first MOTIE PR
    first_motie_pr = str(soup.find(href=re.compile('bbsView'))['href'])

    # Set first MOTIE PR as current PR number
    current_PR_number = first_motie_pr[21:24]

    # Set fully_updated as boolean variable
    fully_updated = False

    while fully_updated is False:

        # Save URL for story
        url = 'http://english.motie.go.kr/en/pc/pressreleases/bbs/bbsView.do?bbs_seq_n={}&bbs_cd_n=2&currentPage=1&search_key_n=&search_val_v=&cate_n='.format(current_PR_number)

        # Save PR Page
        pr = urllib2.urlopen(url)

        # Save PR soup
        soup = BeautifulSoup(pr, 'html.parser')

        # Find PR pr_title - NEED TO FIND TITLE WITHIN THIS SOUP
        pr_title = soup.find('div', class_='press_view')
