from processing import init_fred_data, init_data, init_state_data

print('Retrieving and saving mass shooting data from Mother Jones...')
init_data()
print('Retrieving and saving population data from St. Louis Federal Reserve Bank (FRED)...')
init_fred_data()
print('Building state by state shootings data')
init_state_data()
