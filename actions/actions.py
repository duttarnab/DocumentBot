# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, SlotSet

import json
class ActionCarousel(Action):
    def name(self) -> Text:
        return "action_carousels"
    
    def run(self, dispatcher, tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        
        with open('topics.json') as topicsFile:
            parsedTopics = json.load(topicsFile)

        chunkedTopics = divide_array(parsedTopics['topics'])
        
        elements = []
        for chunk in chunkedTopics:
            buttonJson = {}
            buttonJson['title'] = "Contents"
            buttonJson['subtitle'] = "-------------"
            buttonJson['image_url'] = "https://res.cloudinary.com/hamharry/image/upload/v1656079882/loader_w8ptw0.gif"
            buttonJson['buttons'] = chunk
            
            elements.append(buttonJson)

        message = {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": elements
                }
        }
        dispatcher.utter_message(attachment=message)
        return []

class ActionButtonClick(Action):
    def name(self):
        return "action_button_click"

    def run(self, dispatcher, tracker, domain):
        # Get the value of the button clicked
        print("Inside ActionButtonClick")
        payload = tracker.latest_message["text"]
        if payload == None:
            return []
        
        payload = payload.replace("/content_selection", "")

        payload_object = json.loads(payload)

        print(payload_object["selected_content"])

        # Set the value as a slot
        return [SlotSet("selected_content", payload_object["selected_content"])]

class ActionGetSystemRequirement(Action):
    def name(self):
        return "action_system_requirements"

    def run(self, dispatcher, tracker, domain):
        """Sets the system requirement of Gluu server"""
        print("Inside ActionGetSystemRequirement")
        entities = tracker.latest_message["entities"]

        with open('data.json') as dataFile:
            parsedData = json.load(dataFile)

        result = list(map(lambda x: {"entity": x["entity"].lower(), "value": x["value"].lower()}, entities))  
        
        # get selected button from slots
        selected_content = tracker.get_slot('selected_content')

        matchingObjects = get_matching_objects(parsedData[selected_content], result)

        print(matchingObjects)

        if not matchingObjects or len(matchingObjects) == 0:
            dispatcher.utter_message(text="I did not got that. Try to rephrase.")
            return []

        dispatcher.utter_message(text=matchingObjects[0]['response'])
        return []



def get_matching_objects(array, input_entities):
    matching_objects = []
    for obj in array:
        for entity in obj["data"]:
            if entity in input_entities:
                matching_objects.append(obj)
                break
    matching_objects.sort(key=lambda x: len([e for e in input_entities if e in x["data"]]), reverse=True)
    return matching_objects

def divide_array(arr):
    result = []
    sub_array = []
    for i, element in enumerate(arr):
        sub_array.append(element)
        if (i + 1) % 4 == 0:
            result.append(sub_array)
            sub_array = []
    if len(sub_array) > 0:
        result.append(sub_array)
    return result