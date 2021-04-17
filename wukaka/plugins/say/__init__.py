import random
from _ast import Expression

from aiocqhttp import MessageSegment
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from nonebot.command.argfilter import extractors, controllers

from wukaka.plugins.say.data_source import findSource


@on_command('langue')
async def weather(session: CommandSession):
    txt = session.event.raw_message
    source = findSource(txt)
    count = source.count()
    randint=0
    if(count!=0):
        randint = random.randint(0, count - 1)
    if(count!=0):
        source = source[randint]
        await session.send(source.get("anwser"),at_sender=True)



@on_natural_language(only_to_me=False)
async def _(session: NLPSession):
    return IntentCommand(100.0, 'langue')


@on_command('study', aliases=('学习'))
async def weather(session: CommandSession):
    stu_msg = await session.aget('stu_msg', prompt='你想让他记录的句子是？',
                                 arg_filters=[
                                     str.strip,  # 去掉两边空白字符
                                     controllers.handle_cancellation(session),  # 处理用户可能的取消指令
                                 ]
                                 )

    # source = data_source.findSource(stu_msg)
    # if(source!=None):
    #     session.state.pop("stu_msg")
    #     session.pause('这句话我已经知道怎么回复了哦')
    stu_anwser = await session.aget('stu_anwser', prompt='你想让他回复的的句子是？',
                                 arg_filters=[
                                     str.strip,  # 去掉两边空白字符
                                     controllers.handle_cancellation(session),  # 处理用户可能的取消指令
                                 ]
                                 )
    one = data_source.insert_one(stu_msg, stu_anwser, session.event.user_id)
    await session.send("俺知道了",at_sender=True)