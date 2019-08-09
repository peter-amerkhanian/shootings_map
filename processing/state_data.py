from processing.utils import state_codes, states, abbreviation_translate
from processing.base_data import init_data
import requests
import pandas as pd
import os

key = os.environ['CENSUS_KEY']
census_url = 'https://api.census.gov/data/2018/pep/population?'
PARAMS = {'get': 'POP',
          'for': 'state:*',
          'key': key}


def load_census():
    response = requests.get(url=census_url, params=PARAMS)
    pops = response.json()
    for x in range(len(pops)-1):
        for k, v in state_codes.items():
            if v == pops[x+1][1]:
                pops[x+1][1] = abbreviation_translate(k)
    return {v: k for k, v in dict(pops).items()}


def build_states_df():
    df = init_data()
    census = load_census()
    fatalities_list, states_list, shootings_list, pops_list = [], [], [], []
    for state in states.values():
        states_list.append(state)
        pop = int(census.get(state)) if census.get(state) else 0
        pops_list.append(pop)
        fatalities_list.append(int(df[df['state'].str.lower() == state.lower()].fatalities.sum()))
        shootings_list.append(len(df[df['state'].str.lower() == state.lower()].index))
    fatalities_df = pd.DataFrame.from_dict({'State': states_list,
                                            'Fatalities': fatalities_list,
                                            'Shootings': shootings_list,
                                            'Population': pops_list})
    return fatalities_df


def expand_states_df(fatalities_df):
    fatalities_df['ShootingFatalitiesPerCapita'] = fatalities_df['Fatalities'] / fatalities_df['Population']
    fatalities_df['ShootingPerCapita'] = fatalities_df['Shootings'] / fatalities_df['Population']
    fatalities_df['ShootingFatalitiesPer100000'] = fatalities_df['ShootingFatalitiesPerCapita'] * 100000
    fatalities_df['ShootingPer100000'] = fatalities_df['ShootingPerCapita'] * 100000
    fatalities_df = fatalities_df[fatalities_df['Population'] != 0]
    pd.set_option('display.float_format', lambda x: '%.10f' % x)
    return fatalities_df


def init_states_df():
    df = build_states_df()
    df = expand_states_df(df)
    df.to_csv(os.path.join('data', 'state_shootings_1982_2019.csv'))
    return df
