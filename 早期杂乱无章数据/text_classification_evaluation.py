# coding:gbk
from pyhanlp import *
import zipfile
import os
from pyhanlp.static import download, remove_file, HANLP_DATA_PATH


def test_data_path():
    """
    ��ȡ��������·����λ��$root/data/test����Ŀ¼�������ļ�ָ����
    :return:
    """
    data_path = os.path.join(HANLP_DATA_PATH, 'test')
    if not os.path.isdir(data_path):
        os.mkdir(data_path)
    return data_path


## ��֤�Ƿ�������Ͽ⣬���û���Զ�����
def ensure_data(data_name, data_url):
    root_path = test_data_path()
    dest_path = os.path.join(root_path, data_name)
    if os.path.exists(dest_path):
        return dest_path

    if data_url.endswith('.zip'):
        dest_path += '.zip'
    download(data_url, dest_path)
    if data_url.endswith('.zip'):
        with zipfile.ZipFile(dest_path, "r") as archive:
            archive.extractall(root_path)
        remove_file(dest_path)
        dest_path = dest_path[:-len('.zip')]
    return dest_path


sogou_corpus_path = ensure_data('�ѹ��ı��������Ͽ������',
                                'http://file.hankcs.com/corpus/sogou-text-classification-corpus-mini.zip')

## ===============================================
## ���¿�ʼ ��׼������ ���ر�Ҷ˹ �� SVM ������

IClassifier = JClass('com.hankcs.hanlp.classification.classifiers.IClassifier')
NaiveBayesClassifier = JClass('com.hankcs.hanlp.classification.classifiers.NaiveBayesClassifier')
LinearSVMClassifier = JClass('com.hankcs.hanlp.classification.classifiers.LinearSVMClassifier')
FileDataSet = JClass('com.hankcs.hanlp.classification.corpus.FileDataSet')
IDataSet = JClass('com.hankcs.hanlp.classification.corpus.IDataSet')
MemoryDataSet = JClass('com.hankcs.hanlp.classification.corpus.MemoryDataSet')
Evaluator = JClass('com.hankcs.hanlp.classification.statistics.evaluations.Evaluator')
FMeasure = JClass('com.hankcs.hanlp.classification.statistics.evaluations.FMeasure')
BigramTokenizer = JClass('com.hankcs.hanlp.classification.tokenizers.BigramTokenizer')
HanLPTokenizer = JClass('com.hankcs.hanlp.classification.tokenizers.HanLPTokenizer')
ITokenizer = JClass('com.hankcs.hanlp.classification.tokenizers.ITokenizer')


def evaluate(classifier, tokenizer):
    training_corpus = FileDataSet().setTokenizer(tokenizer).load(sogou_corpus_path, "UTF-8", 0.9)
    classifier.train(training_corpus)
    testing_corpus = MemoryDataSet(classifier.getModel()).load(sogou_corpus_path, "UTF-8", -0.1)
    result = Evaluator.evaluate(classifier, testing_corpus)
    print(classifier.getClass().getSimpleName() + "+" + tokenizer.getClass().getSimpleName())
    print(result)


if __name__ == '__main__':
    evaluate(NaiveBayesClassifier(), HanLPTokenizer())
    evaluate(NaiveBayesClassifier(), BigramTokenizer())
    evaluate(LinearSVMClassifier(), HanLPTokenizer())
    evaluate(LinearSVMClassifier(), BigramTokenizer())