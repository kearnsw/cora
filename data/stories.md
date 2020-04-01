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
* affirm
    - utter_new_symptoms
* deny
    - followup_form
    - form{"name": "followup_form"}
    - form{"name": null}
    - utter_how_are_you
> check_how_are_you

## new symptoms
* greet
    - utter_greet
* affirm
    - utter_new_symptoms
* inform
    - action_add_symptom
    - utter_other_new_symptoms
* deny
    - followup_form
    - form{"name": "followup_form"}
    - form{"name": null}
    - utter_how_are_you
> check_how_are_you

## new symptoms affirm first
* greet
    - utter_greet
* affirm
    - utter_new_symptoms
* affirm
    - utter_ask_new_symptoms
* inform
    - action_add_symptom
    - utter_other_new_symptoms
* deny
    - followup_form
    - form{"name": "followup_form"}
    - form{"name": null}
    - utter_how_are_you
> check_how_are_you

## story_version
* version
  - utter_version
  - action_version
  
## triage
* request_triage
    - triage_form
    - form{"name": "triage_form"}
    - form{"name": null}

## stressed
> check_how_are_you
* stressed
    - utter_stress_suggestion
    - utter_try_suggestion
> check_try_suggestion

## schedule check-in
> check_try_suggestion
* affirm
    - utter_thank_you
    - utter_check_in_reminder

## insomnia
> check_how_are_you
* need_sleep
    - utter_sleep_suggestion
    - utter_try_suggestion
> check_try_suggestion

## worry
> check_how_are_you
* worried
    - utter_worry_suggestion
    - utter_try_suggestion
> check_try_suggestion
    
## social isolation
> check_how_are_you
* social_isolation
    - utter_social_isolation_suggestion
    - utter_try_suggestion
> check_try_suggestion

## financial stress
> check_how_are_you
* financial_stress
    - utter_financial_stress_suggestion
    - utter_try_suggestion
> check_try_suggestion