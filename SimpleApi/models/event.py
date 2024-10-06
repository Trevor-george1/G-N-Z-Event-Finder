#!/usr/bin/python3




class Event():
    def __init__(self, name, date, venue, time) -> None:
        self.name = name
        self.date = date
        self.venue = venue
        self.time = time
        

    def to_dict(self):
        return {
            "name": self.name,
            "date": self.date,
            "vanue": self.venue,
            "time": self.time
        }