#  (for the sanity of the code)
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
# for debugging
import logging
# for creating the webhook
from flask import Flask, Response, Blueprint, request, jsonify
# for creating the custom connector
from rasa.core.channels.channel import UserMessage, OutputChannel
from rasa.core.channels.channel import InputChannel
from rasa.core.channels.channel import CollectingOutputChannel
import json

logger = logging.getLogger(__name__)


class GoogleConnector(InputChannel):

	@classmethod
	def name(cls):
		return 'google_assistant'

	# This function will define the webhook that Google Assistant will use to 
	# pass the user inputs to Rasa Core, 
	# collect the responses and send them back to Google Assistant 
	def blueprint(self, on_new_message):
		# initialising the webhook name
		google_webhook = Blueprint('google_webhook', __name__)

		# define the routes of your webhook: 2 routes
		# health route for the endpoint ‘/’ and a receive route for the endpoint ‘/webhook’

		# health route: 
		# receive GET requests sent by Google Assistant and will return 200 OK message confirming that the connection works well
		@google_webhook.route("/", methods=['GET'])
		def health():
			return jsonify({"status": "ok"})


		@google_webhook.route("/webhook", methods=['POST'])
		def receive():
			payload = json.loads(request.data)		
			sender_id = payload['user']['userId']
			intent = payload['inputs'][0]['intent'] 			
			text = payload['inputs'][0]['rawInputs'][0]['query'] 		
			if intent == 'actions.intent.MAIN':	
				message = "<speak>Hello! <break time=\"1\"/> Welcome to the Rasa-powered Google Assistant skill. You can start by saying hi."			 
			else:
				out = CollectingOutputChannel()			
				on_new_message(UserMessage(text, out, sender_id))
				responses = [m["text"] for m in out.messages]
				message = responses[0]	
			r = json.dumps(
				{
				  "conversationToken": "{\"state\":null,\"data\":{}}",
				  "expectUserResponse": 'true',
				  "expectedInputs": [
					{
					  "inputPrompt": {
					  "initialPrompts": [
						{
						  "ssml": message
						}
					  ]
					 },
					"possibleIntents": [
					 {
					  "intent": "actions.intent.TEXT"
					 }
					]
				   }
				  ]
				 })
			return r
		return google_webhook