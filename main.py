import uvicorn
from src import settings
from src.exceptions import ValidationError
from src.logs.logger_config import logger
from src.plugins.plugin_manager import PluginManager
from src.authenticate import authenticate_jwt
from src.callback_response import CallbackResponse
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException


plugin_manager = PluginManager()


@asynccontextmanager
async def on_startup(app: FastAPI):
    try:
        settings.run_validations()
        plugin_manager.load_plugins(settings.PLUGINS, settings.DB_TYPE)
        logger.info(f"Callback handler is running with the following plugins: {plugin_manager.get_plugins()}")
        yield
    except ValidationError as e:
        logger.error(f"Validation Error: {e}")
        exit(1)


app = FastAPI(lifespan=on_startup)


@app.post("/v2/tx_sign_request")
@authenticate_jwt
async def tx_approval(request: Request, payload: dict):
    try:
        approval_result = await plugin_manager.process_request(payload)
        response_status = "APPROVE" if approval_result else "REJECT"
        reason = None if approval_result else "Logic denied"
        response = CallbackResponse(response_status, payload["requestId"], reason).get_response()
        return JSONResponse(content=response)
    except Exception as e:
        logger.error(f"Transaction Approval process failed with the following error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/v2/config_change_sign_request")
@authenticate_jwt
async def change_approval(request: Request):
    # Assuming this endpoint needs to perform some operations before returning 'reject'
    # Placeholder for actual logic
    return JSONResponse(content={"message": "reject"})

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=settings.SERVER_PORT)
