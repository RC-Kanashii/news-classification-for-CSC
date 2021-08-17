# import newspaper
# url = 'http://www.southcn.com/'      # 南方网
# south_paper = newspaper.build(url,language='zh',memoize_articles = False)    # 构建新闻源
# print(south_paper.size())
# for category in south_paper.category_urls():
#     print(category)
# # 提取源新闻网站的品牌和描述
# print('品牌：',south_paper.brand)  # 品牌
# print('描述：',south_paper.description) # 描述

# import newspaper
# url = 'http://www.people.com.cn/'
# people_paper = newspaper.build(url,language='zh',memoize_articles = False)   #构建人民网新闻源
# print(people_paper.size())
# for category in people_paper.category_urls():
#     print(category)
# print('品牌：',people_paper.brand)  # 品牌
# print('描述：',people_paper.description) # 描述
# a=0
# for article in people_paper.articles:
#     print(article.url)
#     a = a+1
# print(a)      # 查看新闻链接的数量，与south_paper.size()一致


# lidong1979.blog.hexun.com
# house.hexun.com
# cpc.people.com.cn---党政

# http://world.people.com.cn/n1/2021/0308/c1002-32045728.html
## 用Article爬取单条新闻




# from newspaper import Article
# # 目标新闻网址
# url = 'http://world.people.com.cn/n1/2021/0308/c1002-32045728.html'
# news = Article(url, language='zh')
# news.download()        # 加载网页
# news.parse()           # 解析网页
# print('题目：',news.title)       # 新闻题目
# print('正文：\n',news.text)      # 正文内容
# print(news.authors)     # 新闻作者
# print(news.keywords)    # 新闻关键词
# print(news.summary)     # 新闻摘要
# print(news.top_image) # 配图地址
# print(news.movies)    # 视频地址
# print(news.publish_date) # 发布日期
# print(news.html)      # 网页源代





# import pandas as pd         # 导入pandas库
# news_title = []
# news_text = []
# news = south_paper.articles
# for i in range(len(news)):    # 以新闻链接的长度为循环次数
#     paper = news[i]
#     try :
#         paper.download()
#         paper.parse()
#         news_title.append(paper.title)     # 将新闻题目以列表形式逐一储存
#         news_text.append(paper.text)       # 将新闻正文以列表形式逐一储存
#     except:
#         news_title.append('NULL')          # 如果无法访问，以NULL替代
#         news_text.append('NULL')
#         continue
# # 建立数据表存储爬取的新闻信息
# south_paper_data = pd.DataFrame({'title':news_title,'text':news_text})
# print(south_paper_data)


# 000000000中文版0000000000000

cat_list = ["http://finance.people.com.cn","http://house.people.com.cn","http://edu.people.com.cn","http://scitech.people.com.cn","http://military.people.com.cn","http://auto.people.com.cn/","http://ent.people.com.cn","http://game.people.com.cn/","http://media.people.com.cn/","http://cpc.people.com.cn/",""]
channelName = ["财经","房产","教育","科技","军事","汽车","体育","游戏","娱乐","其他"]

# import newspaper
#
# people = newspaper.build("http://finance.people.com.cn", language="zh")
#
# # for category in people.category_urls():
# #     print(category)
#
# news = people.articles
# print(news[0].url)
# for i in news:
#     try:
#
#         i.download()
#         i.parse()
#         print(i.url)
#         # for cat_index in range(len(cat_list)):
#         #     if cat_list[cat_index] in i.url:
#         #         print("分类为：", cat_list)
#
#     except Exception as e:
#         print(e)
#         continue







import newspaper
people = newspaper.build('http://www.people.com.cn/', language='zh', memoize_articles = False)
print("新闻数量：", people.size())
import pandas as pd         # 导入pandas库
news_title = []
news_text = []
news = people.articles

article_info = []
for i in range (len(news)):         #以新闻链接长度为循环次数
    paper = news[i]
    try:
        paper.download()
        paper.parse()
        print(paper.url,type(paper.url))
        for cat_index in range(len(cat_list)):
            if cat_list[cat_index] in paper.url:
                print("分类为：", cat_index)
                break
        # print("标题：",paper.title)
        # print("正文：",paper.text)
        article_info.append(paper.text)
        article_info.append(channelName[cat_index])
        article_info.append(paper.title.split("--")[0].strip())
        print(article_info)
        article_info.clear()
        # if "finance" in paper.url:
        #     print("finance yes!")

        # news_title.append(paper.title)
        # news_text.append(paper.text)       # 将新闻正文以列表形式逐一储存
    except:
        # news_title.append('NULL')          # 如果无法访问，以NULL替代
        # news_text.append('NULL')
        continue