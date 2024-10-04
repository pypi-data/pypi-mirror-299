from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import ChatMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool

# from langchain_together import ChatTogether
from pydantic import BaseModel, Field

from mtmai.agents.states.research_state import add_messages
import mtmai.chainlit as cl
from mtmai.agents.chat_profiles.base_chat_agent import ChatAgentBase
from mtmai.agents.ctx import get_mtmai_ctx
from mtmai.chainlit import context
from mtmai.core.logging import get_logger
from mtmai.models.chat import ChatProfile

logger = get_logger()


# def setup_runnable():
#     memory = cl.user_session.get("memory")  # type: ConversationBufferMemory
#     model = ChatOpenAI(streaming=True)
#     prompt = ChatPromptTemplate.from_messages(
#         [
#             ("system", "You are a helpful chatbot"),
#             MessagesPlaceholder(variable_name="history"),
#             ("human", "{question}"),
#         ]
#     )

#     runnable = (
#         RunnablePassthrough.assign(
#             history=RunnableLambda(memory.load_memory_variables) | itemgetter("history")
#         )
#         | prompt
#         | model
#         | StrOutputParser()
#     )
#     cl.user_session.set("runnable", runnable)


class get_current_weather(BaseModel):
    """Get the current weather in a given location"""

    location: str = Field(..., description="The city and state, e.g. San Francisco, CA")


async def call_model_messages(
    messages: list[ChatMessage],
):
    ctx = get_mtmai_ctx()
    llm_chat = ctx.graph_config.llms.get("chat")

    # prompt_tpl = ChatPromptTemplate.from_messages(
    #     [
    #         (
    #             "system",
    #             "You are a helpful assistant that can access external functions. The responses from these function calls will be appended to this dialogue. Please provide responses based on the information from these function calls.",
    #         ),
    #         (
    #             "user",
    #             "What is the current temperature of New York, San Francisco and Chicago?",
    #         ),
    #         # MessagesPlaceholder(variable_name="messages", optional=False),
    #     ]
    # ).partial()
    # init_messages = prompt_tpl.format_messages(messages=[])
    # messages = [
    #     SystemMessage(
    #         content="You are a helpful assistant that can access external functions."
    #     ),
    #     HumanMessage(
    #         content="What is the current temperature of New York, San Francisco and Chicago?"
    #     ),
    # ]

    # tools = [
    #     {
    #         "type": "function",
    #         "function": {
    #             "name": "get_current_weather",
    #             "description": "Get the current weather in a given location",
    #             "parameters": {
    #                 "type": "object",
    #                 "properties": {
    #                     "location": {
    #                         "type": "string",
    #                         "description": "The city and state, e.g. San Francisco, CA",
    #                     },
    #                     "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
    #                 },
    #             },
    #         },
    #     }
    # ]

    # json_mes = json.dumps(jsonable_encoder(messages), indent=4)
    # print("json_mes", json_mes)

    # llm_inst = ChatOpenAI(
    #     # stream=True,
    #     base_url=llm_chat.base_url,
    #     api_key=llm_chat.api_key,
    #     model=llm_chat.model,
    #     temperature=llm_chat.temperature,
    #     n=1,
    #     # max_tokens=llm_chat.max_tokens, # !!! 注意，together ai，是可以调用工具的，但是如果有max_tokens 参数，就会调用不成功，仅仅返回普通的对话消息。
    # )
    # llm_inst = ChatTogether(
    #     base_url=llm_chat.base_url,
    #     api_key=llm_chat.api_key,
    #     model=llm_chat.model,
    #     temperature=llm_chat.temperature,
    #     max_tokens=llm_chat.max_tokens,
    # )

    # llm_chain = llm_inst
    tools = [home_ui_tool]
    # llm_chain = llm_chain.bind_tools(tools)
    # llm_chain = llm_chain.with_retry(stop_after_attempt=5)
    # ai_msg = llm_chain.invoke(messages)
    # tool_calls = ai_msg.tool_calls
    # print(tool_calls)
    ai_msg = await ctx.ainvoke_model_messages(messages, tools)

    return ai_msg


@tool(parse_docstring=False, response_format="content_and_artifact")
def home_ui_tool():
    """通过调用此工具，可以展示不同的UI 面板，当用户有需要时可以调用这个函数向用户显示不同的操作面板"""
    return (
        "Operation successful",
        {
            "artifaceType": "AdminView",
            "props": {
                "title": "管理面板",
            },
        },
    )


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
        # prompt_tpl = ChatPromptTemplate.from_messages(
        #     [
        #         (
        #             "system",
        #             "You are a helpful assistant that can access external functions. The responses from these function calls will be appended to this dialogue. Please provide responses based on the information from these function calls.",
        #         ),
        #         MessagesPlaceholder(variable_name="messages", optional=False),
        #     ]
        # ).partial()

        # init_messages = prompt_tpl.format_messages(messages=[])
        user_session = cl.user_session
        # user_session.set("chat_messages", init_messages)

        # 升级为 graph 模式
        ctx = get_mtmai_ctx()
        graph = await ctx.get_compiled_graph("home_chat")
        user_session.set("graph", graph)

    async def on_message(self, message: cl.Message):
        user_session = cl.user_session
        pre_messages: list[ChatMessage] = user_session.get("chat_messages")

        inputs = {"messages": pre_messages}
        await self.run_graph(inputs)

    async def run_graph(self, inputs):

        user_session = cl.user_session
        thread_id = context.session.thread_id
        graph = user_session.get("graph")
        thread: RunnableConfig = {
            "configurable": {
                "thread_id": thread_id,
            }
        }


        async for event in graph.astream_events(
            inputs,
            version="v2",
            config=thread,
            subgraphs=True,
        ):
            thread_id = thread.get("configurable").get("thread_id")
            kind = event["event"]
            node_name = event["name"]
            data = event["data"]

            current_state = await graph.aget_state(thread, subgraphs=True)
            # await cl.Message(content=kind).send()
            if kind == "on_chat_model_end":
                output = data.get("output")
                if output:
                    chat_output = output.content
                    await cl.Message(chat_output).send()

            if kind == "on_chain_end":
                if node_name == "LangGraph":
                    logger.info("中止节点")
                    if (
                        data
                        and (output := data.get("output"))
                        and (final_messages := output.get("messages"))
                    ):
                        for message in final_messages:
                            message.pretty_print()

            if kind == "on_tool_start":
                logger.info("(@stream)工具调用开始 %s", node_name)

            if kind == "on_tool_end":
                output = data.get("output")
                logger.info("(@stream)工具调用结束 %s %s", node_name, output)
                if node_name == "coplilot_ui_tools":
                    await cl.Message(content="工具调用结束").send()


