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


from datetime import datetime
import os
from PIL import Image
import requests
from threading import Thread
from time import sleep

from Definitions import *
import ErrorWriter


WEATHER_PATH = "/home/pi/EPaperDisplay/Dependencies/WeatherIcons/"
WEATHER_ICONS = 	{	
							"broken clouds" : "cloudy.jpg",		"error" : "error.jpg",	
							"few clouds" : "partCloudy.jpg", 	"foggy" : "foggy.jpg",
							"heavy rain" : "ain.jpg",			"heavy intensity rain" : "rain.jpg",
							"icey" : "icey.jpg",					"light rain" : "rain.jpg",
							"mist" : "foggy.jpg",				"moderate rain" : "rain.jpg",
							"overcast clouds" : "cloudy.jpg",	"scattered clouds" : "partCloudy.jpg", 
							"rain" : "rain.jpg", 					"scattered clouds" : "partCloudy.jpg",
							"snow" : "snow.jpg",				"clear sky" : "sunny.jpg", 
							"thunderstorm" : "tStorm.jpg",		"tStorms" : "tStorms.jpg",
							"wind" : "windy.jpg"
						}


class Weather:
	def __init__(self, API_key, zip_code, wait=300):
		if "error" not in WEATHER_ICONS \
		or not os.path.exists(WEATHER_PATH+WEATHER_ICONS["error"]):
			raise Exception("The default icon of error.jpg does not exist")

		self.API_key = API_key
		self.zip_code = zip_code
 
		self.current_temp = -273
		self.high = -273
		self.low = -273
		self.city = "Error"
		self.condition = "error"
		self.icon = None

		self.has_not_ended = True
		self.sleep_until_time = datetime.now()
		self.thread = Thread(target=self.thread_loop)
		self.wait = wait


	def create_icon(self):
		if self.condition not in WEATHER_ICONS:
			with open("EXCEPTIONS.txt", "a") as exception_file:
				exception_file.write("Unknown weather description: %s" % (self.condition))
			return Image.open(WEATHER_PATH+"/error.jpg")
		else: self.icon = Image.open(WEATHER_PATH+WEATHER_ICONS[self.condition])


	def decode_request(self, request_json=None):
		self.current_temp = (request_json["main"]["temp"] if request_json else 0) - 273
		self.high = (request_json["main"]["temp_max"] if request_json else 0) - 273
		self.low = (request_json["main"]["temp_min"] if request_json else 0) - 273
		self.city = request_json["name"] if request_json else "Error"
		self.condition = request_json["weather"][0]["description"] if request_json else "error"
		self.create_icon()


	def request(self):
		address = "http://api.openweathermap.org/data/2.5/weather?zip=%d&appid=%s" \
			% (self.zip_code, self.API_key)
		return requests.get(address).json()


	def end(self):
		self.has_not_ended = False


	def sleep(self, sleep_until_time):
		if type(sleep_until_time) == int():
			self.sleep_until_time = datetime.now() + timedelta(seconds=sleep_until_time)
		elif type(sleep_until_time) == type(self.sleep_until_time):
			self.sleep_until_time = sleep_until_time


	def start(self):
		self.thread.start()


	def thread_loop(self):
		while self.has_not_ended:
			while datetime.now() < self.sleep_until_time: sleep(60)
			try:
				request_json = self.request()
				self.decode_request(request_json)
			except Exception as error:
				ErrorWriter.write_error(error)
				self.decode_request()
			sleep(self.wait)
