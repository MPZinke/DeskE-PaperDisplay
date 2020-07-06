#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

##########################################################################################
#
#	created by: MPZinke
#	on 2020.04.05
#
#	DESCRIPTION:	
#	BUGS:
#	FUTURE:	- Expand such that each light is its own object
#
##########################################################################################


from datetime import datetime, timedelta
from requests import get
from time import sleep
from threading import Thread

from Definitions import *


class HueRoom:
	def __init__(self, lights, wait=300):
		self.lights = lights
		self.any_light_is_on = False

		self.has_not_ended = True
		self.sleep_until_time = datetime.now()
		self.thread = Thread(target=self.thread_loop)
		self.wait = wait


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
			while datetime.now() < self.sleep_until_time: sleep(30)
			try:
				request_json = self.request()
				self.decode_request(request_json)
			except Exception as error:
				print(error)
				self.decode_request()
			sleep(self.wait)


	def check_connection(self):
		url = "http://%s/api/%s/lights" % (BRIDGE_IP_ADDRESS, USER_NAME)
		request = get(url=url).json()
		return request



	def check_if_any_light_is_on(self):
		for light in self.lights:
			if self.light_is_on(light): return True
		return False


	def light_is_on(self, light):
		url = "http://%s/api/%s/lights/%d" % (BRIDGE_IP_ADDRESS, USER_NAME, light)
		request = get(url=url).json()
		if "state" in request and request["state"]["reachable"] and request["state"]["on"]:
			return True
		return False
