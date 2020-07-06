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


class EVENT:
	def __init__(self, dictionary):
		self.summary = ""  # name of event
		self.location = ""  # address of event
		self.description = ""  # description/notes of event
		# time
		self.start = ""  # start of event in datetime
		self.start_text = ""
		self.end = ""  # end of event in datetime
		self.end_text = ""
		self.day = ""  # day of week (Today, Tomorrow, Monday, etc) of event

		self.creator = ""  # person who instatiated event
		self.dictionary = dictionary  # main argument passed for event creation
		self.set_attributes_from_dictionary()


	def set_attributes_from_dictionary(self):
		if "summary" not in self.dictionary:
			raise Exception("Entry #%s does not have a title" % (self.dictionary["etag"]))
		else: self.summary = self.dictionary["summary"]

		for attr in ("location", "creator", "description"):
			if attr in self.dictionary:
				setattr(self, attr, self.dictionary[attr])

		# time
		for attr in ("start", "end"):
			setattr(self, attr, datetime.strptime(	self.dictionary[attr]["dateTime"][:19], 
													"%Y-%m-%dT%H:%M:%S"))
		for attr in ("start", "end"):
			setattr(self, attr+"_text", str(getattr(self, attr))[:19])
		self.day = self.day_of_week()


	def day_of_week(self):
		day_difference = (self.start.date() - datetime.today().date()).days
		if not day_difference: return "Today"
		elif day_difference == 1: return "Tomorrow"
		return "On " + self.start.strftime("%a")

