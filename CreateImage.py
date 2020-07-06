#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

##########################################################################################
#
#	created by: MPZinke
#	on 2020.03.31
#
#	DESCRIPTION:	Uses PIL to create an image.  This will be based off of the objects passed.  For reference
#		see test.png.
#	BUGS:
#	FUTURE:
#
##########################################################################################


from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from platform import system
from datetime import datetime

from Definitions import *
import ErrorWriter


# main function call to create image for displaying.
# if image name passed, function also saves a PNG to the local directory
def create_image(all_ip_checkers, calendar_event_list, time, weather, output_image_name=None):
	image = Image.new('1', (WIDTH, HEIGHT), 1)  # 1: clear the frame
	draw = ImageDraw.Draw(image)
	draw.rectangle((0, 0, WIDTH, HEIGHT), fill=255)

	add_people_home(draw, image, all_ip_checkers)
	add_time(draw, time)
	add_calendar_event_list(draw, calendar_event_list)
	add_weather(draw, image, weather)
	add_inside_temperature(draw, 0)

	if output_image_name: image.save("%s.png" % (output_image_name), "PNG")
	return image.rotate(180)


# —————————————————— PARTS ———————————————————

# goes through list of EVENT objects and pulls relevent data to write to image
def add_calendar_event_list(draw, calendar_event_list):
	for x in range(min(len(calendar_event_list), 8)):
		text_fill = 255*((x+1)%2)
		# rectangle
		draw.rectangle((350, x*48, 640, x*48+47), fill=not text_fill)
		# summary
		draw.text((355, x*48+5), calendar_event_list[x].summary[:25], font=FONT16, fill=text_fill)
		draw.text((355, x*48+25), calendar_event_list[x].day, font=FONT16, fill=text_fill)  # day

		if calendar_event_list[x].start < datetime.now(): start = "Now"
		else: start = str(calendar_event_list[x].start.time().strftime("%-I:%M %p"))
		draw.text((550, x*48+5), start, font=FONT16, fill=text_fill)

		draw.text((550, x*48+25), str(calendar_event_list[x].end.time().strftime("%-I:%M %p")), font=FONT16, fill=text_fill)


# compiles a list of people who are home from all_ip_checkers; creates an icon from first letter of their name
def add_people_home(draw, image, all_ip_checkers):
	helvetica_font = ImageFont.truetype("/home/pi/EPaperDisplay/Dependencies/Helvetica_Bold.ttf", 36)
	ips_that_are_home = [all_ip_checkers[x] for x in range(len(all_ip_checkers)) if all_ip_checkers[x].is_home]
	for x in range(len(ips_that_are_home)):
		x_position = 5 + x * 50
		name_char = ips_that_are_home[x].name[0]
		draw.ellipse((x_position, 215, x_position + 40, 255), fill=0)
		text_x_pos = x_position + 20 - draw.textsize(name_char, font=helvetica_font)[0] / 2
		draw.text((text_x_pos, 220), name_char, fill=255, font=helvetica_font)


def add_time(draw, time):
	# top left: TIME & DATE
	width, height = draw.textsize(time.now, font=FONT42)
	draw.text((int(165-width/2), 75), time.now, font=FONT44, fill=0)

	width, height = draw.textsize(time.day.upper()+" "+time.date, font=FONT20)
	draw.text((int(165-width/2), 125), time.day.upper()+" "+time.date, font=FONT20, fill=0)


def add_weather(draw, image, weather):
	draw.rectangle((0, 259, 345, 384), fill=0)
	# ———— CURRENT WEATHER ————
	current_temp_width = draw.textsize("%.1f°C" % (weather.current_temp), font=FONT40)[0]
	current_condition_width = draw.textsize(weather.condition, font=FONT16)[0]
	max_width = max(current_temp_width, current_condition_width)
	text_middle = int(80 + (max_width / 2))

	image.paste(weather.icon, (5, 266))  # const size of 67
	draw.text((int(text_middle - current_temp_width / 2), 271), "%.1f°C" % (weather.current_temp), font=FONT40, fill=255)
	draw.text((int(text_middle - current_condition_width / 2), 312), weather.condition, font=FONT16, fill=255)

	# ———— LOW & HIGH ————
	draw.line((max_width + 90, 264, max_width + 90, 335), fill=255)  # current temp underlining bar
	draw.text((max_width + 100, 279), "MAX %.1f°C" % (weather.high), font=FONT16, fill=255)
	draw.text((max_width + 100, 306), "MIN %.1f°C" % (weather.low), font=FONT16, fill=255)


# ———— INSIDE THERMOMETER TEMPERATURE ————
def add_inside_temperature(draw, inside_temp):
	temperature_string = "Currently %d°C Inside" % (inside_temp)
	text_start = (340 - draw.textsize(temperature_string, font=FONT24)[0]) / 2 + 5 
	draw.text((text_start, 350), temperature_string, font=FONT24, fill=255)
