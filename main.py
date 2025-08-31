import uvicorn
import logging
import logging.config
import os

log_config_path = "core/logging_config.ini"
logs_dir = "Logs"

if os.path.exists(log_config_path):
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
else:
    logging.basicConfig(level=logging.INFO)
    logging.warning("logging_config.ini not found. Using basicConfig.")

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_config=log_config_path if os.path.exists(log_config_path) else None
    )
