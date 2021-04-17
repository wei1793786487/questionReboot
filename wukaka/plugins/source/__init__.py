import time

from nonebot.command import CommandSession
from nonebot.plugin import on_command

from wukaka.plugins.source.data_source import findSource


@on_command('source', aliases=('排行榜'), only_to_me=False)
async def translate(session: CommandSession):
    user_id = session.event.user_id
    sources = await findSource(user_id)
    res = ""
    inx = 1
    for _source in sources:
        if (inx > 10):
            break
        res += "{}:{}({})=>{}分\n \n".format(inx, _source.get("name"),_source.get("id"), _source.get("source"))
        inx = inx + 1
    await session.send(res)
