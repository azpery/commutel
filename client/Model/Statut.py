from enum import Enum

class statut(Enum):
    READY_FOR_CONVERSATION = 200
    CONNECTION_OK = 202
    DISCONNECTED = 204
    BUSY = 206
    UNREGISTRED = 1
    COMPOSING = 6
    REGISTRED = 4
    TIME_OUT = 13
    PENDING = 66
    NOT_FOUND = 404