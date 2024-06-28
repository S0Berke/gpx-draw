
from typing import Tuple, List, Dict

import pandas as pd
import folium

pd.set_option('display.precision', 2)


df_sites = pd.DataFrame(
    [['hotel',              48.8527, 2.3542],
     ['Sacre Coeur',        48.8867, 2.3431],   
     ['Louvre',             48.8607, 2.3376],
     ['Montmartre',         48.8872, 2.3388],
     ['Port de Suffren',    48.8577, 2.2902],
     ['Arc de Triomphe',    48.8739, 2.2950],
     ['Av. Champs Élysées', 48.8710, 2.3036],
     ['Notre Dame',         48.8531, 2.3498],
     ['Tour Eiffel',        48.8585, 2.2945]],
    columns=pd.Index(['site', 'latitude', 'longitude'], name='paris')
)

df_sites

avg_location = df_sites[['latitude', 'longitude']].mean()
map_paris = folium.Map(location=avg_location, zoom_start=13)

for site in df_sites.itertuples():
    marker = folium.Marker(location=(site.latitude, site.longitude),
                           tooltip=site.site)
    marker.add_to(map_paris)

map_paris

for site in df_sites.itertuples():
    marker = folium.Marker(location=(site.latitude, site.longitude),
                           tooltip=site.site)
    marker.add_to(map_paris)

map_paris
 
df_route_segments = df_route.join(
    df_route.shift(-1),  # map each stop to its next stop
    rsuffix='_next'
).dropna()  # last stop has no "next one", so drop it

df_route_segments

map_paris = folium.Map(location=avg_location, zoom_start=13)

for stop in df_route_segments.itertuples():
    initial_stop = stop.Index == 0
    # icon for current stop
    icon = folium.Icon(icon='home' if initial_stop else 'info-sign', 
                       color='cadetblue' if initial_stop else 'red')
    # marker for current stop
    marker = folium.Marker(location=(stop.latitude, stop.longitude),
                           icon=icon, tooltip=stop.site)
    # line for the route segment connecting current to next stop
    line = folium.PolyLine(
        locations=[(stop.latitude, stop.longitude), 
                   (stop.latitude_next, stop.longitude_next)],
        tooltip=f"{stop.site} to {stop.site_next}",
    )
    # add elements to the map
    marker.add_to(map_paris)
    line.add_to(map_paris)

# When for loop ends, the stop variable has the second-to-last 
# stop in the route, so the marker for the last stop is missing 
# We add it now using the "next" columns of the last row
folium.Marker(
    location=(stop.latitude_next, stop.longitude_next),
    tooltip=stop.site_next, 
 
   icon = folium.Icon(icon='info-sign', color='red')
   ).add_to(map_paris)

map_paris  # show map

from geopy.distance import geodesic

_Location = Tuple[float, float]


def ellipsoidal_distance(point1: _Location, point2: _Location) -> float:
    """Calculate ellipsoidal distance (in meters) between point1 and 
    point2 where each point is represented as a tuple (lat, lon)"""
    return geodesic(point1, point2).meters

df_route_segments['distance_seg'] = df_route_segments.apply(
    lambda stop: ellipsoidal_distance(
        (stop.latitude, stop.longitude), 
        (stop.latitude_next, stop.longitude_next)), 
    axis=1
)

df_route_segments
map_paris = folium.Map(location=avg_location, zoom_start=13)

for stop in df_route_segments.itertuples():
    initial_stop = stop.Index == 0
    # marker for current stop
    icon = folium.Icon(icon='home' if initial_stop else 'info-sign', 
                       color='cadetblue' if initial_stop else 'red')
    marker = folium.Marker(
        location=(stop.latitude, stop.longitude),
        icon=icon, 
        # display the name and stop number at each site's marker
        tooltip=f"<b>Name</b>: {stop.site} <br>" \
              + f"<b>Stop number</b>: {stop.Index} <br>"
    )
    # line for the route segment connecting current to next stop
    line = folium.PolyLine(
        locations=[(stop.latitude, stop.longitude), 
                   (stop.latitude_next, stop.longitude_next)],
        # display the start, end, and distance of each segment
        tooltip=f"<b>From</b>: {stop.site} <br>" \
              + f"<b>To</b>: {stop.site_next} <br>" \
              + f"<b>Distance</b>: {stop.distance_seg:.0f} m",
    )
    # add elements to the map
    marker.add_to(map_paris)
    line.add_to(map_paris)

# add route's last marker, as it wasn't included in for loop
folium.Marker(
    location=(stop.latitude_next, stop.longitude_next),
    tooltip=f"<b>Name</b>: {stop.site_next} <br>" \
          + f"<b>Stop number</b>: {stop.Index + 1} <br>", 
    icon = folium.Icon(icon='info-sign', color='red')
).add_to(map_paris);

map_paris  # show map

def _make_route_segments_df(df_route: pd.DataFrame) -> pd.DataFrame:
    """Given a dataframe whose rows are ordered stops in a route, 
    and where the index has integers representing the visit order of those
    stops, return a dataframe having new columns with the information of 
    each stop's next site"""
    df_route_segments = df_route.join(
        df_route.shift(-1),  # map each stop to its next
        rsuffix='_next').dropna()

    df_route_segments['distance_seg'] = df_route_segments.apply(
        lambda stop: ellipsoidal_distance(
            (stop.latitude, stop.longitude), 
            (stop.latitude_next, stop.longitude_next)
        ), axis=1
    )
    return df_route_segments


def plot_route_on_map(df_route: pd.DataFrame) -> folium.Map:
    """Takes a dataframe of a route and displays it on a map, adding 
    a marker for each stop and a line for each pair of consecutive 
    stops"""
    df_route_segments = _make_route_segments_df(df_route)
    
    # create empty map
    avg_location = df_route[['latitude', 'longitude']].mean()
    map_route = folium.Map(location=avg_location, zoom_start=13)

    for stop in df_route_segments.itertuples():
        initial_stop = stop.Index == 0
        # marker for current stop
        icon = folium.Icon(icon='home' if initial_stop else 'info-sign', 
                           color='cadetblue' if initial_stop else 'red')
        marker = folium.Marker(
            location=(stop.latitude, stop.longitude),
            icon=icon, 
            tooltip=f"<b>Name</b>: {stop.site} <br>" \
                  + f"<b>Stop number</b>: {stop.Index} <br>"
        )
        # line for the route segment connecting current to next stop
        line = folium.PolyLine(
            locations=[(stop.latitude, stop.longitude), 
                       (stop.latitude_next, stop.longitude_next)],
            # add to each line its start, end, and distance
            tooltip=f"<b>From</b>: {stop.site} <br>" \
                  + f"<b>To</b>: {stop.site_next} <br>" \
                  + f"<b>Distance</b>: {stop.distance_seg:.0f} m",
        )
        # add elements to the map
        marker.add_to(map_route)
        line.add_to(map_route)
    
    # When for loop ends, the stop variable has the second-to-last stop in 
    # the route, so the marker for the last stop is missing, and we add it 
    # now using the "next" columns of the last row
    folium.Marker(
        location=(stop.latitude_next, stop.longitude_next),
        tooltip=f"<b>Name</b>: {stop.site_next} <br>" \
              + f"<b>Stop number</b>: {stop.Index + 1} <br>", 
        icon = folium.Icon(icon='info-sign', color='red')
    ).add_to(map_route)
    
    return map_route

df_route_closed = pd.concat(
   [df_route, df_route.head(1)], ignore_index=True
)
df_route_closed.index.name = df_route.index.name

df_route_closed

plot_route_on_map(df_route_closed)

# NOTE: trimmed down function for reference only, do not copy-paste.
def plot_route_on_map(df_route: pd.DataFrame) -> folium.Map:
    #----- map is created here -----
    # ...
    #----- markers are created here -----
    for stop in df_route_segments.itertuples():
        # ...
        # ( ఠ ͟ʖ ఠ)
        # ...
        # for loop ends!

    ### 𝗡𝗲𝘄 𝗰𝗼𝗻𝗱𝗶𝘁𝗶𝗼𝗻 𝗰𝗵𝗲𝗰𝗸𝗲𝗿 ###
    # check if first site's name and location coincide with last's?
     first_stop = df_route.iloc[0][['site', 'latitude', 'longitude']]
    last_stop = df_route.iloc[-1][['site', 'latitude', 'longitude']]
    is_closed_tour = (first_stop == last_stop).all()
    
    # When for loop ends, the marker for the last stop is missing 
    # (**unless the route is closed**). if the route is not closed, 
    # we add it now using the "next" columns of the last row
    if not is_closed_tour:
        folium.Marker(
            location=(stop.latitude_next, stop.longitude_next),
            tooltip=f"<b>Name</b>: {stop.site_next} <br>" \
                  + f"<b>Stop number</b>: {stop.Index + 1} <br>", 
            icon = folium.Icon(icon='info-sign', color='red')
        ).add_to(map_route)
    
    return map_route

plot_route_on_map(df_route_closed)

TAG_ROUTE_NAME = "Name"
TAG_NUMBER_STOPS = "Num stops"
TAG_TOTAL_DISTANCE = "Distance"
_SPACE_HTML = "&nbsp"  # needed to add empty spaces between KPIs

# get summary info to display on map
name = df_route_segments.columns.name.capitalize()
n_stops = df_route_segments['site'].size
route_distance = df_route_segments['distance_seg'].sum().round(0)

from IPython.display import HTML, display
# show a hello world message in blue and bold 
display(HTML("<span style='color:steelblue'>Hello <b>world</b></span>"))

_html_text_title = f"<b>{TAG_ROUTE_NAME}</b>: {name}"

display(HTML(_html_text_title))  # [Out]: 𝗡𝗮𝗺𝗲: Paris

STYLE_TITLE = (
    "position:absolute;z-index:100000;left:5vw;color:black;"
    "font-size:30px;text-shadow:-1px 0 white, 0 1px white, 0 1px white"
)
html_title = f'<h3 style="{STYLE_TITLE}">{_html_text_title}</h3>'

# let's see how that title looks like on the map (run all in same cell):
map_with_title = plot_route_on_map(df_route)

root_map = map_with_title.get_root()
root_map.html.add_child(folium.Element(html_title))

map_with_title

_html_text_summary = f"""
<b>{TAG_NUMBER_STOPS}</b> <b>{TAG_TOTAL_DISTANCE}</b>
<br>
{n_stops} {16 * _SPACE_HTML} {route_distance:.0f} m
"""

display(HTML(_html_text_summary))
# [Out]:
# 𝐍𝐮𝐦 𝐬𝐭𝐨𝐩𝐬  𝐃𝐢𝐬𝐭𝐚𝐧𝐜𝐞
# 8          25158 m
STYLE_SUMMARY = (
    "position:absolute;z-index:100000;font-size:20px;"
    "right:0;bottom:0;color:black;"
    "text-shadow:-1px 0 white, 0 1px white, 0 1px white"
)
html_summary = f'<h2 style="{STYLE_SUMMARY}">{_html_text_summary}</h2>'

# let's see how the KPIs look like (run all in same cell):
map_with_kpis = plot_route_on_map(df_route)

root_map = map_with_kpis.get_root()
root_map.html.add_child(folium.Element(html_summary))

map_with_kpis

my_map = plot_route_on_map(df_route)

root_map = my_map.get_root()
root_map.html.add_child(folium.Element(html_title))  # add title
root_map.html.add_child(folium.Element(html_summary))  # add summary KPIs
my_map  # check it out

def _get_text_for_title(df_route_segments):
    """Given a dataframe representing a route, where the column index has 
    the name of the route, returns an HTML string with a nice display of 
    this name"""
    # 1) get the info to display
    name = df_route_segments.columns.name
    name = name.capitalize() if name else ''
    
    # 2) parse the info as HTML for addition to map
    _html_text_title = f"<b>{TAG_ROUTE_NAME}</b>: {name}"
    html_title = f'<h3 style="{STYLE_TITLE}">{_html_text_title}</h3>'
    return html_title


def _get_kpis_to_display_on_map(df_route_segments):
    """Given a dataframe representing a route, and having columns 'site' 
    and 'distance_seg', returns an HTML string with a nice display of 
    the number of sites and the total distance of the route"""
    # 1) get the info to display
    n_stops = df_route_segments['site'].size
    route_distance = df_route_segments['distance_seg'].sum().round(0)
    
    # 2) parse the info as HTML for addition to map
    _html_text_summary = f"""
    <b>{TAG_NUMBER_STOPS}</b> <b>{TAG_TOTAL_DISTANCE}</b>
    <br>
    {n_stops} {16 * _SPACE_HTML} {route_distance:.0f} m
    """
    html_summary = f'<h2 style="{STYLE_SUMMARY}">{_html_text_summary}</h2>'
    return html_summary

def display_route_on_map(df_route, include_kpis=True) -> folium.Map:
    """Given a dataframe representing a route, creates a folium map 
    and adds markers for the stops and lines for the route segments, 
    with the option to also add an automatic title and 2 KPIs: 
     - number of stops in the route
     - total distance of route
    
    Parameters
    ----------
    df_route : pd.DataFrame
      A dataframe representing a route, whereby each row contains
      information on a different stop of the route, and rows are sorted 
      by stop visiting order.
    include_kpis : bool (default=True)
      Whether to include the title and the 2 KPIs in the map

    Returns
    -------
    A folium map that can be displayed or re-used"""
    # 1) create empty map
    avg_location = df_route[['latitude', 'longitude']].mean()
    map_route = folium.Map(location=avg_location, zoom_start=13)

    # 2) create DF with segment information
    df_route_segments = _make_route_segments_df(df_route)
    
    # 3) add title and KPIs to the map
    if include_kpis:
        html_title = _get_text_for_title(df_route_segments)
        html_summary = _get_kpis_to_display_on_map(df_route_segments)
        root_map = map_route.get_root()
        root_map.html.add_child(folium.Element(html_title))  # add title
        root_map.html.add_child(folium.Element(html_summary))  # add KPIs

    # 4) add route to the map
    for stop in df_route_segments.itertuples():
        initial_stop = stop.Index == 0
        # marker for current stop
        icon = folium.Icon(icon='home' if initial_stop else 'info-sign', 
                           color='cadetblue' if initial_stop else 'red')
        marker = folium.Marker(
            location=(stop.latitude, stop.longitude),
            icon=icon, 
            tooltip=f"<b>Name</b>: {stop.site} <br>" \
                  + f"<b>Stop number</b>: {stop.Index} <br>"
        )
        # line for the route segment connecting current to next stop
        line = folium.PolyLine(
            locations=[(stop.latitude, stop.longitude), 
                       (stop.latitude_next, stop.longitude_next)],
            # add to each line its start, end, and distance
            tooltip=f"<b>From</b>: {stop.site} <br>" \
                  + f"<b>To</b>: {stop.site_next} <br>" \
                  + f"<b>Distance</b>: {stop.distance_seg:.0f} m",
        )
        # add elements to the map
        marker.add_to(map_route)
        line.add_to(map_route)

    # does the first site's name and location coincide with the last's?
    first_stop = df_route.iloc[0][['site', 'latitude', 'longitude']]
    last_stop = df_route.iloc[-1][['site', 'latitude', 'longitude']]
    is_closed_tour = (first_stop == last_stop).all()
    
    # When for loop ends, the stop variable has the second-to-last 
    # stop in the route, so the marker for the last stop is missing 
    # (**unless the route is closed**). We add it now using 
    # the "next" columns of the last row, if the route is open
    if not is_closed_tour:
        folium.Marker(
            location=(stop.latitude_next, stop.longitude_next),
            tooltip=f"<b>Name</b>: {stop.site_next} <br>" \
                  + f"<b>Stop number</b>: {stop.Index + 1} <br>", 
            icon = folium.Icon(icon='info-sign', color='red')
        ).add_to(map_route)

    return map_route

