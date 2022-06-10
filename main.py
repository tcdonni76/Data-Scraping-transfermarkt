import requests
import csv
import re
from bs4 import BeautifulSoup as soup


def clean_expenditure(expenditure):
    arr = re.split("([0-9]+[.]?[0-9]+)", expenditure)
    # Catch if team has spent no money
    if len(arr) > 1:
        val = float(arr[1])
        if arr[2].strip() != 'm':
            val = val / 1000
        return val
    else:
        return 0


start_year = 2021
end_year = 1991
names = {}

header = ["Team"]

for year in range(start_year, end_year, -1):
    print(str(year))
    header.append(year)
    # Have the url of each season that
    url = 'https://www.transfermarkt.co.uk/premier-league/transfers/wettbewerb/GB1/plus/?saison_id=' + str(year) + '&s_w=&leihe=1&intern=0&intern=1'
    headers = {'User-Agent':
               'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

    web_page = requests.get(url, headers=headers)

    # call BeautifulSoup for parsing
    page_soup = soup(web_page.content, "html.parser")

    pl_names = page_soup.find_all("h2")
    money_spent = page_soup.find_all(class_="transfer-einnahmen-ausgaben redtext")

    order = 0
    for name in pl_names:
        # Checks that it is a club and is not the image of the badge
        if name.a and name.text != "" and name.text:
            expenditure = clean_expenditure(money_spent[order].text)
            # If already have the team
            if name.text not in names.keys():
                names[name.text] = [[expenditure, year]]

            # If do not already have the team
            else:
                names[name.text].append([expenditure, year])
            order = order + 1


print(names)

with open('transfer_history.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    for key, val in names.items():
        row = [key]
        curr_el = 0
        for n in range(start_year, end_year, -1):
            if curr_el < len(val):
                if int(val[curr_el][1]) == n:
                    row.append(str(val[curr_el][0]))
                    curr_el += 1
                else:
                    row.append(" ")
            else:
                row.append(" ")
        writer.writerow(row)
