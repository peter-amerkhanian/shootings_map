import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
from utils import states

url = "https://docs.google.com/spreadsheets/d/1b9o6uDO18sLxBqPwl_Gh9bnhW-ev_dABH83M5Vb5L8o/htmlview?sle=true#gid=0"
today = datetime.today()


def parse_data(uri):
    """
    parse the data from the web
    :param uri: a url of the google spreadsheet
    :return: generate a list of rows in the spreadsheet
    """
    data = requests.get(uri)
    html = BeautifulSoup(data.text, 'html.parser')
    table = html.body.contents[1]
    elements = table.findAll('td')
    cleaned_elements = []
    for elem in elements:
        if not elem == table.find('td', {'class': 'freezebar-cell'}):
            cleaned_elements.append(elem)
    temp = None
    # the number of s0 elements is also the number of rows
    num_rows = len(table.findAll('td', {'class': 's0'}))
    for ind, elem in enumerate(cleaned_elements):
        if ind % num_rows == 0:
            if temp:
                yield temp
            temp = []
        temp.append(elem.text)


def build():
    df = pd.DataFrame(list(parse_data(url)))
    df.at[0, 7] = 'setting'
    df.columns = df.iloc[0]
    df = df.drop(0)
    return df


def abbreviation_translate(abbreviation):
    full = states.get(abbreviation.upper())
    if full:
        return full
    else:
        return abbreviation


def clean_df(df):
    df['fatalities'] = df['fatalities'].astype('int')
    df['injured'] = df['injured'].astype('int')
    df['total_victims'] = df['total_victims'].astype('int')
    df['year'] = df['year'].astype('int')
    df['age_of_shooter'] = df['age_of_shooter'].astype('int')
    df['latitude'] = df['latitude'].astype('float')
    df['longitude'] = df['longitude'].astype('float')
    df['city'], df['state'] = df['location'].str.split(", ").str
    df['state'] = [abbreviation_translate(state) for state in df['state']]
    return df


def init_data():
    df = build()
    df = clean_df(df)
    return df
