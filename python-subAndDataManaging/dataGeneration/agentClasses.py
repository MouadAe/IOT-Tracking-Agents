import enum
from typing import Text


class ENUM_AgentType(enum.Enum):
    client = "CLIENT"
    taxi = "TAXI"


class Agent:
    def __init__(self, firstName, agentType, isFree):
        self.firstName: Text = firstName
        self.type: ENUM_AgentType = agentType
        self.isFree: bool = isFree
    # Using enum class create enumerations


class TrakingAgent:
    def __init__(self, latitude, longitude, date_time, id_agent):
        self.latitude = latitude
        self.longitude = longitude
        self.date_time = date_time
        self.id_agent = id_agent
