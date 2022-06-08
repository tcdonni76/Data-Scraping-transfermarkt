# HTML parser
import numpy as np
import re
import requests
from bs4 import BeautifulSoup as soup

names = {}
for year in range(2021, 1992, -1):
    print(str(year))
    # Have the url of each season that
    url = 'https://www.transfermarkt.co.uk/premier-league/transfers/wettbewerb/GB1/plus/?saison_id=' + str(year) + '&s_w=&leihe=1&intern=0&intern=1'
    headers = {'User-Agent':
               'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

    web_page = requests.get(url, headers=headers)

    # call BeautifulSoup for parsing
    page_soup = soup(web_page.content, "html.parser")

    pl_names = page_soup.find_all("h2")
    money_spent = page_soup.find_all(class_ = "transfer-einnahmen-ausgaben redtext")

    order = 0
    for name in pl_names:
        # Checks that it is a club and is not the image of the badge
        if name.a and name.text != "" and name.text:
            # If already have the team
            if name.text not in names.keys():
                names[name.text] = [money_spent[order].text]

            # If do not already have the team
            else:
                names[name.text].append(money_spent[order].text)
            order = order + 1



    print(names)

