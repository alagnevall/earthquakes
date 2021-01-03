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