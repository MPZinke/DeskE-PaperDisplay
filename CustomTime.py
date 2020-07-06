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


from datetime import datetime, timedelta
from time import sleep
from threading import Thread

from Definitions import *
import ErrorWriter


class CurrentTime:
	def __init__(self, lead=0):
		self.lead = lead
		self.now = self.time_string()
		self.day = self.day_string()
		self.date = self.date_string()

		self.has_not_ended = True
		self.sleep_until_time = datetime.now()
		self.thread = Thread(target=self.thread_loop)


	def day_string(self):
		return datetime.today().strftime("%a")


	def date_string(self):
		return datetime.today().strftime("%b %-d, %Y")


	def time_string(self):
		return (datetime.now() + timedelta(minutes=1) + timedelta(seconds=self.lead)).strftime("%-I:%M %p")


	def end(self):
		self.has_not_ended = False


	def start(self):
		self.thread.start()


	def sleep(self, sleep_until_time):
		if type(sleep_until_time) == int():
			self.sleep_until_time = datetime.now() + timedelta(seconds=sleep_until_time)
		elif type(sleep_until_time) == type(self.sleep_until_time):
			self.sleep_until_time = sleep_until_time


	def thread_loop(self):
		while self.has_not_ended:
			while datetime.now() < self.sleep_until_time: sleep(60)
			try:
				self.now = self.time_string()
				self.day = self.day_string()
				self.date = self.date_string()
			except Exception as error:
				ErrorWriter.write_error(error)
				self.now = "ERROR"
				self.day = "ERROR"
				self.date = "ERROR"

			sleep(59)
