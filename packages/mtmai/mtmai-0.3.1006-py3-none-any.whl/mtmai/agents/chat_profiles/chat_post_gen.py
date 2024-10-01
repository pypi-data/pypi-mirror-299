"""
GraphIterator Module
"""

import json
import uuid

from fastapi.encoders import jsonable_encoder

import mtmai.chainlit as cl
from mtmai.agents.chat_profiles.base_chat_agent import ChatAgentBase
from mtmai.agents.nodes.hello_agent import (
    NodeSectionWriterRequest,
    RefineOutlineNodeRequest,
    init_outline_v3,
    node_refine_outline,
    node_section_writer,
    node_survey_subjects,
)
from mtmai.agents.nodes.qa_node import QaNodeRequest, QaNodeResult, node_qa
from mtmai.agents.states.research_state import ResearchState
from mtmai.chainlit.context import context
from mtmai.core.db import get_async_session
from mtmai.core.logging import get_logger
from mtmai.crud.curd_site import get_site_by_id
from mtmai.models.chat import ChatProfile

logger = get_logger()


class PostGenAgent(ChatAgentBase):
    """
    前端站点的 “AI生成新文章”按钮，调用这个agent
    """

    def __init__(
        self,
    ):
        pass

    async def __call__(self, state: dict, batchsize: int) -> dict:
        """"""
        # TODO: langgraph 调用入口

        return {}

    @classmethod
    def name(cls):
        return "postGen"

    @classmethod
    def get_chat_profile(self):
        return ChatProfile(
            name="postGen",
            description="博客文章生成器",
        )

    async def chat_start(self):
        await cl.Message(content="post gen 博客文章生成开始").send()

        fnCall_result = await context.emitter.send_call_fn("fn_get_site_id", {})
        # # logger.info("函数调用结果 %s", fnCall_result)
        siteId = fnCall_result.get("siteId", "")
        async with get_async_session() as session:
            site = await get_site_by_id(session, uuid.UUID(siteId))

        site_description = site.description

        # await step_hello2()
        # # await step_joke_graph(topic=site_description)
        # # 提示，这两步可以并发执行

        # # 获取相关主题
        # async with cl.Step(name="获取相关主题", type="llm") as step:
        #     step.input = "Test hello input"
        #     subjects = await node_survey_subjects(topic=site_description)
        #     step.output = subjects
        # # logger.info("result: %s", result)
        # await cl.Message(content="文章生成完毕，需要发布吗？").send()

        # inputs = {
        #     "prompt": site_description,
        #     "topic": site_description,
        # }
        graph_state = ResearchState(
            topic=site_description,
        )

        if not graph_state.outline:
            # 生成初始大纲
            init_outline = await init_outline_v3(topic=site_description)
            graph_state.outline = init_outline

        if not graph_state.editors:
            # 获取相关主题
            async with cl.Step(name="获取相关主题", type="llm") as step:
                step.input = "Test hello input"
                subjects = await node_survey_subjects(topic=site_description)
                step.output = subjects

                graph_state.editors = subjects.editors
        if not graph_state.interview_results:
            # 请教领域专家
            async with cl.Step(name="请教领域专家", type="llm") as step:
                # step.input = "Test hello input"

                qa_results: list[QaNodeResult] = []
                # TODO: 这里应该有多个专家，不过，目前开发阶段暂时只处理一个
                result = await node_qa(
                    req=QaNodeRequest(
                        topic=site_description,
                        editor=graph_state.editors[0],
                    )
                )
                qa_results.append(result)
                step.output = json.dumps(jsonable_encoder(result.format_conversation()))

                graph_state.interview_results = result
            # 根据专家对话重新大纲
            await cl.Message(content="根据专家对话改进大纲").send()
            await node_refine_outline(
                RefineOutlineNodeRequest(
                    topic=graph_state.topic,
                    old_outline=graph_state.outline,
                    qa_results=qa_results,
                )
            )
            # 专家对话的结果, 以及引用的网址存入知识库(暂时跳过，因为还没完善)
            # await cl.Message(content="将专家对话的结果存入知识库").send()
            # ctx = get_mtmai_ctx()
            # vs = ctx.vectorstore
            # all_docs = []
            # for interview_state in graph_state.interview_results:
            #     reference_docs = [
            #         Document(page_content=v, metadata={"source": k})
            #         for k, v in interview_state.references.items()
            #     ]
            #     all_docs.extend(reference_docs)
            # await vs.aadd_documents(all_docs)

        # 根据大纲编写章节内容(TODO: 这里需要并发执行)
        await cl.Message(content="开始编写章节内容").send()
        all_sections = []
        for section in graph_state.outline.sections:
            a = await node_section_writer(
                NodeSectionWriterRequest(
                    topic=graph_state.topic,
                    outline=graph_state.outline,
                    section=section,
                )
            )
            all_sections.append(a)

        #         graph_state["interview_results"] = subjects.editors
        # await agent_event_stream_v2(model="storm", inputs=graph_state, debug=True)

    async def on_message(self, message: cl.Message):
        logger.info("TODO: on_message (ChatPostGenNode)")
        pass


async def step_hello2():
    async with cl.Step(name="TestStep2", type="llm") as step:
        step.input = "step_hello2 input"
        step.output = "step_hello2 output"
        await cl.Message(content="step_hello2 hello output").send()
