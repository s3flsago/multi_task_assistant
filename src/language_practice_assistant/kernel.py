import asyncio
import logging
import json
import os

from dotenv import load_dotenv

from openai import AsyncOpenAI
from semantic_kernel import Kernel
from semantic_kernel.functions import kernel_function
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

from typing import Annotated

load_dotenv()


class Verbs:
    """Plugin for learning verbs with the assistant"""

    def __init__(self):
        self.verbs: list[str] = ["drive", "walk", "fly"]

    @kernel_function(
        name="get_verbs",
        description="Gets the list of verbs that can be learned",
    )
    def get_verbs(
        self,
    ) -> Annotated[list[str], "a list of verbs that can be learned"]:
        """Test function"""
        return self.verbs


class SemanticKernel:

    def __init__(self):
        self.kernel = Kernel()

        ai_service = OpenAIChatCompletion(
            service_id="chat_completion",
            async_client=AsyncOpenAI(),
            ai_model_id="gpt-4o-mini",
        )
        self.kernel.add_service(ai_service)

        verbs_plugin = Verbs()
        self.kernel.add_plugin(verbs_plugin, "verbs")

        self.chat_completion: OpenAIChatCompletion = self.kernel.get_service(
            type=ChatCompletionClientBase
        )

        self.execution_settings = OpenAIChatPromptExecutionSettings(
            service_id="chat",
            max_tokens=2000,
        )
        self.execution_settings.function_choice_behavior = FunctionChoiceBehavior.Auto(
            auto_invoke=True, filters={"included_plugins": ["verbs"]}
        )

        self.history = ChatHistory()

    async def answer(self, history: str | ChatHistory):

        while True:
            userInput = history
            logging.info("User > " + userInput)

            self.history.add_user_message(userInput)

            full_result = await self.chat_completion.get_chat_message_contents(
                chat_history=self.history,
                settings=self.execution_settings,
                kernel=self.kernel,
                arguments=KernelArguments(),
            )
            for res in full_result[1:]:
                self.history.add_message(res)
            result = full_result[0]

            print("Assistant > " + str(result))
            break
        return self.history

    def run(self, history: str | ChatHistory):
        hstry = asyncio.run(self.answer(history=history))

        for el in hstry:
            print()
            print(
                "____________________________________________________________________________"
            )
            logging.error(el.role)
            dct = el.to_dict()
            if "content" in dct.keys():
                logging.error(el.to_dict()["content"])
            for item in el.items:
                if isinstance(item, FunctionCallContent):
                    logging.error(item)

        return self.history[-1].content


if __name__ == "__main__":

    verbs_plugin = Verbs()
    print(verbs_plugin.get_verbs())

    kernel = SemanticKernel()
    init_prompt: str = "What verbs can be learned?"
    answer = kernel.run(init_prompt)
    print(answer)
