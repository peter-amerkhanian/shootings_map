import pandas as pd
from datetime import datetime
from processing.utils import states, state_codes
import os


def init_fred_data():
    state_populations = {}
    for ind, state in enumerate(state_codes.keys()):
        if state == "PR":
            continue
        url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?" \
            "bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&" \
            "graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&" \
            "txtcolor=%23444444&ts=12&tts=12&width=1168&nt=0&thu=0&trc=0&show_legend=yes&" \
            "show_axis_titles=yes&show_tooltip=yes&id={}POP&scale=left&cosd=1900-01-01&" \
            "coed=2018-01-01&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&" \
            "mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Annual&fam=avg&fgst=lin&fgsnd=2009-06-01&" \
            "line_index=1&transformation=lin&vintage_date=2019-08-13&" \
            "revision_date=2019-08-13&nd=1900-01-01".format(state)
        df = pd.read_csv(url)
        print(state, " retrieved.", end=" ")
        if ind == 0:
            state_populations['Year'] = [datetime.strptime(x, "%Y-%m-%d").year for x in df['DATE'].tolist()]
        pop = [x*1000 for x in df['{}POP'.format(state)].tolist()]
        # Normalize the length of Alaska and Hawaii arrays
        while len(pop) != len(state_populations['Year']):
            pop.insert(0, 0)
        state_populations[states[state]] = pop
    df = pd.DataFrame.from_dict(state_populations)
    df.to_csv(os.path.join('data', 'state_pop_1900_2018.csv'))
    return df

