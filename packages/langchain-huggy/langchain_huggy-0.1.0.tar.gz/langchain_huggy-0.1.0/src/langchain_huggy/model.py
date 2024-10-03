from typing import Any, Dict, List, Optional, Union
from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, ChatMessage, HumanMessage, SystemMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from hugchat import hugchat
from hugchat.login import Login
from configparser import ConfigParser
import os
from dotenv import load_dotenv

load_dotenv()


class HuggingChat(BaseChatModel):
    model: str = "meta-llama/Meta-Llama-3.1-70B-Instruct"
    cookies: Dict[str, str] = None
    chatbot: hugchat.ChatBot = None

    def __init__(self, model: str = None, **kwargs):
        super().__init__(**kwargs)
        self.model = model or self.model
        self.cookies = self._setup_login()
        self.chatbot = self._setup_chatbot()

    @property
    def _llm_type(self) -> str:
        return "hugging-chat"

    def _setup_login(self) -> Dict[str, str]:
        config_parser = ConfigParser()
        config_parser.read("/home/ntlpt59/MAIN/omni-ai/src/main/backend/config.ini")
        email = os.getenv("HUGGINGFACE_EMAIL")
        passwd = os.getenv("HUGGINGFACE_PASSWD")

        cookie_path_dir = "./cookies/"
        sign = Login(email, passwd)
        cookies = sign.login(cookie_dir_path=cookie_path_dir, save_cookies=True)
        return cookies.get_dict()

    def _setup_chatbot(self) -> hugchat.ChatBot:
        return hugchat.ChatBot(cookies=self.cookies, default_llm=self.model)

    def _convert_messages_to_prompt(self, messages: List[BaseMessage]) -> str:
        prompt = ""
        for message in messages:
            if isinstance(message, SystemMessage):
                prompt += f"System: {message.content}\n"
            elif isinstance(message, HumanMessage):
                prompt += f"Human: {message.content}\n"
            elif isinstance(message, AIMessage):
                prompt += f"AI: {message.content}\n"
            elif isinstance(message, ChatMessage):
                prompt += f"{message.role.capitalize()}: {message.content}\n"
        return prompt.strip()

    def _generate(
            self,
            messages: List[BaseMessage],
            stop: Optional[List[str]] = None,
            run_manager: Optional[CallbackManagerForLLMRun] = None,
            **kwargs: Any,
    ) -> ChatResult:
        prompt = self._convert_messages_to_prompt(messages)
        response = self.chatbot.chat(prompt, **kwargs)

        ai_message = AIMessage(content=response)
        chat_generation = ChatGeneration(message=ai_message)
        return ChatResult(generations=[chat_generation])

    def _stream(
            self,
            messages: List[BaseMessage],
            stop: Optional[List[str]] = None,
            run_manager: Optional[CallbackManagerForLLMRun] = None,
            **kwargs: Any,
    ) -> Union[ChatGeneration, List[ChatGeneration]]:
        prompt = self._convert_messages_to_prompt(messages)
        for resp in self.chatbot.chat(prompt, stream=True, **kwargs):
            if resp:
                chunk = resp['token']
                if run_manager:
                    run_manager.on_llm_new_token(chunk)
                yield ChatGeneration(message=AIMessage(content=chunk))

    def _add_system_prompt(self, query: str) -> str:
        system_prompt = """
        You are an AI assistant created by OmniAI. Approach each query with careful consideration and analytical thinking. When responding:

        1. Thoroughly analyze complex and open-ended questions, but be concise for simpler tasks.
        2. Break down problems systematically before providing final answers.
        3. Engage in discussions on a wide variety of topics with intellectual curiosity.
        4. For long tasks that can't be completed in one response, offer to do them piecemeal and get user feedback.
        5. Use markdown for code formatting.
        6. Avoid unnecessary affirmations or filler phrases at the start of responses.
        7. Respond in the same language as the user's query.
        8. Do not apologize if you cannot or will not perform a task; simply state that you cannot do it.
        9. If asked about very obscure topics, remind the user at the end that you may hallucinate in such cases.
        10. If citing sources, inform the user that you don't have access to a current database and they should verify any citations.

        Original query: {query}

        Respond to this query following the guidelines above.
        """
        return system_prompt

    def generate(
            self,
            messages: List[BaseMessage],
            stop: Optional[List[str]] = None,
            run_manager: Optional[CallbackManagerForLLMRun] = None,
            **kwargs: Any,
    ) -> ChatResult:
        enhanced_messages = [SystemMessage(content=self._add_system_prompt(""))] + messages
        return self._generate(enhanced_messages, stop, run_manager, **kwargs)

    def stream(
            self,
            messages: List[BaseMessage],
            stop: Optional[List[str]] = None,
            run_manager: Optional[CallbackManagerForLLMRun] = None,
            **kwargs: Any,
    ) -> Union[ChatGeneration, List[ChatGeneration]]:
        enhanced_messages = [SystemMessage(content=self._add_system_prompt(""))] + messages
        return self._stream(enhanced_messages, stop, run_manager, **kwargs)