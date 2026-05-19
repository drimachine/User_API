from fastapi import Request
from fastapi.responses import JSONResponse
from schemas.errors import ErrorDetail

PUPLIC_ROUTES = {"/docs", "/openapi.json"}

async def user_id_middleware(request, call_next):

    raw = request.headers.get("X-User-Id")

    if request.url.path not in PUPLIC_ROUTES:
        if not raw:
            return JSONResponse(
                status_code = 400,
                content=ErrorDetail.create(
                    status = 400,
                    error = "Missing Header",
                    message = f"O header '{"X-User-Id"}' é obrigatorio",
                    path = request.url.path,
                ).model_dump(),
            )
        

        try:
            response = int(raw)
            request.state.user_id = response
            return await call_next(request)
        except ValueError:
                return JSONResponse(
                    status_code = 422,
                    content=ErrorDetail.create(
                        status = 422,
                        error = "Invalid header value",
                        message = f"O header '{"X-User-Id"}' é invalido",
                        path = request.url.path,
                    ).model_dump(),
                )
    return await call_next(request)