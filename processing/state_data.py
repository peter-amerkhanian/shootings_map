import pandas as pd
import os
import numpy as np


def init_state_data():
    base_df = pd.read_csv(r'data\mass_shootings_1982_2019.csv')
    pop_df = pd.read_csv(r'data\state_pop_1900_2018.csv', index_col='Year')
    start_year = 1999
    base_df = base_df[base_df.year >= start_year]
    pop_df = pop_df[pop_df.index >= start_year]
    pop_df.loc[2019] = (pop_df.loc[2018])
    dates = pd.DataFrame([pop_df.index, np.zeros_like(pop_df.index), np.zeros_like(pop_df.index)]).T
    dates.columns=['year', 'fatalities', 'shootings']
    all_states_dict = {}
    for x in range(len(pop_df.columns)-1):
        state_dict = {}
        state = base_df[base_df['state'] == pop_df.columns[x+1]]
        state = state.groupby('year', as_index=False)[['fatalities']].sum()
        state = pd.merge(dates, state, how='outer', on='year', copy=False)
        state['fatalities'] = state['fatalities_y']
        state = state.drop(['fatalities_x', 'fatalities_y'], axis=1)
        state = state.fillna(0)
        for ind in range(state.shape[0]):
            year = state.loc[ind, 'year']
            state.loc[ind, 'population'] = pop_df.loc[year, pop_df.columns[x+1]]
            state.loc[ind, 'fatal_per_100k'] = state.loc[ind, 'fatalities']/state.loc[ind, 'population'] * 100000
        max_year = int(min(state[state['fatal_per_100k'] == max(state['fatal_per_100k'].values)].year))
        maximum = np.max(state.fatal_per_100k)
        mean = np.mean(state.fatal_per_100k)
        median = np.median(state.fatal_per_100k)
        all_states_dict[pop_df.columns[x+1]] = {'median': median,
                                                'mean': mean,
                                                'max': maximum,
                                                'max_year': max_year}
    # average yearly mass shooting crime rate, 1999 - 2019
    df = pd.DataFrame(all_states_dict).T.sort_index()
    df.to_csv(os.path.join('data', 'state_shootings_1982_2019_updated.csv'))
    return df
