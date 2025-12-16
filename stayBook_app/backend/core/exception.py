class StayBookError(Exception):
    '''
    Base class for all custom errors
    '''
    status_code = 500
    error_type = "StayBookError"
    message = "Something went wrong"
    

class ListingNotFoundError(StayBookError):
    status_code = 404
    error_type = "ListingNotFound"
    message = "Listing not found"
    

class ValidationError(StayBookError):
    status_code = 400
    error_type = "ValidationError"
    message = "Invalid input provided"