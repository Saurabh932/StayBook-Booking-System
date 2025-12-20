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
    
    
class ReviewsNotFoundError(StayBookError):
    status_code = 404
    error_type = "ReviewsNotFoundError"
    message = "Reviews not found"
    
    
class UserAlreadyExistsError(StayBookError):
    status_code = 404
    error_type = "UserAlreadyExistsError"
    message = "User with this email and username already exists"
    
    
class InvalidCredentialsError(StayBookError):
    status_code = 404
    error_type = "InvalidCredentialsError"
    message = "Invalid email or password"
    

class ForbiddenError(StayBookError):
    status_code = 403
    error_type = "Forbidden"
    message = "You are not allowed to perform this action"
