#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

##########################################################################################
#
#	created by: MPZinke
#	on 2020.03.31
#
#	DESCRIPTION:	Main Loop for running Waveshare 5x7in EPaper Display.  This is meant to run on a 
#		Raspberry Pi.
#		Creates objects imported for Time, Google Calendar, Weather, and checking who is home (Android 
#		only).  Then it creates an image for the display using CreateImage functions.  The image is then written
#		to the E-paper display using Waveshare's EPD7x5 Library. 
#		Google Calendar API permissions must be enabled
#	BUGS:
#	FUTURE:	- Add inside temperature API integration
#
##########################################################################################

from copy import deepcopy
from datetime import datetime, date, time
from threading import Thread
from time import sleep

from Definitions import *

import CreateImage
import CustomTime
import ErrorWriter
import EPD7x5
import GoogleCalendar
import HueRoom
import Weather
import WhoIsHome


def create_ip_checkers():
	all_ip_checkers = []
	for ip_user in IP_USERS:
		all_ip_checkers.append(WhoIsHome.IPChecker(	ip_user["IP"], ip_user["image"],
																ip_user["name"], ip_user["wait"]))
	return all_ip_checkers


# calculate screen time to sleep: either 5 minutes or 30 based on time of day
# if it is 12 AM to 6 AM, threads will be put to sleep until 6 AM
def sleep_display_and_threads(threaded_objects):
	now = datetime.now()
	now = datetime.combine(date.min, time(now.hour, now.minute, now.second))
	time_to_next_5_minutes =  (int((now.minute / 5) + 1) * 5 - now.minute - 1) * 60 + 60 - now.second

	# if it is before 6 AM: sleep display for 30 minute increment
	if now < datetime.combine(date.min, time(6)):
		# sleep threads until 6 AM
		seconds_to_6AM = (datetime.combine(date.min, time(6)) - now).total_seconds()
		for x in range(len(threaded_objects)): threaded_objects[x].sleep(seconds_to_6AM)

		# sleep display for 30 minute intervals
		if now.minute < 30: difference = datetime.combine(date.min, time(now.hour, 30)) - now
		else: difference = datetime.combine(date.min, time(now.hour + 1)) - now
		sleep(int(difference.total_seconds()))

	# tell display to update by end of this 5 minute interval
	elif time_to_next_5_minutes - 24 >= 2: sleep(time_to_next_5_minutes - 25)


# main loop to pull data from objects, create image & write to screen
# if user is home the screen will update at a constant 5 minute (30 minute from 12 AM to 6 AM) interval
# if user is NOT home, screen will not update & will sleep objects (except user home object) for 30 minutes 
def update_screen_loop(ip_checkers, calendar, current_time, hue_room, weather):
	display = EPD7x5.setup_display()
	user_ip_checker = ip_checkers[0]
	all_objects = ip_checkers + [calendar, weather]
	while True:
		# print("Writing to screen...", end="")  #TESTING
		print(datetime.now())
		if hue_room.check_if_any_light_is_on():  # check that room is in use (lights are on)
			image = CreateImage.create_image(ip_checkers, calendar.events, current_time, weather)
			display.display_frame(display.get_frame_buffer(image))
			sleep_display_and_threads(all_objects)

		# user not home, so why change display
		else: 
			while not hue_room.check_if_any_light_is_on():
				for x in range(1, len(all_objects)): all_objects[x].sleep(30)
				sleep(30)
		# print("DONE", end="\t")  #TESTING
		print(datetime.now())


# main guarded by try-catch blocks in a loop to keep running on failure
# creates objects, then starts the threads they manage
# waits 4 seconds for objects to collect data
# begins display update loop (write data out to E-Paper screen)
def main():
	while True:
		try:
			# ———— CREATE OBJECTS ————
			# print("Creating Objects...", end="")  #TESTING
			calendar = GoogleCalendar.GoogleCalendar(
												CREDENTIAL_PATH, PICKLE_PATH, 
												SCOPES, 600)
			current_time = CustomTime.CurrentTime(24)
			ip_checkers = create_ip_checkers()
			hue_room = HueRoom.HueRoom(HUE_LIGHTS)
			weather = Weather.Weather(API_key, 76133, 600)
			# print("DONE")  #TESTING

			# ———— START OBJECT THREADS ————
			# print("Starting threaded programs...", end="")  #TESTING
			calendar.start()
			current_time.start()
			weather.start()
			for x in range(len(ip_checkers)): ip_checkers[x].start()
			# print("DONE")  #TESTING

			sleep(4)  # give objects time to retreive data
			update_screen_loop(ip_checkers, calendar, current_time, hue_room, weather)

		except Exception as error:
			try: ErrorWriter.write_error(error)
			except: print("BAD")
		sleep(2)



if __name__ == "__main__":
	main()
