#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 18:09:44 2022

@author: lucywang
"""

from bs4 import BeautifulSoup
import requests
import pgeocode
import os
import datetime
import pymongo
import pprint
import pandas as pd


zipcode = input()
nomi = pgeocode.Nominatim('us')
lat = nomi.query_postal_code(zipcode)['latitude']
lon = nomi.query_postal_code(zipcode)['longitude']
website = "https://forecast.weather.gov/MapClick.php?lat="+str(lat)+"&lon="+str(lon)+"#.Y22HCy1h1QI"
#print(website)
page = requests.get(website)
page.status_code
page.content
soup = BeautifulSoup(page.content, 'html.parser')
#print(soup.prettify())


#Scrape the 7 day forecast and display to the user
seven_day=soup.find(id="seven-day-forecast")
forecast_items = seven_day.find_all(class_="tombstone-container")
tonight = forecast_items[0]

period_tags = seven_day.select(".tombstone-container .period-name") 
periods = [pt.get_text() for pt in period_tags]
periods

short_descs = [sd.get_text() for sd in seven_day.select(".tombstone-container .short-desc")]
temps = [t.get_text() for t in seven_day.select(".tombstone-container .temp")]
descs = [d["title"] for d in seven_day.select(".tombstone-container img")]
print(short_descs)
                                                                                                                                                              
weather = {
    "period": periods, 
    "short_desc": short_descs, 
    "temp": temps, 
    "desc":descs
} 
weather                                                                                
                                                                                
                                                                                
                                                                                

#Display the current conditions - humidity, windspeed, Dewpoint and Last Update Time
conditions = soup.body.find(id='current_conditions_detail')
conditions = conditions.find_all("td")

humidity = conditions[1].get_text()
windspeed = conditions[3].get_text()
dewpoint = conditions[7].get_text()
last_update_time = conditions[11].get_text().strip(" ")[-18:]

conditions_info = {"Humidity": humidity,
        "Windspeed": windspeed,
        "Dewpoint": dewpoint,
        "Last Update Time": last_update_time
       }

conditions_info





host_name = "localhost"
port = "27017"

atlas_cluster_name = "sandbox"
atlas_default_dbname = "local"
#atlas_user_name = "m001-student"
#atlas_password = "m001-mongodb-basics"


conn_str = {
    "local" : f"mongodb://{host_name}:{port}/",
#    "atlas" : f"mongodb+srv://{atlas_user_name}:{atlas_password}@{atlas_cluster_name}.zibbf.mongodb.net/{atlas_default_dbname}"
}

client = pymongo.MongoClient(conn_str["local"])

print(f"Local Connection String: {conn_str['local']}")
#print(f"Atlas Connection String: {conn_str['atlas']}")





#Store the 7 day forecast in a MongoDB
db_name = "forecast"

db = client[db_name]
client.list_database_names()

posts = db.posts
post_id = posts.insert_one(weather).inserted_id

#print("Document ID: ", post_id)

#print("Databases: ", client.list_database_names())
#print("Collections: ", db.list_collection_names())

#pprint.pprint(posts.find_one({}))





#Store the current conditions in a MongoDB
db_name = "conditions"

db = client[db_name]
client.list_database_names()

posts = db.posts
post_id = posts.insert_one(conditions_info).inserted_id

#print("Document ID: ", post_id)

#print("Databases: ", client.list_database_names())
#print("Collections: ", db.list_collection_names())

#pprint.pprint(posts.find_one({}))


