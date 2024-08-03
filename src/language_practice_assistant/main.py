"""
This File contains the main method to start this service. 
"""

import logging

logger = logging.getLogger(__name__)


if __name__ == "__main__":

    from src.language_practice_assistant.assistant import Assistant

    assistant = Assistant()

    assistant.start()
