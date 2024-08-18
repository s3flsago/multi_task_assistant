import asyncio
import logging

from dotenv import load_dotenv

from openai import AsyncOpenAI
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import (
    OpenAIChatCompletion,
    OpenAIChatPromptExecutionSettings,
)
from semantic_kernel.connectors.ai.chat_completion_client_base import (
    ChatCompletionClientBase,
)
from semantic_kernel.connectors.ai.function_choice_behavior import (
    FunctionChoiceBehavior,
)
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.functions.kernel_arguments import KernelArguments
from semantic_kernel.contents.function_call_content import FunctionCallContent
from semantic_kernel.contents.chat_message_content import ChatMessageContent


from src.language_practice_assistant.kernel_plugins import Verbs

load_dotenv()


class SemanticKernel:

    def __init__(self, config: dict):
        self.config: dict = config
        self.kernel: Kernel = Kernel()

        ai_service: OpenAIChatCompletion = OpenAIChatCompletion(
            service_id="chat_completion",
            async_client=AsyncOpenAI(),
            ai_model_id="gpt-4o-mini",
        )
        self.kernel.add_service(ai_service)

        verbs_plugin: Verbs = Verbs(self.config)
        self.kernel.add_plugin(verbs_plugin, "verbs")
        self.history: ChatHistory = self._initiate_chat_history(Verbs.system_prompt())

        self.chat_completion: OpenAIChatCompletion = self.kernel.get_service(
            type=ChatCompletionClientBase
        )

        self.execution_settings: OpenAIChatPromptExecutionSettings = (
            OpenAIChatPromptExecutionSettings(
                service_id="chat",
                max_tokens=2000,
            )
        )
        self.execution_settings.function_choice_behavior = FunctionChoiceBehavior.Auto(
            auto_invoke=True, filters={"included_plugins": ["verbs"]}
        )

    @staticmethod
    def _initiate_chat_history(initial_system_prompt) -> ChatHistory:
        history: ChatHistory = ChatHistory()
        history.add_system_message(initial_system_prompt)
        return history

    async def generate(self):

        while True:
            new_chat_messages: list[ChatMessageContent] = (
                await self.chat_completion.get_chat_message_contents(
                    chat_history=self.history,
                    settings=self.execution_settings,
                    kernel=self.kernel,
                    arguments=KernelArguments(),
                )
            )

            break
        return new_chat_messages

    def run(self, history: str | ChatHistory):
        if isinstance(history, str):
            self.history.add_user_message(history)
        else:
            self.history: ChatHistory = history
        first_new_message_index: int = len(self.history) - 1

        new_chat_messages: ChatHistory = asyncio.run(self.generate())

        try:
            new_messages: list[ChatMessageContent] = self.history[
                first_new_message_index:
            ]
        except UnboundLocalError as u_err:
            logging.error(str(u_err) + "\t-\tApparently, the bot did not answer.")
            return "Sorry, I cannot provide an answer for this. Please provide new instructions."

        for message in new_messages:
            self.history.add_message(message)

            # only for logging
            dct = message.to_dict()
            if "content" in dct.keys():
                logging_output: str = dct["content"]
            for item in message.items:
                if isinstance(item, FunctionCallContent):
                    logging_output: str = str(item)
            logging.info(f"\t{message.role}:\t\t{logging_output}")

        # TODO: check, which new answers are actually responses (maybe more than one?)
        if len(new_chat_messages) == 1:
            last_answer: str = new_chat_messages[-1].content
        else:
            raise IndexError("More than one message returned")

        return last_answer
