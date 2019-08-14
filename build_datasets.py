from processing import init_fred_data, init_data, init_states_df

print('Retrieving and saving mass shooting data from Mother Jones...')
init_data()
print('Retrieving and saving population data from St. Louis Federal Reserve Bank (FRED)...')
init_fred_data()
#TO DO edit the states df module
print('Retrieving and saving population data from US Census...')
init_states_df()
