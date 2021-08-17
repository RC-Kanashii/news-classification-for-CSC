# coding:utf-8

import newspaper
import openpyxl


# ava_url_list：实际可以作为source的分类的网址
ava_url_list = ["https://www.meishichina.com/News/"] # 记得要改

# 白名单，如果url中出现了以下子串，则说明该新闻链接可能是所需要的
white_cat_list = ["h"] # 记得要改

# 黑名单，如果url中出现了以下子串，则会被跳过；黑名单优先级更高
black_cat_list = ["iqiyi", "photoview", "search", "media", "comment", "live", "room", "special", "video"]

# 每读取SAVE_CNT条新闻就保存一次，SAVE_CNT越大，执行效率越高，但是一旦中间出现意外可能会出现数据丢失的情况
SAVE_CNT = 5


def check_news_invalid(news):
    """
    检查新闻是否不合法
    :param news: 待检查的新闻
    :return: True, False
    """
    not_invalid = True
    for i in white_cat_list:
        if i in news.url:
            not_invalid = False
            break
    for i in black_cat_list:
        if i in news.url:
            not_invalid = True
            break
    if len(news.text) < 20 or len(news.title) <= 5:
        not_invalid = True
    return not_invalid


def export2excel(news_info, excel_name):
    """
    把新闻的信息追加到excel工作簿对应分类表格的后面
    :param news_info: 新闻信息，是个列表:[正文,分类,标题]
    :param excel_name: excel工作簿名字
    :return: None
    """
    workbook = openpyxl.load_workbook(excel_name)
    for tmp_news_info in news_info:
        cat = tmp_news_info[1]
        table = workbook[cat]
        table.append(tmp_news_info)
    workbook.save(excel_name)


def catch_news():
    """
    抓取新闻
    :return: None
    """
    for cat_url in ava_url_list:
        news_info = []  # 共有SAVE_CNT篇新闻，稍后会被追加到excel表格中
        # 把当前的分类板块的url作为新闻源
        news_source = newspaper.build(cat_url,  # 各个板块的链接
                                      language="zh",  # 语言
                                      memoize_articles=False,  # 是否要记忆已经访问过的文章
                                      fetch_images=False  # 是否要获取图片
                                      )
        print("该分类", cat_url, "下共有", news_source.size(), "条新闻")
        news_list = news_source.articles
        for news in news_list:
            try:
                cat_name = "其他" # 分类名字，记得要改
                news.download()
                news.parse()
                url = news.url
                # 去掉一些无效链接和重复的链接
                if check_news_invalid(news):
                    continue
                print(url)
                tmp_news_info = [news.text.replace("\n", ""),
                                 cat_name,
                                 news.title.split("--")[0].strip()]  # 单篇新闻的内容、类别、标题，稍后会被追加到news_info中
                news_info.append(list(tmp_news_info))
                print(tmp_news_info)
                tmp_news_info.clear()  # 记得清空临时存储单条新闻的列表
                if len(news_info) >= SAVE_CNT:
                    print("保存", SAVE_CNT, "条新闻")
                    # export2excel(news_info, "新闻文本分类算法样本集 - 美食天下 "+cat_name+".xlsx")  # 保存到对应名称的excel工作簿中
                    news_info.clear()  # 保存完了以后要清空news_info
            except Exception as e:
                print(e)
                continue


if __name__ == "__main__":
    catch_news()