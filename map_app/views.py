import folium
from folium.plugins import Search, MarkerCluster
import pandas as pd
import json
import geopandas as gpd
from django.shortcuts import render

def dms_to_dd(dms_str):
    """Convert DMS (Degrees Minutes Seconds) string to decimal degrees."""
    parts = dms_str.split()
    degrees = float(parts[0])
    minutes = float(parts[1])
    seconds = float(parts[2])
    return degrees + (minutes / 60) + (seconds / 3600)

def map_view(request):
    with open("C:/Users/71/map_project/Data/Indian_States.geojson", 'r') as f:
        india_geojson = json.load(f)

    data = pd.read_csv("G:/SUMAN/wb_map/cors_data.csv") 

    latitude = dms_to_dd(data['Latitude of Site (DMS)'][0])  
    longitude = dms_to_dd(data['Longitude of Site (DMS)'][0]) 

    m = folium.Map(location=[latitude, longitude], zoom_start=6)

    folium.GeoJson(india_geojson, name="State Boundaries").add_to(m)

    # Dictionary to hold feature groups by attribute
    feature_groups = {}
    # Create feature groups for each unique state
    for state in data['State'].unique():
        feature_group = folium.FeatureGroup(name=f"{state}")
        feature_groups[state] = feature_group
        feature_group.add_to(m)

    features = []

    for index, row in data.iterrows():
        lat = dms_to_dd(row['Latitude of Site (DMS)'])
        lon = dms_to_dd(row['Longitude of Site (DMS)'])
        popup_text = f"""
        <b>State:</b> {row['State']}<br>
        <b>Site Name:</b> {row['Site Name']}<br>
        <b>Vendor:</b> {row['Vendor Username']}<br>
        <b>Latitude:</b> {lat:.6f}<br>
        <b>Longitude:</b> {lon:.6f}
        """
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [lon, lat]
            },
            "properties": {
                "popup": popup_text,
                "Site Name": row['Site Name'],
                "State":row['State'],
                "Latitude": lat,
                "Longitude": lon
            }
        }
        features.append(feature)
        
        marker = folium.Marker(
            location=[lat, lon],
            popup=popup_text
        )
        
        if row['State'] in feature_groups:
            marker.add_to(feature_groups[row['State']])


    geojson = folium.GeoJson(
        data={"type": "FeatureCollection", "features": features},
        name="Stations",
        tooltip=folium.features.GeoJsonTooltip(
            fields=["State", "Site Name", "Latitude", "Longitude"],
            aliases=["State:", "Site Name:","Latitude:", "Longitude:"],
            localize=True
        ),
    ).add_to(m)

    Search(
        layer=geojson,
        search_label="Site Name",
        placeholder="Search for station...",
        collapsed=False,
        search_zoom= 28,
        zoom_on_click=True
    ).add_to(m)


    folium.LayerControl(collapsed=False).add_to(m)

    map_html = m._repr_html_()

    return render(request, 'map_app/map.html', {'map': map_html})








