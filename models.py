class Match:
    def __init__(self, match_id: str, name: str, last_activity_date: str):
        self.match_id = match_id
        self.name = name
        self.last_activity_date = last_activity_date


class Message:
    def __init__(self, from_: str, text: str, timestamp: str):
        self.from_ = from_
        self.text = text
        self.timestamp = timestamp
