import json
import logging

from fastapi.encoders import jsonable_encoder
from langchain_core.runnables import RunnableConfig

import mtmai.chainlit as cl
from mtmai.agents.states.ctx import get_mtmai_ctx
from mtmai.mtlibs import mtutils

logger = logging.getLogger()


async def agent_event_stream_v2(
    *,
    model: str | None = None,
    inputs: dict,
    debug: bool = False,
):
    current_step = cl.context.current_step
    ctx = get_mtmai_ctx()
    graph = await ctx.get_compiled_graph(model)

    thread_id = mtutils.gen_orm_id_key()
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
        # user_id = user.id
        kind = event["event"]
        node_name = event["name"]
        data = event["data"]

        current_state = await graph.aget_state(thread, subgraphs=True)
        # logger.info("current_state next: %s", current_state.next)
        graph_step = -1
        if current_state and current_state.metadata:
            graph_step = current_state.metadata.get("step")  # 第几步

        if kind == "on_chain_start":
            if node_name == "LangGraph":
                await cl.Message(content="流程开始").send()
            elif not is_internal_node(node_name):  # 跳过内部节点
                await cl.Message(
                    content="开始 %s, 第 %s 步" % (node_name, graph_step)
                ).send()

        elif kind == "on_chat_model_start":
            if debug:
                await cl.Message(content="调用大语言模型开始").send()
        elif kind == "on_chat_model_end":
            elements = [
                cl.Text(
                    name="simple_text",
                    content=json.dumps(jsonable_encoder(data)),
                    display="inline",
                )
            ]
            await cl.Message(
                content="调用大语言模型结束",
                elements=elements,
            ).send()

        elif kind == "on_chat_model_stream":
            if event["metadata"].get("langgraph_node") == "human_node":
                content = data["chunk"].content
                if content:
                    await current_step.stream_token(content)

            if event["metadata"].get("langgraph_node") == "final":
                logger.info("终结节点")

        elif kind == "on_chat_model_end":
            output = data.get("output")
            if output:
                chat_output = output.content
                current_step.output = "节点输出：" + chat_output
                await cl.Message("节点输出：" + chat_output).send()

        # if kind == "on_chain_stream":
        #     if data and node_name == "entry_node":
        #         chunk_data = data.get("chunk", {})
        #         picked_data = {
        #             key: chunk_data[key]
        #             for key in ["ui_messages", "uistate"]
        #             if key in chunk_data
        #         }

        #         if picked_data:
        #             yield aisdk.data(picked_data)
        elif kind == "on_chain_end":
            #     chunk_data = data.get("chunk", {})

            #     if node_name == "human_node":
            #         output = data.get("output")
            #         if output:
            #             artifacts = data.get("output").get("artifacts")
            #             if artifacts:
            #                 yield aisdk.data({"artifacts": artifacts})

            if node_name == "LangGraph":
                await cl.Message(content="流程结束（或暂停）").send()
                if (
                    data
                    and (output := data.get("output"))
                    and (final_messages := output.get("messages"))
                ):
                    for message in final_messages:
                        message.pretty_print()
            else:
                if not is_internal_node(node_name):
                    await cl.Message(
                        content=f"节点 {node_name} 结束, 第 {graph_step}步"
                    ).send()

        elif kind == "on_tool_start":
            logger.info("工具调用开始 %s", node_name)
            if debug:
                await cl.Message(content=f"工具调用开始 {node_name}").send()
        elif kind == "on_tool_end":
            logger.info("工具调用结束 %s", node_name)
            await cl.Message(content=f"工具调用结束 {node_name}").send()

        else:
            logger.info("kind: %s, node_name: %s", kind, node_name)
            if debug:
                await cl.Message(content=f"其他节点 {node_name}").send()


internal_node_types = set(
    [
        "RunnableSequence",
        "RunnableLambda",
        "RunnableParallel<raw>",
        "RunnableWithFallbacks",
        "_write",
        "start",
        "end",
    ]
)


def is_internal_node(node_name: str):
    """
    判断是否是内部节点
    """
    return node_name in internal_node_types
