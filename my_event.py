from enum import Enum

class EvnetType(Enum):
    mouse = 1
    button = 2
    key =3 
    update=4

class ButtonEvnetType(Enum):
    add_file = 11
    remove_file = 22

class WordEventType(Enum):
    to_known=111
    to_next=222
    to_unknown=333

class Event:
    def __init__(self, event_type, data=None):
        self.event_type = event_type
        self.data = data

class EventDispatcher:
    def __init__(self):
        self.listeners = {}

    def add_listener(self, event_type, listener):
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(listener)

    def remove_listener(self, event_type, listener):
        if event_type in self.listeners:
            self.listeners[event_type].remove(listener)
            if not self.listeners[event_type]:
                del self.listeners[event_type]

    def dispatch(self, event):
        if event.event_type in self.listeners:
            for listener in self.listeners[event.event_type]:
                listener(event)
