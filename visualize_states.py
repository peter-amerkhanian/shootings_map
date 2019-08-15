from processing.utils import get_href
import folium
import pandas as pd
import os

url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
state_geo = f'{url}/us-states.json'
state_data = pd.read_csv(os.path.join('data', 'state_shootings_1982_2019.csv'))
df = pd.read_csv(os.path.join('data', 'mass_shootings_1982_2019.csv'))
m = folium.Map(location=[34, -102], zoom_start=4)

folium.Choropleth(
    geo_data=state_geo,
    name='choropleth',
    data=state_data,
    columns=['state', 'mean'],
    key_on='feature.properties.name',
    fill_color='YlGn',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Average Yearly Mass Shooting Fatalities per 100,000 people, 1999-2019').add_to(m)
folium.LayerControl().add_to(m)

icon_url = 'https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com' \
           '/thumbs/120/microsoft/209/large-red-circle_1f534.png'

for i in range(df.shape[0]):
    event = df.iloc[i]
    if event.year < 1999:
        continue
    href = get_href(event)
    popup = f'''
    <b>
        <a href="{get_href(event)}">{event.case}</a>
    </b>
    <hr>
    <p>
    Fatalities: {event.fatalities} <br/>
    Injured: {event.injured} <br/>
    Date: {event.date}
    </p>
    '''
    folium.Marker(location=(event.latitude,
                            event.longitude),
                  popup=popup,
                  icon=folium.features.CustomIcon(icon_image=icon_url,
                                                  icon_size=(8, 8))).add_to(m)
m.save(os.path.join('visuals', 'state_shootings_1982_2019.html'))
