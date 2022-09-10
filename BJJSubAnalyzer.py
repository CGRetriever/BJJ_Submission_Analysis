import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt
plt.rcdefaults()


submission_dictionary = {}
fighter_roster = []


def submission_counter(submission, increment):
    # Making sure the increment variable is an int
    increment = int(increment)

    # This will attempt to increment the counter for the submission. If the submission does not exist then it will
    # add it to the dictionary instead (via the except loop)
    try:
        submission_dictionary[submission] += int(increment)
    except KeyError:
        submission_dictionary[submission] = int(increment)


def get_fighters():
    # This will be grab the information from the bjjheroes website so that we can parse it
    page = requests.get(
        "https://www.bjjheroes.com/a-z-bjj-fighters-list")
    fighter_soup = BeautifulSoup(page.content, 'html.parser')

    # Search through the html for the first and last name of the fighters
    fighters_first_name = fighter_soup.find_all("td", class_='column-1')
    fighters_last_name = fighter_soup.find_all("td", class_='column-2')

    # Weird ass regex stuff. I don't understand it, I just copy and pasted this
    marker1 = ">"
    marker2 = "<"
    regexExpression = marker1 + '(.+?)' + marker2

    # This for loop is to create a full name for each fighter so that we can query the URLs with
    # each fighter's name
    for i, x in zip(fighters_first_name, fighters_last_name):
        tempFirst = str(i)
        tempLast = str(x)

        firstString = re.search(regexExpression, tempFirst).group(1)
        firstString = firstString.split(">")

        lastString = re.search(regexExpression, tempLast).group(1)
        lastString = lastString.split(">")
        fullname = firstString[1] + "-" + lastString[1]
        print(fullname)
        fighter_roster.append(fullname)
        web_scrape(fullname)


def web_scrape(fighter):
    # This sets up the intial request to the site that we want to pull data from
    page = requests.get(
        "https://www.bjjheroes.com/bjj-fighters/" + fighter)
    soup = BeautifulSoup(page.content, 'html.parser')

    # print(soup)

    submissions_html = soup.find_all("div", class_='text')
    submission_numbers = soup.find_all("div", class_='totalvalue')
    example = soup.find_all(id="donut_value")
    marker1 = ">"
    marker2 = "<"
    regexExpression = marker1 + '(.+?)' + marker2

    for i, x in zip(submissions_html, submission_numbers):
        tempSubStr = str(i)
        tempNumStr = str(x)
        submissionString = re.search(regexExpression, tempSubStr).group(1)
        numberString = re.search(regexExpression, tempNumStr).group(1)
        submission_counter(submissionString, numberString)

    print(submission_dictionary)


def create_bar_chart():
    plt.figure(figsize=(20, 3))  # width:20, height:3
    plt.bar(range(len(submission_dictionary)), submission_dictionary.values(), align='edge', width=0.3,
            tick_label=submission_dictionary.keys())
    plt.xticks(range(len(submission_dictionary)), submission_dictionary.keys(), color='orange', rotation=30,
               fontweight='normal', fontsize='10',
               horizontalalignment='right')
    plt.show()


if __name__ == '__main__':
    get_fighters()
    create_bar_chart()
