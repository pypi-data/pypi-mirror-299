from typing import Annotated

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import Runnable, RunnableConfig
from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState, tools_condition
from mtmai.agents.graphchatdemo.tools.search_tools import search_tool
from mtmai.agents.ctx import get_mtmai_ctx
from mtmai.agents.states.state import MainState
from mtmai.core.config import settings
from mtmai.core.logging import get_logger

logger = get_logger()


class OnChatStartNode:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    async def __call__(self, state: MainState, config: RunnableConfig):
        logger.info("on_chat_start_node")
        ctx = get_mtmai_ctx()
        return {
            "messages": [],
        }
