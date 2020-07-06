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
from os import devnull
import subprocess
from threading import Thread
from time import sleep

import ErrorWriter


class IPChecker:
	def __init__(self, IP, image, name, wait=30):  # IP address of device, name of device, time between checks
		self.IP = IP
		self.user_image = image
		self.name = name
		self.wait = wait

		self.is_home = False

		self.has_not_ended = True
		self.sleep_until_time = datetime.now()
		self.thread = Thread(target=self.thread_loop)


	def device_is_on_network(self):
		with open(devnull, 'w') as FNULL:
			return subprocess.call(["ping", "-c", "1", "-w", "1", self.IP], stdout=FNULL) == 0


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
			while datetime.now() < self.sleep_until_time: sleep(15)
			try: self.is_home = self.device_is_on_network()
			except Exception as error: ErrorWriter.write_error(error)
			sleep(self.wait)
