# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 00:16:24 2018

@author: HP
"""


import requests
import ogr  
import json
import flask

def GeomPoint(Geom): 
    lon = Geom.GetX()
    lat = Geom.GetY()        
    return lon, lat

app = flask.Flask('server')

@app.route('/')
def site():
    return flask.redirect("./site/index.html", code=302)

@app.route('/site/<path:path>')
def shareSite(path):
        return flask.send_from_directory('site', path)



@app.route('/getdata')
def getData():
    Shp = ogr.Open(r'D:\Users\HP\Desktop\hackathon\points\glims_points.shp')  
    url = "http://api.planetos.com/v1/datasets/noaa_gfs_pgrb2_global_forecast_recompute_0.25degree/point"
    Layer = Shp.GetLayer()   
    F_count = Layer.GetFeatureCount() 
    data = []
    for number in range(F_count):
        Pol_i = Layer.GetFeature(number)  
        Geom = Pol_i.GetGeometryRef()
        lon, lat = GeomPoint(Geom)    
        querystring = {"lon": lon, "lat": lat,"apikey":"71bf43647607441faf0e31c8b72e7b67"}
        response = requests.request("GET", url, params=querystring)
        response = json.loads(response.text);
        response = response['entries'][len(response['entries'])-1]['data']['Maximum_temperature_height_above_ground_Mixed_intervals_Maximum']
        res = int(response) - 273
        if res > 0:
            data.append([lon,lat])
    
    return json.dumps(data)