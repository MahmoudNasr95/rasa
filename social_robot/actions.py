# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import datetime
import requests
import mysql.connector


# Initialization for mysql database for medication
# mydb = mysql.connector.connect(host = '10.42.0.174', port='8080', user = 'pami',passwd = 'pamiuser', database = 'myAlexa')
# mycursor = mydb.cursor()
# print(mydb)

def organize_entities(tracker):
	# this function takes the tracker and organizes all extracted entities into a dictionary with their type and value
	entities = dict()
	prediction = tracker.latest_message
	if prediction['entities']:
		for ent in prediction['entities']:
			ent_name = ent['entity']
			ent_value = ent['value']

			entities.update({ent_name:ent_value})
	return entities


# test action from RASA (use as template)
class ActionHelloWorld(Action):

	def name(self) -> Text:
		return "action_hello_world"

	def run(self, dispatcher: CollectingDispatcher,
			tracker: Tracker,
			domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

		dispatcher.utter_message("Hello World!")

		return []

# action to retrieve medication name and time to send to db
class ActionGetMedName(Action):
	def name(self) -> Text:
		return "action_get_med"

	def run(self, dispatcher: CollectingDispatcher,
			tracker: Tracker,
			domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

		dict0 = {"Medication": None, "Day": None, "Time":None}
		entities = organize_entities(tracker)
		msg = "Ok I will remind you"
		if "med_name" in entities.keys():
			dict0["Medication"] = entities["med_name"]
			msg = msg + ' of ' + entities["med_name"]
		else:
			dict0["Medication"] = "unknown"
		
		if "DATE" in entities.keys():
			dict0["Day"] = entities["DATE"]
			msg = msg + ' on ' + entities["DATE"]
		else:
			currentDT = datetime.datetime.now()
			dict0["Day"] = currentDT.strftime("%A")
			msg = msg + ' on ' + currentDT.strftime("%A")

		if "TIME" in entities.keys():
			dict0["Time"] = entities["TIME"]
			msg = msg + ' at ' + entities["TIME"]
		else:
			dict0["Time"] = "unknown"

		dispatcher.utter_message(msg)
		# print all recovered entities
		print_ent = 0
		if print_ent:
			entities = organize_entities(tracker)
			if any(entities):
				dispatcher.utter_message("I got the following entities:")
				for x in entities:
					dispatcher.utter_message("%s with a value of %s" %(x,entities[x]))
			else:
				dispatcher.utter_message("I could not extract any entities")
		return []


# action to respond to movement commands for robot from user
class ActionMove(Action):

	def name(self) -> Text:
		return "action_move"

	def run(self, dispatcher: CollectingDispatcher,
			tracker: Tracker,
			domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

		# retrieve entities
		entities = organize_entities(tracker)
		if any(entities):
			# 'go forward 1 meter'
			# go forward
			# go 1 meter
			# go
			msg = entities["move_type"]
			if "direction" in entities.keys():
				msg = msg + ' ' + entities["direction"]
			if "number" in entities.keys():
				msg = msg + ' ' + entities["number"]

			data = {'value': msg}
			url = 'https://93a4a1e3.ngrok.io/postjson'
			requests.post(url,data)
		else:
			dispatcher.utter_message('Something went wrong with my action.')

		dispatcher.utter_message(msg)
		return []
	

