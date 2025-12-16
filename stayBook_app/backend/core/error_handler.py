from fastapi import Request
from fastapi.responses import JSONResponse
from .exception import StayBookError
from fastapi.exceptions import RequestValidationError

async def staybook_exception_handler(request: Request, exc: StayBookError):
    return JSONResponse(status_code=exc.status_code,
                        content={"success":False,
                                 "error":{"type":exc.error_type,
                                          "message":exc.message}})
    
    
async def generic_exception_handler(request:Request, exc: Exception):
    return JSONResponse(status_code=500,
                        content={"success":False,
                                 "error":{"type":"InternalServerError",
                                          "message":"Unexpected server error"}})


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    errors = {}

    for err in exc.errors():
        field = ".".join(str(loc) for loc in err["loc"] if loc != "body")
        message = err["msg"]
        errors[field] = message

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": {
                "type": "ValidationError",
                "details": errors,
            },
        },
    )
    