from nonebot import on_request, RequestSession, on_notice, NoticeSession


# 将函数注册为群请求处理器
@on_request('group')
async def _(session: RequestSession):
    if (session.event.get("sub_type") == "invite"):
        # 加群处理
        await session.approve()
    if (session.event.get("sub_type") == "increase"):
        await session.send('欢迎新朋友～,我是答题机器人，你可以跟我说出题,我来给你出题哦')


