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
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from time import sleep
from threading import Thread

from Definitions import *
import ErrorWriter
from Event import EVENT


class GoogleCalendar:
	def __init__(self, credential_file, pickle_file, scopes, wait=300):
		if not os.path.exists(pickle_file):
			creds = InstalledAppFlow.from_client_secrets_file(credential_file, scopes).run_local_server(port=0)
			with open(pickle_file, 'wb') as token:
				pickle.dump(creds, token)
			raise Exception("No .pickle file")

		self.has_not_ended = True
		self.sleep_until_time = datetime.now()
		self.thread = Thread(target=self.thread_loop)
		self.wait = wait

		self.events = []
		self.credential_file = credential_file
		self.pickle_file = pickle_file
		self.scopes = scopes

		self.build = None
		self.creds = None
		with open(self.pickle_file, "rb") as token:
			self.creds = pickle.load(token)
		self.revalidate_credentials()


	def end(self):
		self.has_not_ended = False


	def query(self):
		now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
		events_result = self.build.events().list(
													calendarId='primary', timeMin=now,
													timeMax=(datetime.today() + timedelta(weeks=1)).isoformat() + 'Z',
													maxResults=10, singleEvents=True,
													orderBy='startTime'
												).execute()
		return events_result.get('items', [])


	def revalidate_credentials(self):
		if not self.creds.valid:
			if self.creds.expired and self.creds.refresh_token: self.creds.refresh(Request())
			else: self.creds = InstalledAppFlow.from_client_secrets_file(self.credential_file, self.scopes).run_local_server(port=0)

			with open(self.pickle_file, "wb") as token:
				pickle.dump(self.creds, token)

		self.build = build("calendar", "v3", credentials=self.creds)


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
				if not self.creds.valid or self.creds.expired or self.creds.refresh_token:
					self.revalidate_credentials()
				result_json = self.query()
				self.events = [EVENT(value) for value in result_json]
			except Exception as error:
				ErrorWriter.write_error(error)
				self.events = []
			sleep(self.wait)
