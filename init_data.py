import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
from utils import states


url = "https://docs.google.com/spreadsheets/d/1b9o6uDO18sLxBqPwl_Gh9bnhW-ev_dABH83M5Vb5L8o/htmlview?sle=true#gid=0"
today = datetime.today()


def get_data(uri):
    """
    HELPER for build(). get the table from Mother Jones
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


def abbreviation_translate(state):
    """
    HELPER for alter_rows(). Replaces abbreviated state names with full name
    :param state: the state entry, could be complete, could be abrev
    :return: string of the state in full name form
    """
    full = states.get(state.upper())
    if full:
        return full
    else:
        return state


def correct_types(df):
    """
    HELPER for clean(). Changes data types for the columns in the df
    :param df: the Mother Jones data in df form
    :return: df object with corrected types
    """
    df['fatalities'] = df['fatalities'].apply(int)
    df['injured'] = df['injured'].apply(int)
    df['total_victims'] = df['total_victims'].apply(int)
    df['year'] = df['year'].apply(int)
    df['age_of_shooter'] = df['age_of_shooter'].apply(int)
    df['latitude'] = df['latitude'].apply(float)
    df['longitude'] = df['longitude'].apply(float)
    return df


def alter_rows(df):
    """
    HELPER for clean(). Creates state and city out of location row, applies abbreviation_translate.
    :param df: the Mother Jones data in df form
    :return: df object with new columns and corrected state column
    """
    df['city'], df['state'] = df['location'].str.split(", ").str
    df['state'] = [abbreviation_translate(state) for state in df['state']]
    return df


def build():
    """
    Build the data frame with Mother Jones' data
    :return: df with raw data
    """
    df = pd.DataFrame(list(get_data(url)))
    df.at[0, 7] = 'setting'
    df.columns = df.iloc[0]
    df = df.drop(0)
    return df


def clean(df):
    """
    Clean the data
    :param df: data frame with Mother Jones' data
    :return: df with cleaned data
    """
    df = correct_types(df)
    df = alter_rows(df)
    return df


def init_data():
    """
    Build and clean the data
    :return: df with cleaned version of Mother Jones data
    """
    df = clean(build())
    return df
