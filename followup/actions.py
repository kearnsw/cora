from typing import Dict, Text, Any, List, Union

from rasa_sdk import Tracker, Action
from rasa_sdk.events import EventType, SlotSet, SessionStarted, ActionExecuted
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction


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

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any], **kwargs) -> List[EventType]:

        # the session should begin with a `session_started` event
        events = [SessionStarted()]

        # any slots that should be carried over should come after the
        # `session_started` event
        events.extend(self.fetch_slots(tracker))

        # an `action_listen` should be added at the end as a user message follows
        events.append(ActionExecuted("action_listen"))

        return events


class CoronaScreeningForm(FormAction):
    """Example of a custom form action"""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "screening_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return ["relation", "age", "fever", "coughing", "contact"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "relation": [
                self.from_entity(entity="relation"),
            ],
            "age": [
                self.from_entity(entity="age"),
            ],
            "fever": [
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False)
            ],
            "cough": [
                self.from_entity(entity="viscosity"),
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False)
            ],
            "contact": [
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False)
            ]
        }

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""

        # utter submit template
        dispatcher.utter_message(template="utter_submit")
        return []


class Empathize(Action):

    def name(self) -> Text:
        return "action_empathize"

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any], **kwargs) -> List[Dict[Text, Any]]:
        sensitive_keywords = ["died", "dies", "dying", "sick"]
        mood = tracker.get_slot('state')
        print("Recieved: {}".format(tracker.latest_message))
        dispatcher.utter_message("[empathic response]", image="https://i.imgur.com/nGF1K8f.jpg")
        return []
