# coding:utf-8


import os
from pyhanlp.static import STATIC_ROOT
from pyhanlp.static import download, remove_file, HANLP_DATA_PATH


sogou_corpus_path = "过滤标点、英语、数字 新闻文本分类算法样本集+人民网+网易+旅兴网+读书网+美食台+美食天下+新浪+中华网+铁血+军事前沿+西陆+搜狗新闻库+数码科技网+科技快报网"#"新闻库（过滤停用词）"


## ===============================================
## 以下开始 支持向量机SVM


def install_jar(name, url):
    dst = os.path.join(STATIC_ROOT, name)
    if os.path.isfile(dst):
        return dst
    download(url, dst)
    return dst


install_jar('text-classification-svm-1.0.2.jar', 'http://file.hankcs.com/bin/text-classification-svm-1.0.2.jar')
install_jar('liblinear-1.95.jar', 'http://file.hankcs.com/bin/liblinear-1.95.jar')
from pyhanlp import *

LinearSVMClassifier = SafeJClass('com.hankcs.hanlp.classification.classifiers.LinearSVMClassifier')
IOUtil = SafeJClass('com.hankcs.hanlp.corpus.io.IOUtil')
FileDataSet = SafeJClass('com.hankcs.hanlp.classification.corpus.FileDataSet')
MemoryDataSet = SafeJClass('com.hankcs.hanlp.classification.corpus.MemoryDataSet')
Evaluator = JClass('com.hankcs.hanlp.classification.statistics.evaluations.Evaluator')
# LinearSVMClassifier = JClass('com.hankcs.hanlp.classification.classifiers.LinearSVMClassifier')
BigramTokenizer = SafeJClass('com.hankcs.hanlp.classification.tokenizers.BigramTokenizer')

def train_or_load_classifier222():
    model_path = sogou_corpus_path + '.svm.ser'
    if os.path.isfile(model_path):
        return LinearSVMClassifier(IOUtil.readObjectFrom(model_path))
    classifier = LinearSVMClassifier()
    classifier.train(sogou_corpus_path)
    model = classifier.getModel()
    IOUtil.saveObjectTo(model, model_path)
    return LinearSVMClassifier(model)


def train_or_load_classifier():
    model_path = sogou_corpus_path + '.2gram.ser'
    if os.path.isfile(model_path):
        return LinearSVMClassifier(IOUtil.readObjectFrom(model_path))
    classifier = LinearSVMClassifier()
    classifier.train(sogou_corpus_path)
    model = classifier.getModel()
    IOUtil.saveObjectTo(model, model_path)
    return LinearSVMClassifier(model)


def evaluate(classifier, tokenizer):
    training_corpus = FileDataSet().setTokenizer(tokenizer).load(sogou_corpus_path, "UTF-8", 0.9)
    classifier.train(training_corpus)
    testing_corpus = MemoryDataSet(classifier.getModel()).load(sogou_corpus_path, "UTF-8", -0.1)
    result = Evaluator.evaluate(classifier, testing_corpus)
    print(classifier.getClass().getSimpleName() + "+" + tokenizer.getClass().getSimpleName())
    print(result)
    print("F1_score为：", result.average_f1)

def predict(classifier, text):
    print("《%16s》\t属于分类\t【%s】" % (text, classifier.classify(text)))
    print("各类别概率：")
    predict_dict = classifier.classify(text)
    for cat in predict_dict:
        print(cat, round(predict_dict[cat]*100, 2))
    # 如需获取离散型随机变量的分布，请使用predict接口
    # print("《%16s》\t属于分类\t【%s】" % (text, classifier.predict(text)))


if __name__ == '__main__':
    print("读取或训练模型……")
    classifier = train_or_load_classifier()
    print("评价模型")
    evaluate(classifier, BigramTokenizer())
    print("开始预测")
    # predict(classifier, "张文木做客观察者网：解决台湾问题，现在各种条件都越来越成熟了")
    # predict(classifier, "小度推智能屏品牌“添添”，称要把用户在手机上的需求抢过来")
    # predict(classifier, "牧原股份：生猪行业将在明后年触底，做好迎接行业冬天的准备")
    # predict(classifier, "勇士无缘季后赛！但NBA应该感谢库里，他拯救了这个赛季")
    # predict(classifier, "最高法力纠超标查封问题：诉讼保全应秉持善意文明执行理念")
    predict(classifier, "中经联盟专家走进财富港活动圆满落幕来源：北京楼讯5月20日，以“汇智|谋进|共赢”为主题的“中经联盟专家走进财富港”活动圆满举行。当日中经联盟专家、以及国内房地产行业各专业领域的权威嘉宾坐镇活动现场。就北京城市副中心、京津冀发展趋势、商办市场趋势等话题进行了深入探讨，通过精深对话，聚焦行业痛点，共谋区域红利，赋能价值共生。此大会也见证了财富港与中经联盟战略合作正式启动，共同解锁绿色商务创新地产新模式。大会伊始，华北世茂京津片区总经理刘垚代表主办方致辞，向中经联盟及与会嘉宾表示热烈欢迎。他表示，目前商办市场行业整体开始逐步进入新一轮发展周期，市场活跃度也将稳步提升。财富港项目，赋予商务办公新的功能，在区域内商办市场高端占位，为新经济企业提供对标国际一流的商务平台。且以其稀缺的产品形态和广阔的发展前景，成为了国内外知名企业争相入驻的热土，开创新型生态办公商务新时代。")
    predict(classifier, "俄媒：俄成功试射最新型洲际弹道导弹 没有细节公开。[环球网军事报道]塔斯社28日报道，据俄罗斯国防工业界的一名消息人士周一称，俄罗斯最新型洲际弹道导弹试射成功。报道称，该消息人士透露，在6月中旬，这种由莫斯科热工技术研究所开发，独特的最新型弹道导弹在普列谢茨克成功试射。不过对于这一消息，塔斯社尚未得到该研究所的官方评论。目前也没有关于这款最新型洲际导弹的进一步消息。")
    predict(classifier, "外媒：苹果要求部分员工佩戴警用级随身摄像头，以防止产品泄密。据外媒 frontpagetech，苹果要求部分员工佩戴警用级别的随身摄像头，类似执法记录仪，以防止员工进行泄密。外媒表示，这一举措已在苹果内部实施了几个星期，目前仅限于部分涉密团队，并没有广泛采用。IT之家了解到，苹果近期向许多爆料者发送了律师函，警告他们不得泄露未发布的苹果项目的信息，因为这可能会给苹果的竞争对手提供有价值的信息，同时也会“误导客户，因为披露的内容可能不准确。”")
    predict(classifier, "革命者》聚焦李大钊革命生平 22城开启主题观影。新浪娱乐讯 电影《革命者》于6月26日-27日，在全国22所城市开启限量超前党员主题观影。影片由知名导演管虎监制、青年导演徐展雄执导，梁静任总制片人，张颂文、李易峰、佟丽娅领衔主演，彭昱畅、韩庚、李九霄、白客、秦昊、于谦等特别出演（按照影片中出场顺序），孙浠伦、章若楠、辛云来、朱梓瑜、张承等主演（按照影片中出场顺序）。电影《革命者》在前期筹备、剧本创作、史料调研等各环节深耕细作，深入李大钊故乡河北省唐山市乐亭县采访采风。演员方面，电影经过层层反复筛选，综合李大钊的个人外在形象和内在精神品格，最终敲定了由演员张颂文出演“李大钊”一角。为了演好这个角色，张颂文仔细研读李大钊过往文章，钻研李大钊的神态举止，领悟李大钊的精神世界，力求在外部形象、动作神态、内在灵魂上还原一个鲜活立体的李大钊。")
    predict(classifier, "北京初中学考6月24日开考 7月5日起可查成绩。新京报讯（记者 杨菲菲）2021年北京市初中学业水平考试将于6月24日至27日举行。6月22日，北京教育考试院发布提醒，备考期间，考生要劳逸结合，配合学校做好考前健康监测，以平常心态迎接考试；同时，考生和家长要提前关注交通信息，确保准时到达考点。8.5万初三学生参加考试，7月5日可查成绩6月24日至26日为初三年级学考时间，开考科目包括语文、数学、外语、历史、道德与法治、物理和化学7科。全市共安排考点198个，备用考点20个。8.5万初三学生将参加此次考试。6月27日为初二年级学考时间，考试科目为地理和生物两科。")
    predict(classifier, "国内首款正版授权俄罗斯方块手游《俄罗斯方块环游记》定档7月！今日，由畅游聚变工作室打造，腾讯代理的国内唯一正版授权的俄罗斯方块手游——《俄罗斯方块环游记》正式宣布定档，将于2021年7月与各位俄罗斯方块爱好者正式见面。在俄罗斯方块环游记中，大家可以体验到过去30余年全世界最经典的俄罗斯方块玩法，也可以进入竞技场，随时随地和其他玩家来一场紧张激烈的方块对决！童年时那些有关于方块消行的记忆正在等待你唤醒。俄罗斯方块之父倾情推荐，国内唯一正版授权手游。说到俄罗斯方块，想必大家都不陌生。1984年6月，在俄罗斯科学院计算机中心工作的电脑工程师阿列克谢·帕基特诺夫从拼图游戏里得到灵感，利用空闲时间编出一个游戏程序，这就是最初的俄罗斯方块。时光飞逝，距大家初次见到俄罗斯方块已经过去三十余年，在这些年内，俄罗斯方块发展出了各式各样的玩法，也创造了一个个让人难以想象的历史记录。")
    predict(classifier, """新华社达喀尔10月15日电（记者邢建桥）巴马科消息：联合国马里多层面综合稳定特派团（马里稳定团）15日发表新闻公报说，一名维和士兵当天在马里东北部基达尔省执行任务时遇袭身亡。    公报说，一辆载有马里稳定团维和士兵的车辆当天在距基达尔省首府基达尔市50公里处遭遇爆炸袭击。袭击造成1人死亡、1人重伤，伤者已被送往医疗机构接受治疗。公报未透露这两名维和士兵的国籍。    公报强烈谴责针对联合国人员、马里和国际部队，以及无辜平民的无差别袭击。马里稳定团团长安纳迪夫在公报中表示，马里稳定团将继续致力于支持马里人民和政府重获持久和平的努力。    这是今年以来第三起马里稳定团维和人员遇袭身亡事件。今年5月和6月，分别有3名和2名维和人员在执行任务时遇袭身亡。    2012年3月，马里发生军事政变。2013年4月，联合国安理会通过决议，决定设立马里稳定团。2015年5月，马里政府与北部地区部分武装组织签署《和平与和解协议》。同年6月，各方完成协议最终签署。然而，马里北部地区近年来一直冲突不断，中部地区的武装袭击也有增多趋势。""")
