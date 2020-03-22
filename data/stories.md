## scheduled followup
* start
    - utter_scheduled_greet
* affirm
    - followup_form
    - form{"name": "followup_form"}
    - form{"name": null}

## user initiated followup
* greet
    - utter_greet
* update_symptoms
    - followup_form
    - form{"name": "followup_form"}
    - form{"name": null}

## story_version
* version
  - utter_version
  - action_version
