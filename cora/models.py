from typing import Any, Dict, List, Optional, Text

from cora.utils import convert_model_to_snake_case


class Symptom:
    def __init__(
            self,
            name: Optional[Text] = None,
            start_date: Optional[int] = None,
            end_date: Optional[int] = None,
            severity: Optional[int] = None,
            description: Optional[Text] = None,
    ):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.severity = severity
        self.description = description

    def to_dynamo_model(self) -> Dict[Text, Any]:
        model = {"name": self.name,
                 "startDate": int(0 if self.start_date is None else self.start_date),
                 "endDate": int(0 if self.end_date is None else self.end_date),
                 "severity": int(0 if self.severity is None else self.severity),
                 "description": self.description
                 }

        return {k: v for k, v in model.items() if v is not None and v != ""}

    def load_from_model(self, m: Dict[Text, Any]):
        for k, v in convert_model_to_snake_case(m).items():
            setattr(self, k, v)
        return self


class UserRecord:
    def __init__(
            self,
            user_id: Optional[Text] = None,
            timestamp: Optional[int] = None,
            phone_number: Optional[Text] = None,
            age: Optional[int] = None,
            zip_code: Optional[Text] = None,
            dob: Optional[int] = None,
            gender: Optional[Text] = None,
            health_condition: Optional[bool] = None,
            international_travel: Optional[bool] = None,
            covid_contact: Optional[bool] = None,
            symptoms: Optional[List[Symptom]] = None,
    ):
        self.user_id = user_id
        self.timestamp = timestamp
        self.phone_number = phone_number
        self.age = age
        self.zip_code = zip_code
        self.dob = dob
        self.gender = gender
        self.health_condition = health_condition
        self.international_travel = international_travel
        self.covid_contact = covid_contact
        self.symptoms = symptoms

        if symptoms is None:
            self.symptoms = []

    def to_dynamo_model(self) -> Dict[Text, Any]:
        model = {"userId": self.user_id,
                 "timestamp": int(0 if self.timestamp is None else self.timestamp),
                 "phoneNumber": self.phone_number,
                 "age": int(0 if self.age is None else self.age),
                 "zipCode": self.zip_code,
                 "dob": int(0 if self.dob is None else self.dob),
                 "gender": self.gender,
                 "healthCondition": self.health_condition,
                 "internationalTravel": self.international_travel,
                 "covidContact": self.covid_contact,
                 "symptoms": [symptom.to_dynamo_model() for symptom in self.symptoms]
                 }

        return {k: v for k, v in model.items() if v is not None and v != ""}

    def load_from_model(self, m: Dict[Text, Any]):
        for k, v in convert_model_to_snake_case(m).items():
            if k == "symptoms":
                v = [Symptom().load_from_model(symptom) for symptom in v]
            setattr(self, k, v)
        return self

    def most_severe_symptom(self) -> Symptom:
        return max(self.symptoms, key=lambda s: s.severity)

    def symptoms_by_severity(self) -> List[Symptom]:
        return sorted(self.symptoms, key=lambda s: s.severity, reverse=True)
