import logging
from typing import Annotated

from langchain_core.tools import tool
from langgraph.graph import END, StateGraph
from langgraph.graph.message import AnyMessage, add_messages
from langgraph.prebuilt import ToolNode

# from openai import BaseModel
from pydantic import BaseModel

from mtmai.agents.graphs.abstract_graph import AbstractGraph
from mtmai.agents.nodes.chat_node import ChatNode
from mtmai.llm.llm import get_fast_llm

logger = logging.getLogger()


class HomeChatState(BaseModel):
    messages: Annotated[list[AnyMessage], add_messages]


@tool(parse_docstring=False, response_format="content_and_artifact")
def coplilot_ui_tools(panel_name: str):
    """Call to control frontend coplilot ui panels"""
    return (
        "Operation successful",
        {
            "artifaceType": "AdminView",
            "props": {
                "title": "管理面板",
            },
        },
    )


def should_continue(state: HomeChatState):
    messages = state.messages
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return "chat_node"


class HomeChatGraph(AbstractGraph):
    def create_graph(self) -> StateGraph:
        tools = [coplilot_ui_tools]
        tool_node = ToolNode(tools)

        runnable = get_fast_llm()
        runnable = runnable.bind_tools(tools)

        wf = StateGraph(HomeChatState)
        wf.add_node("chat_node", ChatNode(runnable))
        wf.add_node("tools", tool_node)

        wf.add_conditional_edges("chat_node", should_continue, ["tools", END])

        wf.set_entry_point("chat_node")

        return wf
