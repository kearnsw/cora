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

    # single_file = True
    #
    # min_len = 3
    #
    # solution_prompt = "What is a possible solution to help you feel better?"
    # barrier_prompt = "What is a potential barrier to implementing this solution?"
    # overcoming_prompt = "How might you overcome this barrier?"
    # hope_prompt = "What gave you the most hope today?"
    # anxiety_prompt = "What caused you the most anxiety today?"
    #
    # if single_file:
    #     process_events_to_csv(solution_events, "all.jsonl", solution_prompt, min_len=min_len)
    #     process_events_to_csv(barrier_events, "all.jsonl", barrier_prompt, append=True, min_len=min_len)
    #     process_events_to_csv(overcoming_events, "all.jsonl", overcoming_prompt, append=True, min_len=min_len)
    #     process_events_to_csv(hope_events, "all.jsonl", hope_prompt, append=True, min_len=min_len)
    #     process_events_to_csv(anxiety_events, "all.jsonl", anxiety_prompt, append=True, min_len=min_len)
    # else:
    #     process_events_to_csv(solution_events, "solutions.txt", solution_prompt)
    #     process_events_to_csv(barrier_events, "barriers.txt", barrier_prompt)
    #     process_events_to_csv(overcoming_events, "overcoming.txt", overcoming_prompt)
    #     process_events_to_csv(hope_events, "hope.txt", hope_prompt)
    #     process_events_to_csv(anxiety_events, "anxiety.txt", anxiety_prompt)
    # dates = sorted(dates)
    #
    # date_counter = Counter()
    # for date in dates:
    #     date_counter[datetime.utcfromtimestamp(date).strftime('%Y-%m-%d')] += 1
    #
    # df = pd.read_json(json.dumps([i.__dict__ for i in instances]))
    #
    # print(df.head)
    # df["date"] = df["date"].astype("datetime64")
    # ax = df.groupby([df["date"].dt.month, df["date"].dt.day])["user_id"]\
    #     .nunique()\
    #     .plot(kind="bar")
    # ax.set_ylabel("Participants (n=#)")
    # ax.set_xlabel("Date")
    #
    #
    # plt.show()
    #
    # participation = defaultdict(list)
    #
    # for index, row in df.iterrows():
    #     participation[row["user_id"]].append(row["date"])
    #
    # survey_completion = {k: len(v) for k, v in sorted(participation.items(), key=lambda item: len(item[1]))}
    #
    # participation = defaultdict(dict)
    # for i in instances:
    #     k = i.user_id
    #     v = re.search("\.(.*?)'", str(type(i))).group(1)
    #     d = datetime.fromtimestamp(i.date).strftime("%Y-%m-%d")
    #
    #     if v in participation[k]:
    #         participation[k][v].append(d)
    #     else:
    #         participation[k][v] = [d]
    # participation = {k: v for k,v in sorted(participation.items(), key=lambda item: len(item[1]['LikertResponseForm']), reverse=True)}
    #
    # with open("report.txt", "w") as outfile:
    #     for id, p in participation.items():
    #         outfile.write(f'Participant: {id}\n')
    #         for form_type, dates in p.items():
    #             outfile.write(f'\tType: {form_type} ({len(dates)})\n')
    #             for d in dates:
    #                 outfile.write(f'\t\t{d}\n')
    #
    #         outfile.write("\n=========================================================\n\n")
    #
    #
