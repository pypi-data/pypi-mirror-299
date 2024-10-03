from pydantic import BaseModel


class ThreadUIState(BaseModel):
    """ThreadView 的UI 状态"""

    enableChat: bool | None = False
    enableScrollToBottom: bool = True
    title: str | None = None
    description: str | None = None
    icons: str | None = None
    layout: str | None = None
    theme: str | None = None

