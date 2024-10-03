from operator import itemgetter

from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableLambda, RunnablePassthrough
from langchain_community.chat_models import ChatOpenAI
from langchain_core.messages import ChatMessage

import mtmai.chainlit as cl
from mtmai.agents.chat_profiles.base_chat_agent import ChatAgentBase
from mtmai.agents.states.ctx import get_mtmai_ctx
from mtmai.core.logging import get_logger
from mtmai.models.chat import ChatProfile

logger = get_logger()


def setup_runnable():
    memory = cl.user_session.get("memory")  # type: ConversationBufferMemory
    model = ChatOpenAI(streaming=True)
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful chatbot"),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{question}"),
        ]
    )

    runnable = (
        RunnablePassthrough.assign(
            history=RunnableLambda(memory.load_memory_variables) | itemgetter("history")
        )
        | prompt
        | model
        | StrOutputParser()
    )
    cl.user_session.set("runnable", runnable)


class HomeAgent(ChatAgentBase):
    """
    首页 聊天机器人
    1: 相当于客服的功能
    """

    def __init__(
        self,
    ):
        pass

    async def __call__(self, state: dict, batchsize: int) -> dict:
        """"""
        return {}

    @classmethod
    def name(cls):
        return "HomeAgent"

    @classmethod
    def get_chat_profile(self):
        return ChatProfile(
            name="HomeAgent",
            description="助手聊天机器人",
        )

    async def chat_start(self):
        # cl.user_session.set("memory", ConversationBufferMemory(return_messages=True))
        # setup_runnable()

        # messages :list[ChatMessage] = []
        prompt_tpl = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a helpful assistant. 负责回答网站用户的问题"),
                MessagesPlaceholder(variable_name="messages", optional=False),
            ]
        ).partial()

        init_messages = prompt_tpl.format_messages(messages=[])
        user_session = cl.user_session
        user_session.set("chat_messages", init_messages)

    async def on_message(self, message: cl.Message):
        user_session = cl.user_session

        pre_messages: list[ChatMessage] = user_session.get("chat_messages")
        pre_messages.append(ChatMessage(role="user", content=message.content))

        ctx = get_mtmai_ctx()

        ai_response = await ctx.call_model_messages(pre_messages)

        await cl.Message(content=ai_response.content).send()
