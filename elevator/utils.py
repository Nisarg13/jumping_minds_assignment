import logging

from rest_framework.exceptions import ParseError

from elevator_system.user_messages import UserMessages

logger = logging.getLogger('django')


class ValidationUtils:
    @classmethod
    def validate_keys_in_request_body(cls, request_data, list_of_keys):
        if not all(x in request_data for x in list_of_keys):
            logger.error(UserMessages.INCORRECT_PAYLOAD.value)
            raise ParseError(detail=UserMessages.INCORRECT_PAYLOAD.value)

    @classmethod
    def validate_values_of_keys_in_request_body(cls, request_data, list_of_keys):
        if any(not request_data[x] for x in list_of_keys):
            logger.error(UserMessages.MANDATORY_FIELDS_NOT_PRESENT.value)
            raise ParseError(detail=UserMessages.MANDATORY_FIELDS_NOT_PRESENT.value)
