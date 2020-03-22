from cora.models import UserRecord, Symptom
from cora.responses import UserRecordResponse


def test_most_recent_record():
    most_recent = UserRecordResponse("test_user", [UserRecord(timestamp=1584818778),
                                                   UserRecord(timestamp=1584810778),
                                                   UserRecord(timestamp=1584918778)]).most_recent()

    assert(most_recent.timestamp == 1584918778)


def test_most_severe_symptom():
    most_severe_symptom = UserRecord(symptoms=[Symptom(severity=3),
                                               Symptom(severity=9),
                                               Symptom(severity=0)]).most_severe_symptom()

    assert(most_severe_symptom.severity == 9)


def test_symptom_severity():
    symptoms_by_severity = UserRecord(symptoms=[Symptom(severity=3),
                                                Symptom(severity=9),
                                                Symptom(severity=0)]).symptoms_by_severity()

    assert(symptoms_by_severity[0].severity == 9)
    assert(symptoms_by_severity[1].severity == 3)
    assert(symptoms_by_severity[2].severity == 0)
