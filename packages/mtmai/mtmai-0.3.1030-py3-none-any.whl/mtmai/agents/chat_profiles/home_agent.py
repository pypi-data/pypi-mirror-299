from fastapi.encoders import jsonable_encoder
import mtmai.chainlit as cl
from mtmai.agents.chat_profiles.base_chat_agent import ChatAgentBase
from mtmai.chainlit.context import context
from mtmai.core.logging import get_logger
from mtmai.models.agent import ChatBotUiStateResponse, CopilotScreen
from mtmai.models.chat import ChatProfile

logger = get_logger()


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
        # TODO: langgraph 调用入口

        return {}

    @classmethod
    def name(cls):
        return "MainCopilotAgent"

    @classmethod
    def get_chat_profile(self):
        return ChatProfile(
            name="MainCopilotAgent",
            description="助手聊天机器人",
        )

    async def chat_start(self):


        await context.emitter.emit(
            "ui_state_upate",
            jsonable_encoder(
                ChatBotUiStateResponse(
                    layout="right_aside",
                    fabDisplayText="Mtm AI",
                    isOpenDataView=False,
                    activateViewName="/",
                    screens=[
                        CopilotScreen(
                            id="/",
                            label="首页",
                            Icon="home",
                        ),
                        CopilotScreen(
                            id="/datas",
                            label="数据",
                            Icon="data",
                        ),
                        # CopilotScreen(
                        #     id="/settings",
                        #     label="设置",
                        #     Icon="settings",
                        # ),
                        CopilotScreen(
                            id="/operation",
                            label="操作",
                            Icon="operation",
                        ),
                    ]
                )
            )
        )


    async def on_message(self, message: cl.Message):
        logger.info("TODO: on_message (ChatPostGenNode)")
        pass
