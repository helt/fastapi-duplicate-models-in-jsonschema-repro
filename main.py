# main.py
import uvicorn

if __name__ == "__main__":
    uvicorn.run("fastapi_duplicate_models_in_jsonschema_repro.main:app", port=8090, log_level="debug", reload=True, host="0.0.0.0")
