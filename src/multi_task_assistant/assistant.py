import logging
import os
import multiprocessing

from dotenv import load_dotenv

from src.multi_task_assistant.kernel import SemanticKernel
from src.multi_task_assistant.telegram_client import TelegramClient

logger = logging.getLogger(__name__)

load_dotenv()



class AssistantHandler():

    def __init__(self, config):
        self.config = config

    def setup_assistants_parallel(self,):
        processes = []
        for assistant_name in self.config["active_agents"]:
            process = multiprocessing.Process(target=self.create_and_start, args=(self.config, assistant_name)) 
            process.start()
            processes.append(process)

        for process in processes:
            process.join() 

    @staticmethod
    def create_and_start(config: dict, assistant_name: str):
        assistant = Assistant(config, assistant_name)
        assistant.start()



class Assistant:

    def __init__(self, config: dict, assistant_name: str):
        logging.info(f"Building assistant {assistant_name}")
        self.semantic_kernel = SemanticKernel(config, assistant_name)
        telegram_token_env_variable: str = config["agent_config_info"][assistant_name]["telegram_token_envvar"]
        telegram_token: str = os.getenv(telegram_token_env_variable)
        
        self.telegram_client = TelegramClient(
            config=config, semantic_kernel=self.semantic_kernel, telegram_token=telegram_token
        )

    def start(self):
        self.telegram_client.run()

    def terminate(self):
        self.telegram_client.shutdown()
        logging.info("Assistant terminated.")
