from bs4 import BeautifulSoup
import requests
import time
import numpy as np
import pandas as pd


# Swellnet's robot.txt - 10 sec request interval - Doesn't disallow crawling the report pages
# https://www.swellnet.com/robots.txt?upapi=true
def main():
    surf_spots = [
        "https://www.swellnet.com/reports/australia/victoria/phillip-island",
        "https://www.swellnet.com/reports/australia/victoria/warrnambool",
        "https://www.swellnet.com/reports/australia/victoria/torquay",
        "https://www.swellnet.com/reports/australia/victoria/mornington-peninsula",
        "https://www.swellnet.com/reports/australia/victoria/barwon-heads",
    ]
    f = open("report_cache.csv", "a")

    for i in range(0, len(surf_spots)):
        row = crawler(surf_spots[i])
        f.write("\n{location}, {date}, {rating}".format(location=row[0], date=row[1], rating=row[2]))
        time.sleep(10)

    f.close()


# function for traversing a site, cleaning the data then adding it to a pandas database
def crawler(spot):
    location, date, rating = None, None, None
    html_doc = requests.get(spot).text
    soup = BeautifulSoup(html_doc, 'html.parser')
    div_container = soup.findAll('span', class_='field-content')
    if div_container:
        location = div_container[0].text
    div_container = soup.find('span', class_='views-field views-field-field-surf-report-date')
    if div_container:
        date = div_container.find('span', class_='field-content').text
    div_container = soup.find('span', class_='views-field views-field-field-surf-report-rating')
    if div_container:
        rating = div_container.find('span', class_='field-content').text
    print([location, date, rating])
    return [location, date, rating]


main()

# Location
# <div class="views-field views-field-title">        <span class="field-content">Phillip Island</span>  </div>
# <div class="views-row views-row-1 views-row-odd views-row-first views-row-last">
# <div class="views-field views-field-title">        <span class="field-content">Phillip Island</span>  </div>  </div>

# Time
# <span class="views-field views-field-field-surf-report-date">    <span class="views-label views-label-field-surf-report-date">Updated: </span>    <span class="field-content">2021-11-09 14:23:00</span>  </span>
# rating
# <span class="views-field views-field-field-surf-report-date">    <span class="views-label views-label-field-surf-report-date">Updated: </span>    <span class="field-content">2021-11-04 14:28:00</span>  </span>

# <div class="panel-pane pane-views-panes pane-surf-reports-panel-pane">
