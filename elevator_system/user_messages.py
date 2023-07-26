from enum import Enum


class UserMessages(Enum):
    INCORRECT_PAYLOAD = 'No data in request or one of the mandatory fields not present in the request'
    MANDATORY_FIELDS_NOT_PRESENT = 'One or more of the mandatory fields not present'
