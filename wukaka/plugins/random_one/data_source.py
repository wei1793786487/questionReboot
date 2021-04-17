import random

from .beauty import remove_tag_type
from .mongo import findQlistLike, findQusone


async def random_question(subject):
    subjects = ["语文", "数学", "计算机", "英语","政治"]
    try:
        if ( subject  in subjects):
            like = findQlistLike(subject, 0)
            randint = random.randint(0, like.count()-1)
            rand_question= like[randint]
            # print("随机的题库是{}".format(rand_question.get("title")))
            # 寻找该题库里面的题
            question_type = random.randint(1, 2)
            qusone = findQusone(rand_question.get("question"),question_type)
            # 生成随机一个题目索引
            randint = random.randint(0, qusone.count()-1)
            rand_question_ = qusone[randint]
            type=qusone[randint].get("question_types")
            tag = remove_tag_type(qusone[randint].get("question"))
            choose = remove_tag_type(qusone[randint].get("answer"))
            question_standard_answer = remove_tag_type(qusone[randint].get("question_standard_answer"))
            question_standard = remove_tag_type(qusone[randint].get("question_analyze"))
            # print("选项是:{}".format(choose))
            # print("答案是:{}".format(question_standard_answer))
            # print(tag)
            return {
                "title": rand_question.get("title"),
                "question":tag,
                "choose":choose,
                "question_standard_answer":question_standard_answer,
                "type":type,
                "question_analyze":question_standard

            }
        else:
            return {}
    except:
        return {}
        pass


