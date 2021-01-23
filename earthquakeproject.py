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

def printToDisplay(line1,line2,line3,line4,line5):

    image = Image.new('1', (disp.width, disp.height))
    draw = ImageDraw.Draw(image)   
    # font = ImageFont.truetype('./library/KronaOne-Regular.ttf', 8)
    font = ImageFont.truetype('./library/04B_08.TTF', 8)
    font2 = ImageFont.truetype('./library/04B_08.TTF', 6)
    # Draw some shapes.
    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,disp.width,disp.height), outline=0, fill=0)

    # First define some constants to allow easy resizing of shapes.
    padding = 0
    top = padding
    bottom = disp.height-padding
    # Move left to right keeping track of the current x position for drawing shapes.
    x = 0

    
    draw.text((x, top), line1, font = font, fill = 255)
    draw.text((x, top+8), line2, font = font, fill = 255)
    draw.text((x, top+16), line3, font = font, fill = 255)
    draw.text((x, top+24), line4, font = font, fill = 255)
    draw.text((x+75, top+8), line5, font = font, fill = 255)
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
earthquake = f"Last Earthquake: {(clock).days} Days "
# dayssince = f"{(clock).days} Days"
info = f'{response["features"][0]["properties"]["title"]}'.split(' of ')
quakedate = f'on {(quaketime).strftime("%Y-%m-%d %H:%M")}'
hours = (f'{round((clock).seconds/3600,0)} Hours')

print(earthquake)
print(info[0])
print(info[1])
print(quakedate)
print(hours)

printToDisplay(earthquake,info[0],info[1], quakedate, hours)

