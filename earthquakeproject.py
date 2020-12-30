#Earthquake project dependancies
import json
import requests
import datetime
import sys
sys.path.insert(1,"./library")
import epd2in13
from PIL import Image, ImageDraw, ImageFont


##start code to display on pi screen

epd = epd2in13.EPD() # get the display
epd.init() 
print("Clear screen") #debugging use
epd.Clear(0xFF) #clear screen back to white

def printToDisplay(string):

    HBlackImage = Image.new('1', (epd2in13.EPD_HEIGHT, epd2in13.EPD_WIDTH), 255)
    draw = ImageDraw.Draw(HBlackImage)   
    font = ImageFont.truetype('/usr/share/fonts/truetype/google/Bangers-Regular.ttf', 30)
    draw.text((25, 65), string, font = font, fill = 0)
    epd.display(epd.getbuffer(HBlackImage))


#Call USGS website with lat/long of Lagnevall house

baseURL = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&"

#paramaters

lat = "37.6955"
lng = "-97.1632"
# this is in km
radius = "48"
limit =  "1"
orderby = "time"

query = f"latitude={lat}&longitude={lng}&maxradiuskm={radius}&limit={limit}&orderby={orderby}"



response = requests.get(baseURL+query).json()
# print(response)

timestamp= int(response["features"][0]["properties"]["time"])
# print(timestamp)
quaketime = datetime.datetime.fromtimestamp(timestamp//1000.0)

clock = datetime.datetime.now() - quaketime


#store as variables instead of print statements to prep for raspberry pi
earthquake = f"Days since last Earthquake"
dayssince = (clock).days
info = f'{response["features"][0]["properties"]["title"]} on {(quaketime).strftime("%Y-%m-%d %H:%M:%S")}'


printToDisplay(info)

