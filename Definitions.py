#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

##########################################################################################
#
#	created by: MPZinke
#	on 2020.03.31
#
#	DESCRIPTION:
#	BUGS:
#	FUTURE:
#
##########################################################################################

from PIL import ImageFont


# ————————————————— PROGRAM ——————————————————

### ERROR LOG ###
ERROR_FILE_NAME = "/home/pi/EPaperDisplay/error.log"
DELIMITER = "|"
DATETIME_STRING_FORMAT = "%Y-%m-%d %H:%M:%S"


# —————————————————— IMAGE ———————————————————

### DISPLAY ###
WIDTH = 640  # width of e-paper display
HEIGHT = 384  # height of e-paper display

FONT_PATH = "/home/pi/EPaperDisplay/Dependencies/Zinke_Regular.ttf"  # enjoy
FONT16 = ImageFont.truetype(FONT_PATH, 16)
FONT20 = ImageFont.truetype(FONT_PATH, 20)
FONT24 = ImageFont.truetype(FONT_PATH, 24)
FONT36 = ImageFont.truetype(FONT_PATH, 36)
FONT40 = ImageFont.truetype(FONT_PATH, 40)
FONT42 = ImageFont.truetype(FONT_PATH, 42)
FONT44 = ImageFont.truetype(FONT_PATH, 44)

PEOPLE_PATH = "/home/pi/EPaperDisplay/Dependencies/PeopleIcons/"


# —————————————————— OBJECTS ——————————————————

### CALENDAR ###
CREDENTIAL_PATH = "/home/pi/EPaperDisplay/credentials.json"
PICKLE_PATH = "/home/pi/EPaperDisplay/token.pickle"
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


### HUE ###
BRIDGE_IP_ADDRESS = "10.0.0.2"  # EDIT: put Hue bridge IP here
HUE_LIGHTS = [4, 5, 6, 7]  # EDIT: put Hue light numbers here
USER_NAME = ""  # EDIT: put Hue project API key here


### IP CHECKER ###
ME_IP = "10.0.0.31"  # EDIT: static IP of your Cell on WiFi
IP_USERS =	[
					{"IP" : "10.0.0.31", "image" : "Me.jpg", "name" : "ME", "wait" : 30},
					{"IP" : "10.0.0.33", "image" : "Male.jpg", "name" : "M1", "wait" : 300},
					{"IP" : "10.0.0.34", "image" : "Female.jpg", "name" : "F1", "wait" : 300}
				]  # EDIT: config what you need


### WEATHER ###
API_key = ""  # EDIT: put weather API key here
ZIP_CODE = 0  # EDIT: put zipcode here


