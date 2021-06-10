from _typeshed import IdentityFunction
import enum


class Agent:
    def __init__(this, firstName, type, isFree):
        this.firstName = firstName
        this.type = type
        this.isFree = isFree
    # Using enum class create enumerations


class ENUM_AgentType(enum.Enum):
    client = "CLIENT"
    taxi = "TAXI"
