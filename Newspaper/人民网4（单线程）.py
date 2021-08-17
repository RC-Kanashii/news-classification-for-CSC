# coding:utf-8

import newspaper
import openpyxl

# cat_list：各个分类的网址，同时也是判断一篇文章类别的依据
cat_url_list = ["http://finance.people.com.cn",  # 财经
                "http://house.people.com.cn",  # 房产
                "http://edu.people.com.cn",  # 教育
                "http://scitech.people.com.cn",  # 科技
                "http://military.people.com.cn",  # 军事
                "http://auto.people.com.cn/",  # 汽车
                "http://ent.people.com.cn",  # 体育
                "http://game.people.com.cn/",  # 游戏
                "http://media.people.com.cn/",  # 娱乐
                "http://cpc.people.com.cn/",  # 其他（凡是“娱乐”后面的分类都归属于“其他”，不限种数）
                "http://env.people.com.cn/",  # 其他
                "http://health.people.com.cn/"]  # 其他

# ava_url_list：实际可以作为source的分类的网址，也就是上面cat_url_list中各链接的根目录
ava_url_list = ["http://finance.people.com.cn",
                "http://house.people.com.cn",
                "http://edu.people.com.cn",
                "http://military.people.com.cn",
                "http://cpc.people.com.cn/"]

# channel_name：分类的名称
channel_name = ["财经", "房产", "教育", "科技", "军事", "汽车", "体育", "游戏", "娱乐", "其他"]

# 每读取SAVE_CNT条新闻就保存一次，SAVE_CNT越大，执行效率越高，但是一旦中间出现意外可能会出现数据丢失的情况
SAVE_CNT = 10


def check_news_invalid(news):
    """
    检查新闻是否不合法
    :param news: 待检查的新闻
    :return: True, False
    """
    return "index.html" in news.url \
           or " " in news.url \
           or "#liuyan" in news.url \
           or len(news.text) < 20 \
           or len(news.title.split("--")[0].strip()) <= 5


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


def get_cat(url):
    """
    获取新闻的类别
    :param url: 新闻的url
    :return: int cat_index，表示channel_name中对应类别的下标
    """
    for i in range(len(cat_url_list)):
        if i >= 9:
            cat_index = 9  # 把下标大于等于9的新闻归为“其他”
        else:
            cat_index = i
        if cat_url_list[i] in url:
            print("分类为：", channel_name[cat_index])
            is_valid = True
            break
    return cat_index


def catch_news():
    """
    抓取新闻
    :return: None
    """
    for cat_url in ava_url_list:
        news_info = []  # 共有SAVE_CNT篇新闻，稍后会被追加到excel表格中
        is_valid = False  # 该篇新闻是否在给定的分类里，初始值为False
        # 把当前的分类板块的url作为新闻源
        news_source = newspaper.build(cat_url,  # 各个板块的链接
                                      language="zh",  # 语言
                                      memoize_articles=False,  # 是否要记忆已经访问过的文章
                                      fetch_images=False  # 是否要获取图片
                                      )
        news_list = news_source.articles
        for news in news_list:
            try:
                news.download()
                news.parse()
                url = news.url
                # 去掉一些无效链接和重复的链接
                if check_news_invalid(news):
                    continue
                for i in range(len(cat_url_list)):
                    if i >= 9:
                        cat_index = 9  # 把下标大于等于9的新闻归为“其他”
                    else:
                        cat_index = i
                    if cat_url_list[i] in url:
                        is_valid = True  # 说明该分类下的新闻是我们所需要的
                        break
                if is_valid:  # 如果新闻的类别是我们所需要的
                    print(url)
                    print("分类为：", channel_name[cat_index])
                    tmp_news_info = [news.text.replace("\n", ""),
                                     channel_name[cat_index],
                                     news.title.split("--")[0].strip()]  # 单篇新闻的内容、类别、标题，稍后会被追加到news_info中
                    news_info.append(list(tmp_news_info))
                    print(tmp_news_info)
                    tmp_news_info.clear()  # 记得清空临时存储单条新闻的列表
                    if len(news_info) >= SAVE_CNT:
                        print("保存", SAVE_CNT, "条新闻")
                        export2excel(news_info, "新闻文本分类算法样本集 - 副本.xlsx")  # 保存到对应名称的excel工作簿中
                        news_info.clear()  # 保存完了以后要清空news_info
                else:
                    print("该新闻不是所需要的：", url)
            except Exception as e:
                print(e)
                continue
            finally:
                is_valid = False


if __name__ == "__main__":
    catch_news()
