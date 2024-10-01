"""
GraphIterator Module
"""

import uuid

from matplotlib.offsetbox import TextArea

import mtmai.chainlit as cl
from mtmai.agents.chat_profiles.base_chat_agent import ChatAgentBase
from mtmai.chainlit.chat_settings import ThreadForm
from mtmai.chainlit.context import context
from mtmai.core.db import get_async_session
from mtmai.core.logging import get_logger
from mtmai.crud.curd_site import get_site_by_id
from mtmai.models.chat import ChatProfile
from mtmai.mtlibs.inputs.input_widget import TextArea, TextInput
from mtmscreentocode.routes.evals import Eval

logger = get_logger()


class MainCopilotAgent(ChatAgentBase):
    """
    站点配置Agent
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
        return "MainCopilotAgent"

    @classmethod
    def get_chat_profile(self):
        return ChatProfile(
            name="MainCopilotAgent",
            description="默认主聊天机器人",
        )

    async def chat_start(self):
        js_code_get_detail_info = """
var results = {};
results.fullUrl=window.location.href;
results.cookie=document.cookie;
results.title=document.title;
results.body=document.body.innerText;
(function() { return results; })();
"""
        js_eval_result = await context.emitter.send_call_fn("js_eval", {"code": js_code_get_detail_info})
        logger.info("js_eval_result %s", js_eval_result)
        # 调用函数检测环境

        # async with get_async_session() as session:
        #     site = await get_site_by_id(session, uuid.UUID(siteId))
        # demo_fn_call_result = await context.emitter.send_form(
        #     ThreadForm(
        #         open=True,
        #         inputs=[
        #             TextInput(
        #                 name="title",
        #                 label="站点名称",
        #                 placeholder="请输入站点名称",
        #                 description="站点名称",
        #                 value=site.title,
        #             ),
        #             TextArea(
        #                 name="description",
        #                 label="站点描述",
        #                 placeholder="请输入站点描述",
        #                 description="站点描述",
        #                 value=site.description,
        #             ),
        #         ],
        #     )
        # )
        # logger.info("表单调用结果 %s", demo_fn_call_result)
        # async with get_async_session() as session:
        #     # item = Site.model_validate(demo_fn_call_result)
        #     # site.update(demo_fn_call_result)
        #     site.sqlmodel_update(site.model_dump(), update=demo_fn_call_result)
        #     session.add(site)
        #     await session.commit()
        #     await session.refresh(site)
        # await context.emitter.emit("clear_ask_form", {})
        # res = await cl.AskUserMessage(content="What is your name?", timeout=10).send()
        # if res:
        #     await cl.Message(
        #         content="Continue!",
        #     ).send()

    async def on_message(self, message: cl.Message):
        logger.info("TODO: on_message (ChatPostGenNode)")
        pass
