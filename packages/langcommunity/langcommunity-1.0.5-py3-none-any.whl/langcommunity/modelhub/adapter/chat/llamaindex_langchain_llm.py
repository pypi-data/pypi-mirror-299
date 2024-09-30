from typing import Any, Callable, Generator, Optional, Sequence

from langchain_core.language_models import BaseLanguageModel


try:
    from llama_index.core.base.llms.generic_utils import (  # type: ignore[unused-ignore] # noqa: F401
        completion_response_to_chat_response,
        stream_completion_response_to_chat_response,
    )
    from llama_index.core.base.llms.types import (  # type: ignore[unused-ignore] # noqa: F401
        ChatMessage,
        ChatResponse,
        ChatResponseAsyncGen,
        ChatResponseGen,
        CompletionResponse,
        CompletionResponseAsyncGen,
        CompletionResponseGen,
        LLMMetadata,
    )
    from llama_index.core.bridge.pydantic import PrivateAttr  # type: ignore[unused-ignore] # noqa: F401
    from llama_index.core.callbacks import CallbackManager  # type: ignore[unused-ignore] # noqa: F401
    from llama_index.core.llms.callbacks import llm_chat_callback, llm_completion_callback  # type: ignore[unused-ignore] # noqa: F401
    from llama_index.core.llms.llm import LLM  # type: ignore[unused-ignore] # noqa: F401
    from llama_index.core.types import BaseOutputParser, PydanticProgramMode, Thread  # type: ignore[unused-ignore] # noqa: F401
    from modelhub.adapter.chat.utils import from_lc_messages, get_llm_metadata, to_lc_messages
except ImportError:
    raise ImportError("Please install `llama_index` library. Please install `poetry add llama-index`.")


class LlamaIndexLangChainChatModel(LLM):
    """Adapter for a LangChain LLM.

    Examples:
        `poetry add llama-index`

        ```python
        from langchain_openai import ChatOpenAI

        from llama_index.llms.langchain import LlamaIndexLangChainLLM

        llm = LlamaIndexLangChainLLM(llm=ChatOpenAI(...))

        response_gen = llm.stream_complete("What is the meaning of life?")

        for r in response_gen:
            print(r.delta, end="")
        ```
    """

    _llm: Any = PrivateAttr()

    def __init__(
        self,
        llm: "BaseLanguageModel",
        callback_manager: Optional[CallbackManager] = None,
        system_prompt: Optional[str] = None,
        messages_to_prompt: Optional[Callable[[Sequence[ChatMessage]], str]] = None,
        completion_to_prompt: Optional[Callable[[str], str]] = None,
        pydantic_program_mode: PydanticProgramMode = PydanticProgramMode.DEFAULT,
        output_parser: Optional[BaseOutputParser] = None,
    ) -> None:
        self._llm = llm
        super().__init__(
            callback_manager=callback_manager,
            system_prompt=system_prompt,
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,
            pydantic_program_mode=pydantic_program_mode,
            output_parser=output_parser,
        )

    @classmethod
    def class_name(cls) -> str:
        return "LlamaIndexLangChainLLM"

    @property
    def llm(self) -> "BaseLanguageModel":
        return self._llm

    @property
    def metadata(self) -> LLMMetadata:
        return get_llm_metadata(self._llm)

    @llm_chat_callback()  # type: ignore[unused-ignore] # noqa: F401
    def chat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        if not self.metadata.is_chat_model:
            prompt = self.messages_to_prompt(messages)
            completion_response = self.complete(prompt, formatted=True, **kwargs)
            return completion_response_to_chat_response(completion_response)

        lc_messages = to_lc_messages(messages)
        lc_message = self._llm.predict_messages(messages=lc_messages, **kwargs)
        message = from_lc_messages([lc_message])[0]
        return ChatResponse(message=message)

    @llm_completion_callback()  # type: ignore[unused-ignore] # noqa: F401
    def complete(self, prompt: str, formatted: bool = False, **kwargs: Any) -> CompletionResponse:
        if not formatted:
            prompt = self.completion_to_prompt(prompt)

        output_str = self._llm.predict(prompt, **kwargs)
        return CompletionResponse(text=output_str)

    @llm_chat_callback()  # type: ignore[unused-ignore] # noqa: F401
    def stream_chat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponseGen:
        if not self.metadata.is_chat_model:
            prompt = self.messages_to_prompt(messages)
            stream_completion = self.stream_complete(prompt, formatted=True, **kwargs)
            return stream_completion_response_to_chat_response(stream_completion)

        if hasattr(self._llm, "stream"):

            def gen() -> Generator[ChatResponse, None, None]:
                lc_messages = to_lc_messages(messages)
                response_str = ""
                for message in self._llm.stream(lc_messages, **kwargs):
                    message = from_lc_messages([message])[0]
                    delta = message.content
                    response_str += delta
                    yield ChatResponse(
                        message=ChatMessage(role=message.role, content=response_str),
                        delta=delta,
                    )

            return gen()

        else:
            from llama_index.core.langchain_helpers.streaming import (
                StreamingGeneratorCallbackHandler,  # type: ignore[unused-ignore] # noqa: F401
            )

            handler = StreamingGeneratorCallbackHandler()

            if not hasattr(self._llm, "streaming"):
                raise ValueError("LLM must support streaming.")
            if not hasattr(self._llm, "callbacks"):
                raise ValueError("LLM must support callbacks to use streaming.")

            self._llm.callbacks = [handler]  # type: ignore
            self._llm.streaming = True  # type: ignore

            thread = Thread(target=self.chat, args=[messages], kwargs=kwargs)
            thread.start()

            response_gen = handler.get_response_gen()

            def gen() -> Generator[ChatResponse, None, None]:
                text = ""
                for delta in response_gen:
                    text += delta
                    yield ChatResponse(
                        message=ChatMessage(text=text),
                        delta=delta,
                    )

            return gen()

    @llm_completion_callback()  # type: ignore[unused-ignore] # noqa: F401
    def stream_complete(self, prompt: str, formatted: bool = False, **kwargs: Any) -> CompletionResponseGen:
        if not formatted:
            prompt = self.completion_to_prompt(prompt)

        from llama_index.core.langchain_helpers.streaming import (
            StreamingGeneratorCallbackHandler,  # type: ignore[unused-ignore] # noqa: F401
        )

        handler = StreamingGeneratorCallbackHandler()

        if not hasattr(self._llm, "streaming"):
            raise ValueError("LLM must support streaming.")
        if not hasattr(self._llm, "callbacks"):
            raise ValueError("LLM must support callbacks to use streaming.")

        self._llm.callbacks = [handler]  # type: ignore
        self._llm.streaming = True  # type: ignore

        thread = Thread(target=self.complete, args=[prompt], kwargs=kwargs)
        thread.start()

        response_gen = handler.get_response_gen()

        def gen() -> Generator[CompletionResponse, None, None]:
            text = ""
            for delta in response_gen:
                text += delta
                yield CompletionResponse(delta=delta, text=text)

        return gen()

    @llm_chat_callback()  # type: ignore[unused-ignore] # noqa: F401
    async def achat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        # TODO: Implement async chat
        return self.chat(messages, **kwargs)

    @llm_completion_callback()
    async def acomplete(self, prompt: str, formatted: bool = False, **kwargs: Any) -> CompletionResponse:
        # TODO: Implement async complete
        return self.complete(prompt, formatted=formatted, **kwargs)

    @llm_chat_callback()
    async def astream_chat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponseAsyncGen:
        # TODO: Implement async stream_chat

        async def gen() -> ChatResponseAsyncGen:
            for message in self.stream_chat(messages, **kwargs):
                yield message

        return gen()

    @llm_completion_callback()
    async def astream_complete(self, prompt: str, formatted: bool = False, **kwargs: Any) -> CompletionResponseAsyncGen:
        # TODO: Implement async stream_complete

        async def gen() -> CompletionResponseAsyncGen:
            for response in self.stream_complete(prompt, formatted=formatted, **kwargs):
                yield response

        return gen()
