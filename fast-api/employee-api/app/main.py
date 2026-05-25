from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.db import create_db_and_tables, engine
from app.exceptions import BusinessRuleError, EntityNotFoundError
from app.routers.employee_router import router as employee_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up... Creating database tables")
    create_db_and_tables()
    yield
    print("Shutting down...")
    engine.dispose()


fastapi_app = FastAPI(
    title="Employee API",
    version="0.1.0",
    description="Employee management REST API",
    lifespan=lifespan,
)


@fastapi_app.exception_handler(BusinessRuleError)
async def business_rule_handler(request: Request, exc: BusinessRuleError) -> JSONResponse:
    return JSONResponse(status_code=400, content={"detail": exc.message})


@fastapi_app.exception_handler(EntityNotFoundError)
async def entity_not_found_handler(request: Request, exc: EntityNotFoundError) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": exc.message})


fastapi_app.include_router(employee_router)
