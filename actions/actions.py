from requests import Response
from typing import Dict, Text, Any, List, Union, Optional
import logging
import json
import requests
import os

from overrides import overrides
from rasa_sdk import Tracker, Action
from rasa_sdk.events import ActionExecuted, AllSlotsReset, EventType, SessionStarted, SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction, REQUESTED_SLOT

from cora.api import get_user_records, put_user_record
from cora.models import Symptom, UserRecord
from cora.responses import UserRecordResponse
from cora.utils import normalize_phone_number

logger = logging.getLogger(__name__)
vers = 'Vers: 0.1.3, Date: Mar 22, 2020'
logger.info(f"Starting vers: {vers}")


class ActionSessionStart(Action):
    def name(self) -> Text:
        return "action_session_start"

    @staticmethod
    def fetch_slots(tracker: Tracker) -> List[EventType]:
        """Collect slots that contain the user's name and phone number."""

        slots = []

        for key in ("name", "phone_number"):
            value = tracker.get_slot(key)
            if value is not None:
                slots.append(SlotSet(key=key, value=value))

        return slots

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any], **kwargs) -> List[
        EventType]:

        # the session should begin with a `session_started` event
        events = [SessionStarted()]

        # any slots that should be carried over should come after the
        # `session_started` event
        events.extend(self.fetch_slots(tracker))

        # an `action_listen` should be added at the end as a user message follows
        events.append(ActionExecuted("action_listen"))

        return events


class Triage(FormAction):

    def name(self) -> Text:
        return "triage_form"

    @staticmethod
    def required_slots(tracker: "Tracker") -> List[Text]:
        baseline = ["person", "age", "cov"]
        if tracker.get_slot("cov"):
            baseline.append("cov_severity")
        return baseline

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "person": [
                self.from_entity(entity="person"),
                self.from_intent(intent="affirm", value=True)
            ],
            "age": [
                self.from_entity(entity="number")
            ],
            "contact": [
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False)
            ],
            "zip": [
                self.from_entity(entity="number")
            ],
            "at_risk": [
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False)
            ],
            "cov": [
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False)
            ],
            "cov_severity": [
                self.from_entity(entity="number"),
            ],
            "cough": [
                self.from_entity(entity="number"),
            ]
        }

    @overrides
    async def validate(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: Dict[Text, Any],
    ) -> List[EventType]:
        """Extract and validate value of requested slot.

        If nothing was extracted reject execution of the form action.
        Subclass this method to add custom validation and rejection logic
        """

        # extract other slots that were not requested
        # but set by corresponding entity or trigger intent mapping
        slot_values = self.extract_other_slots(dispatcher, tracker, domain)

        # extract requested slot
        slot_to_fill = tracker.get_slot(REQUESTED_SLOT)
        if slot_to_fill:
            slot_values.update(self.extract_requested_slot(dispatcher, tracker, domain))

            if not slot_values:
                # reject to execute the form action
                # if some slot was requested but nothing was extracted
                # it will allow other policies to predict another action
                # raise ActionExecutionRejection(
                #     self.name(),
                #     f"Failed to extract slot {slot_to_fill} with action {self.name()}",
                # )
                dispatcher.utter_message(tracker.events[-3].get('text'))
        logger.debug(f"Validating extracted slots: {slot_values}")
        return await self.validate_slots(slot_values, dispatcher, tracker, domain)

    async def submit(self, dispatcher: "CollectingDispatcher", tracker: "Tracker", domain: Dict[Text, Any]) -> List[
        EventType]:
        dispatcher.utter_message(tracker.slots)
        return [AllSlotsReset()]

    def validate_person(self,
                        value: bool,
                        dispatcher: CollectingDispatcher,
                        tracker: Tracker,
                        domain: Dict[Text, Any],
                        ) -> Dict[Text, Any]:
        """Validate symptoms by replying appropriately to changes in the symptom ratings over time."""
        if value is None:
            dispatcher.utter_message(template="utter_request_rating")
            # validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
            return {"person": None}
        elif value:
            return {"person": "self"}
        else:
            return {"person": value}

    def validate_cov_severity(self,
                          value: Text,
                          dispatcher: CollectingDispatcher,
                          tracker: Tracker,
                          domain: Dict[Text, Any]
                          ) -> Dict[Text, Any]:
        """Validate symptoms by replying appropriately to changes in the symptom ratings over time."""
        severity = int(value)
        if 0 <= severity <= 10:
            return {"cov_severity": severity}
        else:
            dispatcher.utter_message(template="utter_request_rating")
            # validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
            return {"cov_severity": None}


class FollowupForm(FormAction):
    """Example of a custom form action"""

    def name(self) -> Text:
        """Unique identifier of the form"""
        return "followup_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        logger.info("followup_form, required_slots")
        symptoms = [symptom.name.lower() for symptom in get_symptoms_by_severity(tracker.sender_id)]
        # return symptoms if len(symptoms) > 0 else []
        return ["fever", "cough"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "fever": [
                self.from_entity(entity="number"),
            ],
            "cough": [
                self.from_entity(entity="number"),
            ]
        }

    @overrides
    def request_next_slot(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: Dict[Text, Any],
    ) -> Optional[List[EventType]]:
        """Request the next slot and utter template if needed,
            else return None"""

        logger.info("Requesting slot...")
        for slot in self.required_slots(tracker):
            if self._should_request_slot(tracker, slot):
                # Check if already captured
                severity = get_symptom_severity(tracker.sender_id, slot)
                if severity is not None:
                    logger.info(f"follow up on {slot}")
                    tracker.slots["severity"] = severity
                    tracker.slots["symptom"] = slot
                    dispatcher.utter_message(template=f"utter_followup_symptom", **tracker.slots)
                else:
                    logger.info(f"first time asking {slot}")
                    dispatcher.utter_message(template=f"utter_ask_{slot}", **tracker.slots)
                return [SlotSet(REQUESTED_SLOT, slot), SlotSet("severity", severity)]

        # no more required slots to fill
        return None

    def validate_fever(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate symptoms by replying appropriately to changes in the symptom ratings over time."""
        return self.validate_symptom_severity("fever", 0, 120, value, dispatcher, tracker)

    def validate_sob(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate symptoms by replying appropriately to changes in the symptom ratings over time."""
        return self.validate_symptom_severity("sob", 0, 10, value, dispatcher, tracker)

    def validate_cough(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate symptoms by replying appropriately to changes in the symptom ratings over time."""
        return self.validate_symptom_severity("cough", 0, 10, value, dispatcher, tracker)

    def validate_symptom_severity(self,
                                  symptom_name: Text,
                                  min_value: float,
                                  max_value: float,
                                  value: Text,
                                  dispatcher: CollectingDispatcher,
                                  tracker: Tracker,
                                  ) -> Dict[Text, Any]:
        """Validate symptoms by replying appropriately to changes in the symptom ratings over time."""
        new_severity = float(value)
        if min_value <= new_severity <= max_value:
            prev_severity = get_symptom_severity(tracker.sender_id, symptom_name)

            if prev_severity is not None:
                prev_severity = float(prev_severity)

                # Condition improved
                if new_severity < prev_severity:
                    dispatcher.utter_message(template="utter_feeling_better")

                # Condition worsened
                elif new_severity > prev_severity:
                    dispatcher.utter_message(template="utter_worsening_symptom")

            return {symptom_name: value}
        else:
            dispatcher.utter_message(f"Please provide a value between {min_value} and {max_value}")
            # validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
            return {symptom_name: None}

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""

        # utter submit template
        res = update_symptoms(tracker)
        if res is not None:
            logger.info(res.status_code, res.text)
        return [AllSlotsReset()]


def update_symptoms(tracker: Tracker) -> Optional[Response]:
    """This function takes the data stored in the form and stores it for long-term use."""
    user_id = normalize_phone_number(tracker.sender_id)
    logger.info(f"Posting new record for {user_id}.")
    user_record = get_user_records(user_id).most_recent()
    symptom_frame = tracker.current_slot_values()
    updated_symptoms = []
    updates = 0
    for symptom in user_record.symptoms:
        logger.info(symptom)
        symptom_name = symptom.name.lower()
        if symptom_frame.get(symptom_name) is not None:
            symptom.severity = int(symptom_frame[symptom_name])
            symptom.description = "Follow-up Form"
            updates += 1
        updated_symptoms.append(symptom)

    if updates == 0:
        return None

    user_record.symptoms = updated_symptoms
    return put_user_record(user_record)


def get_symptoms_by_severity(sender_id: Text) -> List[Symptom]:
    logger.debug(f", get_symptoms_by_severity, sender_id: {sender_id}")
    user_id = normalize_phone_number(sender_id)
    logger.warning(f"user_id: {user_id}")
    records = get_user_records(user_id)
    logger.debug(f"records: {records}, typeof: {type(records)}")
    if records.data:
        record = records.most_recent()
        return record.symptoms_by_severity()
    else:
        return []


def get_symptom_severity(sender_id: Text, slot_name: Text) -> Optional[int]:
    user_id: Text = normalize_phone_number(sender_id)
    records: UserRecordResponse = get_user_records(user_id)
    symptom_severities: Dict[Text, int] = {symptom.name.lower(): symptom.severity for symptom in
                                           records.most_recent().symptoms}
    logger.info(slot_name, symptom_severities)
    return symptom_severities.get(slot_name)


class Suggest(Action):

    def name(self) -> Text:
        return "action_suggest"

    async def run(self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        pass


class Empathize(Action):

    def name(self) -> Text:
        return "action_empathize"

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any], **kwargs) -> List[
        Dict[Text, Any]]:
        sensitive_keywords = ["died", "dies", "dying", "sick"]
        mood = tracker.get_slot('state')
        logger.info("Recieved: {}".format(tracker.latest_message))
        dispatcher.utter_message("[empathic response]", image="https://i.imgur.com/nGF1K8f.jpg")
        return []


class UpdateSymptoms(Action):
    """
    This action retrieves slots from the user record and asks questions to follow-up.
    """

    def __init__(self):
        self.templates = {
            "ask_severity_no_value": "Last time we talked you let me know that you were experiencing {symptom}. "
                                     "How would you rate this symptom today on a scale of 1-10?",
            "ask_severity": "Last we talked you rated your {symptom} as a {severity}. "
                            "How would you rate this symptom now on a scale of 1-10?"}

    def name(self) -> Text:
        return "action_update_symptoms"

    async def run(self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        events = []

        try:
            for symptom in get_symptoms_by_severity(tracker.sender_id):
                if tracker.get_slot(symptom.name) is not None:
                    if symptom.severity is not None:
                        dispatcher.utter_message(self.templates["ask_severity"].format(symptom=symptom.name,
                                                                                       severity=symptom.severity))
                    else:
                        dispatcher.utter_message(self.templates["ask_severity_no_value"].format(symptom=symptom.name))
                    return [ActionExecuted('action_ask_' + symptom.name)]

        except AttributeError:
            return []


class AddSymptom(Action):
    """
    This action retrieves slots from the user record and asks questions to follow-up.
    """

    def __init__(self):
        self.templates = {"utter_new_symptom": "I'm sorry to hear that you've developed a {symptoms}"}

    def name(self) -> Text:
        return "action_add_symptom"

    async def run(self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        symptoms = list(tracker.get_latest_entity_values("symptom"))
        print(symptoms)
        if len(symptoms) == 1:
            symptom_string = symptoms[0]
        else:
            symptom_string = ", ".join(symptoms[:-1]) + " and " + symptoms[-1]
        dispatcher.utter_message(self.templates["utter_new_symptom"].format(symptoms=symptom_string))


        return []


class CheckSymptoms(Action):
    """
    This action retrieves slots from the user record and asks questions to follow-up.
    """

    def __init__(self):
        self.templates = {
            "ask_severity_no_value": "Last time we talked you let me know that you were experiencing {symptom}. "
                                     "How would you rate this symptom today on a scale of 1-10?",
            "ask_severity": "Last we talked you rated your {symptom} as a {severity}. "
                            "How would you rate this symptom now on a scale of 1-10?"}

    def name(self) -> Text:
        return "action_check_symptoms"

    async def run(self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        events = []

        try:
            for symptom in get_symptoms_by_severity(tracker.sender_id):
                if tracker.get_slot(symptom.name) is not None:
                    if symptom.severity is not None:
                        dispatcher.utter_message(self.templates["ask_severity"].format(symptom=symptom.name,
                                                                                       severity=symptom.severity))
                    else:
                        dispatcher.utter_message(self.templates["ask_severity_no_value"].format(symptom=symptom.name))
                    return [ActionExecuted('action_ask_' + symptom.name)]

        except AttributeError:
            return []


class ActionVersion(Action):
    def name(self):
        logger.info("ActionVersion self called")
        # define the name of the action which can then be included in training stories
        return "action_version"

    def run(self, dispatcher, tracker, domain):
        # logger.info(">>> responding with version: {}".format(vers))
        # dispatcher.utter_message(vers) #send the message back to the user
        if os.getenv('RASA_X_PROD_NGINX_SERVICE_HOST'):
            nginx_host = os.getenv('RASA_X_PROD_NGINX_SERVICE_HOST') + ':8000'
        elif os.getenv('RASA_X_1584837298_NGINX_SERVICE_HOST'):
            nginx_host = os.getenv('RASA_X_1584837298_NGINX_SERVICE_HOST') + ':8000'
        else:
            nginx_host = 'rasa-x:5002'
        try:
            # https://kubernetes.io/docs/concepts/services-networking/service/
            logger.info(f"connecting to {nginx_host}")
            request = json.loads(requests.get('http://' + nginx_host + '/api/version').text)
        except:
            request = {"rasa-x": "", "rasa": {"production": ""}}
            # request['rasa-x'] == ''
            # request['rasa']['production'] = ''
        logger.info(">> rasa x version response: {}".format(request['rasa-x']))
        logger.info(">> rasa version response: {}".format(request['rasa']['production']))
        dispatcher.utter_message(f"Action: {vers}\nRasa X: {request['rasa-x']}\nRasa:  {request['rasa']['production']}")
        return []
