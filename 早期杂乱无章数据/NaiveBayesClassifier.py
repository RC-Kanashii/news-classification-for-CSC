# coding=gbk
from pyhanlp import SafeJClass

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


## ��֤�Ƿ���� MSR���Ͽ⣬���û���Զ�����
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
## ���¿�ʼ���ر�Ҷ˹����


NaiveBayesClassifier = SafeJClass('com.hankcs.hanlp.classification.classifiers.NaiveBayesClassifier')
IOUtil = SafeJClass('com.hankcs.hanlp.corpus.io.IOUtil')


def train_or_load_classifier():
    model_path = sogou_corpus_path + '.ser'
    if os.path.isfile(model_path):
        return NaiveBayesClassifier(IOUtil.readObjectFrom(model_path))
    classifier = NaiveBayesClassifier()  # ���ر�Ҷ˹������
    classifier.train(sogou_corpus_path)
    model = classifier.getModel()
    IOUtil.saveObjectTo(model, model_path)
    return NaiveBayesClassifier(model)


def predict(classifier, text):
    print("��%16s��\t���ڷ���\t��%s��" % (text, classifier.classify(text)))
    # �����ȡ��ɢ����������ķֲ�����ʹ��predict�ӿ�
    # print("��%16s��\t���ڷ���\t��%s��" % (text, classifier.predict(text)))


if __name__ == '__main__':
    classifier = train_or_load_classifier()
    predict(classifier, "C�޻�2018�������������Ա ����������ѽ���")
    predict(classifier, "Ӣ���캽ĸ��ʱ8����δ���� ���й��ٶ�ԶԶ˦�����")
    predict(classifier, "�о�����¼ģʽؽ����һ��רҵ��")
    predict(classifier, "���������ʳ���ѹ,�������ʳ������")
    predict(classifier, "ͨ�ü��䲿�־�������Ŀǰ���ڿ��ǽ���������")
