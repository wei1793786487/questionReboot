
import re
from w3lib import html

def remove_tag(htmls):
    '''
     去除所有html标签
    :param htmls:
    :return:
    '''
    result = html.remove_tags(htmls).replace(" ","")  # 标签全部去除
    return  re.sub(r'（&.*?;）', "", re.sub(r'(&.*?;)', "", result))

def remove_tag_type(htmls):
    '''
    判断类型
    :return:
    '''
    try:
        if (type(htmls).__name__ == "list"):
            new_list = []
            for html in htmls:
                new_list.append(remove_tag(html))
            return new_list
        else:
            return remove_tag(htmls)
    except:
        print(htmls)
        pass