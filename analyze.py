import json
import requests
from math import floor
from tqdm import tqdm
import pandas as pd
from typing import Any, Dict, List, Text
from collections import defaultdict
from cora.dynamo import DynamoDbClient


class Form:

    def __init__(self, user_id, date):
        self.user_id = user_id
        self.date = floor(float(date))

    def __str__(self):
        string = ""
        attrs = vars(self)
        user_id = attrs.pop("user_id")
        date = attrs.pop("date")
        for prop, val in attrs.items():
            string += f'{user_id},{date},{prop},{val}\n'

        return string


class LikertResponseForm(Form):

    def __init__(self, user_id: Text, date: float, anxiety: int, satisfaction: int, worthwhile: int, happy: int):

        super().__init__(user_id, date)

        try:
            self.anxiety = int(anxiety)
        except ValueError:
            self.anxiety = -1
        try:
            self.satisfaction = int(satisfaction)
        except ValueError:
            self.satisfaction = -1
        try:
            self.worthwhile = int(worthwhile)
        except ValueError:
            self.worthwhile = -1
        try:
            self.happy = int(happy)
        except ValueError:
            self.happy = -1


class ShortResponseForm(Form):
    def __init__(self, user_id: Text, date: float, sr_hope: Text, sr_anxiety: Text):
        super().__init__(user_id, date)
        self.sr_hope = sr_hope
        self.sr_anxiety = sr_anxiety


class ReflectionForm(Form):
    def __init__(self, user_id: Text, date: float, sr_solutions: Text, sr_barriers: Text, sr_overcome_barriers: Text):
        super().__init__(user_id, date)
        self.sr_solutions = sr_solutions
        self.sr_barriers = sr_barriers
        self.sr_overcome_barriers = sr_overcome_barriers


def read_data(table_name: Text = "Surveys", cache=False) -> List[Dict[Text, Any]]:
    ddb = DynamoDbClient()
    return ddb.scan_all(table_name, cache=cache)


def parse_example(ex: Dict[Text, Any]):
    answers = {k: v["S"] for k, v in ex["answers"]["M"].items()}
    if "happy" in answers:
        return LikertResponseForm(user_id=ex["userId"]["S"], date=ex["date"]["N"], **answers)
    elif "sr_hope" in answers:
        return ShortResponseForm(user_id=ex["userId"]["S"], date=ex["date"]["N"], **answers)
    else:
        return ReflectionForm(user_id=ex["userId"]["S"], date=ex["date"]["N"], **answers)


def process_events(events: List[Text], path: Text):
    with open(path, "w") as f:
        for event in tqdm(events):
            f.write(f"Utterance: {event}\n\n")
            res = requests.post("https://cocobot.ngrok.io/?utterance=%s".format(event.replace(" ", "+")))
            d = res.json()

            for idx, task in enumerate(d["tasks"]):
                f.write(f"{idx + 1}. {task['question']}\n")
                for c in task["candidates"]:
                    f.write(f"\t[ ] {c}\n")

            f.write("===================================================\n\n")


def process_events_to_csv(events: List[Text], path: Text, context: Text, append: bool = False, format="json", min_len=0):
    if append:
        mode = "a"
    else:
        mode = "w"

    with open(path, mode) as f:
        for event in tqdm(sorted(events, key=lambda e: len(e), reverse=True)):
            e = event.replace('"', '')
            if len(e.split()) < min_len:
                continue

            if format != "json":
                f.write(f"{e}\n")
            else:
                f.write(json.dumps({"context": context, "text": e}) + "\n")


def get_examples_by_user(examples: List[Form]):
    examples_by_user = defaultdict(list)
    for ex in examples:
        examples_by_user[ex.user_id].append(ex)

    return {k: sorted(v, key=lambda x: x.date) for k, v in examples_by_user.items()}


if __name__ == "__main__":
    import re
    import json
    from datetime import datetime
    from collections import Counter
    from matplotlib import pyplot as plt

    pd.set_option('display.max_colwidth', None)

    examples = read_data(cache=True)
    instances = [parse_example(ex) for ex in examples]
    dates = [r.date for r in instances if isinstance(r, ShortResponseForm)]
    hope_events = [r.sr_hope for r in instances if isinstance(r, ShortResponseForm)]
    anxiety_events = [r.sr_anxiety for r in instances if isinstance(r, ShortResponseForm)]
    overcoming_events = [r.sr_overcome_barriers for r in instances if isinstance(r, ReflectionForm)]
    solution_events = [r.sr_solutions for r in instances if isinstance(r, ReflectionForm)]
    barrier_events = [r.sr_barriers for r in instances if isinstance(r, ReflectionForm)]

    examples_by_user = get_examples_by_user(instances)
    with open("data_by_user.csv", "w") as f:
        for user, examples in examples_by_user.items():
            for ex in examples:
                f.write(str(ex))
