from init_data import init_data # something with automatically updating the data
from utils import get_href, get_measurements
import folium


df = init_data()
map_object = folium.Map(
    location=[34, -104],
    zoom_start=4,
    tiles='OpenStreetMap')
icon_url = 'https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com' \
           '/thumbs/120/microsoft/209/large-red-circle_1f534.png'
for i in range(df.shape[0]):
    event = df.iloc[i]
    href = get_href(event)
    popup = f'''
    <b>
        <a href="{get_href(event)}">{event.case}</a>
    </b>
    <p>
    Fatalities: {event.fatalities} <br/>
    Injured: {event.injured} <br/>
    Date: {event.date}
    </p>
    '''
    measure = get_measurements(event)
    folium.Marker(location=(float(event.latitude),
                            float(event.longitude)),
                  popup=popup,
                  icon=folium.features.CustomIcon(icon_image=icon_url,
                                                  icon_size=(float(measure), float(measure)))).add_to(map_object)
map_object.save('mass_shootings_1982_2019.html')
