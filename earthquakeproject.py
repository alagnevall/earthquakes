#Earthquake project dependancies
import json
import requests
import datetime
import sys
sys.path.insert(1,"./library")
from PIL import Image, ImageDraw, ImageFont
import SPI
import SSD1305
import subprocess

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 24
SPI_PORT = 0
SPI_DEVICE = 0

# 128x32 display with hardware SPI:
disp = SSD1305.SSD1305_128_32(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

def printToDisplay(line1,line2,line3):

    HBlackImage = Image.new('1', (disp.height, disp.width))
    draw = ImageDraw.Draw(HBlackImage)   
    font = ImageFont.truetype('./library/KronaOne-Regular.ttf', 8)
    # Draw some shapes.
    # First define some constants to allow easy resizing of shapes.
    padding = 0
    top = padding
    bottom = height-padding
    # Move left to right keeping track of the current x position for drawing shapes.
    x = 0

    
    draw.text((x, top), line1, font = font, fill = 255)
    draw.text((x, top+8), str(line2), font = font, fill = 255)
    draw.text((x, top+16), line3, font = font, fill = 255)
    
  # Display image.
    disp.image(image)
    disp.display()

#Call USGS website with lat/long of Meadowlark Elementary

baseURL = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&"

#paramaters

lat = "37.69"
lng = "-97.16"
# this is in km
radius = "60"
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

print(earthquake, dayssince)
print(info)
printToDisplay(earthquake,dayssince,info)

