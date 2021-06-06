from rest_framework.exceptions import APIException


class UnreachableServiceError(APIException):
    default_detail = "Unable to reach the API service."


class ServiceRequestError(APIException):
    default_detail = "Http error from the API service."


class EmptyDataResponseError(APIException):
    default_detail = "Invalid data returned from the API service."


class JSONResponseError(APIException):
    default_detail = "Error decoding JSON data to python data structures."
