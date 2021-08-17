import os
from pyhanlp.static import STATIC_ROOT
from pyhanlp.static import download, remove_file, HANLP_DATA_PATH


sogou_corpus_path = "新闻库"#"新闻库（过滤停用词）"


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
LinearSVMClassifier = JClass('com.hankcs.hanlp.classification.classifiers.LinearSVMClassifier')
BigramTokenizer = SafeJClass('com.hankcs.hanlp.classification.tokenizers.BigramTokenizer')

def train_or_load_classifier():
    model_path = sogou_corpus_path + '.svm.ser'
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
    # 如需获取离散型随机变量的分布，请使用predict接口
    # print("《%16s》\t属于分类\t【%s】" % (text, classifier.predict(text)))


if __name__ == '__main__':
    classifier = train_or_load_classifier()
    predict(classifier, "张文木做客观察者网：解决台湾问题，现在各种条件都越来越成熟了")
    predict(classifier, "小度推智能屏品牌“添添”，称要把用户在手机上的需求抢过来")
    predict(classifier, "牧原股份：生猪行业将在明后年触底，做好迎接行业冬天的准备")
    predict(classifier, "勇士无缘季后赛！但NBA应该感谢库里，他拯救了这个赛季")
    predict(classifier, "最高法力纠超标查封问题：诉讼保全应秉持善意文明执行理念")
    evaluate(classifier, BigramTokenizer())