"""
This File contains the main method to start this service. 
"""

import logging
import os
import json

logger = logging.getLogger(__name__)


if __name__ == "__main__":

    config_path: str = os.path.join(os.getcwd(), "config", "config.json")
    with open(config_path, "r") as file:
        config: dict = json.load(file)
    config["absolute_data_path"] = os.path.join(os.getcwd(), config["data_path"])

    logging.basicConfig(
        level=config["log_level"],
        format="%(filename)s:%(lineno)d %(asctime)s %(levelname)s:%(message)s",
    )

    from src.language_practice_assistant.assistant import Assistant

    assistant = Assistant(config)

    assistant.start()
