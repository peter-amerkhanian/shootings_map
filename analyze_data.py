from utils import state_codes, states, abbreviation_translate
from init_data import init_data
import requests
import pandas as pd
import os

df = init_data()
key = os.environ['CENSUS_KEY']
census_url = 'https://api.census.gov/data/2018/pep/population?'
PARAMS = {'get': 'POP',
          'for': 'state:*',
          'key': key}
response = requests.get(url=census_url, params=PARAMS)
pops = response.json()

for x in range(len(pops)-1):
    for k, v in state_codes.items():
        if v == pops[x+1][1]:
            pops[x+1][1] = abbreviation_translate(k)
pops = {v: k for k, v in dict(pops).items()}

fatalities_list, states_list, shootings_list, pops_list = [], [], [], []
for state in states.values():
    states_list.append(state)
    pop = int(pops.get(state)) if pops.get(state) else 0
    pops_list.append(pop)
    fatalities_list.append(int(df[df['state'].str.lower() == state.lower()].fatalities.sum()))
    shootings_list.append(len(df[df['state'].str.lower() == state.lower()].index))
fatalities_df = pd.DataFrame.from_dict({'State': states_list,
                                        'Fatalities': fatalities_list,
                                        'Shootings': shootings_list,
                                        'Population': pops_list})

fatalities_df['ShootingFatalitiesPerCapita'] = fatalities_df['Fatalities']/fatalities_df['Population']
fatalities_df['ShootingPerCapita'] = fatalities_df['Shootings']/fatalities_df['Population']
pd.set_option('display.float_format', lambda x: '%.10f' % x)
fatalities_df.to_csv('state_shootings_1982_2019.csv')
