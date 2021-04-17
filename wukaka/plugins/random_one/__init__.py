import time

from nonebot.command import CommandSession
from nonebot.command.argfilter import extractors, controllers, validators
from nonebot.plugin import on_command

from wukaka.plugins.random_one.data_source import random_question
from wukaka.plugins.random_one.mongo import addRanking


@on_command('question', aliases=('出题'), only_to_me=False)
async def translate(session: CommandSession):
    subject = await session.aget('subject', prompt='你想啥样的类型？',
                                 arg_filters=[
                                     extractors.extract_text,  # 取纯文本部分
                                     controllers.handle_cancellation(session),  # 处理用户可能的取消指令
                                     str.strip  # 去掉两边空白字符
                                 ]
                                 )
    if subject == "数学":
        await session.finish("数学题目属于图片，暂时发不出来")
    elif subject not in ["语文", "数学", "计算机", "英语", "政治"]:
        await session.finish("不支持你所输入的科目,仅支持语文，数学，计算机，英语，政治")
        question = {}

    while True:
        try:
            question = await random_question(subject)
            while question == {}:
                question = await random_question(subject)
            print(question)
            print(question == {})
            types = question.get("type")
            # 随机题库
            anwser = "随机的题库为:《{}》\n{}\n \n".format(question.get("title"), question.get("question"))
            gets = question.get("choose")

            if (types != 3):
                if (type(gets).__name__ == "list"):
                    if (len(gets)) != 0:
                        inx = 0
                        for choose in gets:
                            anwser = anwser + tran_numer_to_char(inx) + ":" + choose + "\n"
                            inx = inx + 1
                else:
                    anwser = anwser + gets + "\n"

            await session.send(anwser)
            isFigth = False
            rigth_number = 0

            # 正确与错误判断逻辑
            if (types == 1):
                # 单选题逻辑
                user_anwser = await session.aget('ansser', prompt='这是一道选择题,请输入你的答案 ',
                                                 arg_filters=[
                                                     extractors.extract_text,  # 取纯文本部分
                                                     controllers.handle_cancellation(session),  # 处理用户可能的取消指令
                                                     str.strip,  # 去掉两边空白字符
                                                     validators.match_regex(r'^[a,b,c,d,A,B,C,D]$', '请输入a b c d'),
                                                 ]
                                                 )
                print(user_anwser)
                upper = str.upper(user_anwser)
                number_inx = int(question.get("question_standard_answer"))
                number = tran_numer_to_char(number_inx)
                print("答案是{}".format(number))
                if (upper == number):
                    isFigth = True
                else:
                    rigth_number = number
                # await session.send("这是一道选择题,请输入前面的索引 如1,2,3,4")
            elif (types == 2):
                print("多选")
                # 多选题逻辑
                user_anwsers = await session.aget('ansser', prompt='这是一道多选题,请输入你的答案,以空格分割。 ',
                                                  arg_filters=[
                                                      extractors.extract_text,  # 取纯文本部分
                                                      controllers.handle_cancellation(session),  # 处理用户可能的取消指令
                                                      str.strip,  # 去掉两边空白字符
                                                  ]
                                                  )
                tran_user_anwser = []
                # 正确答案转换为abc
                tran_str_answser = []
                str_anwsers = str.split(replace_to_arry(question.get("question_standard_answer")),",")
                for str_anwser_one in str_anwsers:
                    tran_str_answser.append(tran_numer_to_char(int(str_anwser_one)))

                # 将用户的回答转换，排序
                strip_anwser_list = user_anwsers.split(" ")
                print(strip_anwser_list)
                for strip_anwser in strip_anwser_list:
                    tran_user_anwser.append(str.upper(strip_anwser))

                tran_user_anwser.sort()

                if (tran_user_anwser == tran_str_answser):
                    isFigth = True
                else:
                    rigth_number = tran_str_answser

            elif (types == 3):
                # 填空题逻辑
                user_anwsers = await session.aget('ansser', prompt='这是一道填空题,请输入你的答案 ',
                                                  arg_filters=[
                                                      extractors.extract_text,  # 取纯文本部分
                                                      controllers.handle_cancellation(session),  # 处理用户可能的取消指令
                                                      str.strip,  # 去掉两边空白字符
                                                  ]
                                                  )
                replace =question.get("question_standard_answer")
                if(user_anwsers==replace):
                    isFigth = True
                else:
                    rigth_number = replace

            else:
                await session.send("sorry，现在只支持单选题")

            if isFigth:
                await session.send("恭喜您答对了,\n这道题目的解析是\n{}".format(question.get("question_analyze")))
                sender = session.event.sender
                addRanking(sender.get("user_id"), sender.get("nickname"))
            else:
                await session.send(
                    "抱歉你回答错了,\n正确答案是{},\n这道题目的解析是\n{}".format(rigth_number, question.get("question_analyze")))
            session.state.pop("ansser")
            time.sleep(2)
        except Exception:
            print(Exception.__name__)
            session.finish("让我休息0.00001秒")
            # pass


def tran_numer_to_char(number: int):
    CAHR = ["A", "B", "C", "D", "E", "F", "G", "H"]
    return CAHR[number]

def replace_to_arry(str_string:str):
    # 我是彩笔
    return str_string.replace("[","").replace("]","").replace('"',"")
