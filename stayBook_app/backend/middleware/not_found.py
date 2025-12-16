from fastapi import Request
from fastapi.responses import RedirectResponse, JSONResponse


async def not_found_middleware(request: Request, call_next):
    response = await call_next(request)

    if response.status_code == 404:
        accept = request.headers.get("accept", "")

        if "text/html" in accept:
            # 👇 IMPORTANT: use 302 or 307, NOT 404
            return RedirectResponse("/error.html", status_code=302)

        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "error": {
                    "type": "NotFound",
                    "message": "Resource not found",
                },
            },
        )

    return response
