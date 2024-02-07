import uvicorn
import settings
from logger_config import logger
from plugin_manager import PluginManager
from authenticate import authenticate_jwt
from fastapi import FastAPI, Request, Response
from callback_response import CallbackResponse

app = FastAPI()
plugin_manager = PluginManager()
plugin_manager.load_plugins(settings.PLUGINS, settings.DB_TYPE)


@app.post("/v2/tx_sign_request")
@authenticate_jwt
async def tx_approval(payload: dict):
    try:
        if await plugin_manager.process_request(payload):
            response = CallbackResponse(
                "APPROVE", payload["requestId"], None
            ).get_response()
            return Response(response)
        else:
            response = CallbackResponse(
                "REJECT", payload["requestId"], "Logic denied"
            ).get_response()
            return Response(response)
    except Exception as e:
        logger.error(f"Transaction Approval process failed with the following error: {e}")


@app.post("/v2/config_change_sign_request")
async def change_approval(request: Request):
    return Response(content="reject")


if __name__ == "__main__":
    logger.info(
        f"Callback handler is running with the following plugins: {plugin_manager.get_plugins()}"
    )
    uvicorn.run("main:app", host="127.0.0.1", port=8000)

