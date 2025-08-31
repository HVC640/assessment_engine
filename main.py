import uvicorn
import logging
import logging.config
import os

if os.path.exists("core/logging_config.ini"):
    logging.config.fileConfig("core/logging_config.ini", disable_existing_loggers=False)
else:
    logging.basicConfig(level=logging.INFO)
    logging.warning("logging_config.ini not found. Using basicConfig.")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
