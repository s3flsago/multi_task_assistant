import asyncio
import logging
import os
import pkgutil
import importlib
import inspect
from typing import Optional, Callable

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
from semantic_kernel.contents.utils.author_role import AuthorRole
from semantic_kernel.contents import ChatMessageContent, TextContent, ImageContent

from pydantic import BaseModel, Field



class KernelFunctionMapping(BaseModel): 
    name: str = Field(..., min_length=1, max_length=50)
    object_spec: Optional[Callable[..., object]] = None
    methods: Optional[list[str]] = Field(default_factory=list)


class SemanticKernel:

    system_prompt: str = None

    def __init__(self, config: dict, assistant_name: str):
        self.config: dict = config
        self.agent_config: dict = config["agent_config_info"][assistant_name]
        self.kernel: Kernel = Kernel()

        ai_service: OpenAIChatCompletion = OpenAIChatCompletion(
            service_id="chat_completion",
            async_client=AsyncOpenAI(),
            ai_model_id=self.agent_config["llm_name"],
        )
        self.kernel.add_service(ai_service)

        plugin_class_names: list[str] = self.agent_config["included_plugins"]
        selected_plugins: list[KernelFunctionMapping] = self.select_plugins(plugin_class_names)
        
        for plugin_class in selected_plugins:
            plugin_instance = plugin_class.object_spec(self.config)
            self.kernel.add_plugin(plugin_instance, plugin_instance.name)
            if plugin_instance.system_prompt():
                if not self.system_prompt:
                    self.system_prompt: str = plugin_instance.system_prompt()
                else:
                    raise ValueError(f"More than one plugin with system prompt detected")
        self.history: ChatHistory = self._initiate_chat_history(self.system_prompt)

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

    def select_plugins(self, plugin_class_names: list[str]) -> list[KernelFunctionMapping]:
        logging.info(f"Scanning plugin classes for {plugin_class_names}...")
        current_directory = os.path.dirname(os.path.abspath(__file__))
        plugins_directory= os.path.join(current_directory, "kernel_plugins")

        available_plugin_modules: list[str] = [
            module.name for module in pkgutil.iter_modules([plugins_directory])
        ]
        scanned_classes: list[KernelFunctionMapping] = []
        for plugin_module_name in available_plugin_modules:
            logging.info(f"Checking available module {plugin_module_name}")
            full_module_name: str = f"{self.config['plugins_path']}.{plugin_module_name}"
            try:
                module = importlib.import_module(full_module_name)
            except ImportError as e:
                logging.error(f"Error importing plugin module {full_module_name}: {e}")

            for _, obj in inspect.getmembers(module, inspect.isclass):
                logging.info(f"Checking available class {plugin_module_name}.{obj.__name__}")
                if obj.__name__ in plugin_class_names:
                    # Check if the class is defined in this module (not imported) and is not abstract
                    if obj.__module__ == full_module_name and not inspect.isabstract(obj):
                        logging.info(f"Checking module: {obj.__module__} ({module})")
                        
                        # Get the class methods and check for @kernel_function
                        class_methods = [
                            func for _, func in inspect.getmembers(obj, inspect.isfunction)
                            # if hasattr(func, "_kernel_function_")
                        ]
                        logging.info(f"Module: {obj.__module__} has class_methods: {class_methods}")

                        if class_methods:
                            # Add class to the kernel and log the added methods
                            method_names = [func.__name__ for func in class_methods]
                            fnct = KernelFunctionMapping(
                                name=obj.__name__, 
                                object_spec=obj, 
                                methods=method_names
                            )
                            scanned_classes.append(fnct)
                            
                            logging.info(
                                "Added plugin %s to kernel with methods: '%s'",
                                obj.__name__,
                                method_names,
                            )
                        else:
                            logging.warning(f"Module {full_module_name} does not have class methods.")
        return scanned_classes



    @staticmethod
    def _initiate_chat_history(initial_system_prompt) -> ChatHistory:
        history: ChatHistory = ChatHistory()
        history.add_system_message(initial_system_prompt)
        logging.info(f"Initated chat history.")
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

    @staticmethod
    def get_data_uri_from_bytes(bytes, mime_type: str) -> str:
        import base64
        base64_encoded_data = base64.b64encode(bytes).decode("utf-8")
        data_uri = f"data:{mime_type};base64,{base64_encoded_data}"
        return data_uri

    def run(self, input_text: str | None, input_image: bytes | None ):
        if input_text=="!new":
            self.history: ChatHistory = self._initiate_chat_history(self.system_prompt)

        user_input_items = []
        if input_text:
            user_input_items.append(TextContent(text=input_text))
        if input_image:
            data_uri = self.get_data_uri_from_bytes(input_image, "image/jpeg")
            user_input_items.append(ImageContent(data_uri=data_uri,))

        user_chat_message_content = ChatMessageContent(
            role=AuthorRole.USER, items=user_input_items
        )

        self.history.add_message(user_chat_message_content)

        first_new_message_index: int = len(self.history) - 1
        new_chat_messages: ChatHistory = asyncio.run(self.generate())

        try:
            # logging.info(f"Length of history: {len(self.history)}")
            new_messages: list[ChatMessageContent] = self.history[first_new_message_index:] + [new_chat_messages[-1]]
        except UnboundLocalError as u_err:
            logging.error(str(u_err) + "\t-\tApparently, the bot did not answer.")
            return "Sorry, I cannot provide an answer for this. Please provide new instructions."

        for message in new_messages:
            self.history.add_message(message)

            # only for logging
            dct = message.to_dict()

            for item in message.items:
                if isinstance(item, FunctionCallContent):
                    logging_plugin_output: str = str(item)
                    logging.info(f"\t{message.role}:\t\t{logging_plugin_output}")
            if "content" in dct.keys():
                logging_message_output: str = dct["content"]
                logging.info(f"\t{message.role}:\t\t{logging_message_output}")

        # TODO: check, which new answers are actually responses (maybe more than one?)
        if len(new_chat_messages) == 1:
            last_answer: str = new_chat_messages[-1].content
            self.history.add_message(new_chat_messages[-1])

        else:
            raise IndexError("More than one message returned")
        

        return last_answer
