import tkinter as tk
import easygui as g
import ctypes
from tkinter import scrolledtext as st
import tkinter.font as tkFont

from pyhanlp import SafeJClass
import six
# import 模型训练.新闻文本分类SVM新样本集1 as svm



global e1,e2#定义全局变量，储存标题和文件
global t2,t1
window = tk.Tk()
window.title('my window')
window.geometry('1800x900')

#尾号为1的是关于功能1的
#尾号为2的是关于功能2的


sogou_corpus_path = "新闻文本分类算法样本集+人民网+网易+旅兴网+读书网+美食台+美食天下+新浪+中华网+铁血+军事前沿+西陆+搜狗新闻库+数码科技网+科技快报网"#"新闻库（过滤停用词）"
model_path = sogou_corpus_path + '.2gram.ser'
LinearSVMClassifier = SafeJClass('com.hankcs.hanlp.classification.classifiers.LinearSVMClassifier')
IOUtil = SafeJClass('com.hankcs.hanlp.corpus.io.IOUtil')
classifier = LinearSVMClassifier(IOUtil.readObjectFrom(model_path))
def predict(classifier, text):
    res = "《%16s》\t属于分类\t【%s】" % (text, classifier.classify(text))
    print(res)
    print("各类别概率：")
    predict_dict = classifier.classify(text)
    for cat in predict_dict:
        print(cat, round(predict_dict[cat]*100, 2))
    return res
# classifier=svm.train_or_load_classifier()
def insert_1():#功能1：输入单条新闻，输出新闻的分类

    t1.place(x=180, y=580)#用于输出程序结果，处理后的结果需要编写）

    str = predict(classifier,"国内首款正版授权俄罗斯方块手游《俄罗斯方块环游记》定档7月！今日，由畅游聚变工作室打造，腾讯代理的国内唯一正版授权的俄罗斯方块手游——《俄罗斯方块环游记》正式宣布定档，将于2021年7月与各位俄罗斯方块爱好者正式见面。在俄罗斯方块环游记中")
    t1.insert(tk.INSERT,str)



#def insert_2():#在进行点击功能2按钮后才会开始读取文件信息
#    b9 = tk.Button(window, text='选择文件', width=10, height=2, command=start_job_2,font=f1)#在start_job_2中开始实现功能2
#    b9.grid(row=3,column=2)#按钮重叠，点击同一处地方即可实现功能

def start_job_2():##功能2：支持本地上传csv/xlsx文件，批量输入新闻，并输出新闻分类
    # fileopenbox()函数的返回值是你选择的那个文件的具体路径
    str1 = g.fileopenbox('open file', 'C:/User/Administrator/Desktop/__pycache__')
    # msgbox()是测试用的，可以不用写
    #g.msgbox(str1)
    global t2
    l3=tk.Label(window,text='文件路径：'+str1,font=f1)
    l3.place(x=965, y=270)
    #b2 = tk.Button(window, text='开始预测，预测结果如下', width=19, height=2, command=start_2,font=f1)#在start_2中具体实现功能2
    #b2.grid(row=4,column=2)
    t2 = st.ScrolledText(window, height=15,font=f1,width=60)
    t2.place(x=935, y=350)


def start_2():#功能2：支持本地上传csv/xlsx文件，批量输入新闻，并输出新闻分类
    t2.place(x=935, y=350)#用于输出程序结果，处理后的结果（需要编写）


f1 = tkFont.Font(family='microsoft yahei', size=16) # 字体设定

l = tk.Label(window,text=' ')
l1 = tk.Label(window,text='功能1：输入单条新闻，输出新闻的分类',width=75,font=f1)
l2 = tk.Label(window,text='功能2：支持本地上传xlsx文件  ，批量输入新闻,并输出新闻分类',width=83,font=f1)
l3 = tk.Label(window,text=' ')


l.grid()
l1.grid()#功能1的简介
l3.grid()
#功能1的板块
l4=tk.Label(window,text='标题:',width=60,anchor="w",font=f1)
l4.grid(row=4,column=0)
e1=st.ScrolledText(window,width=50,font=f1,height=2)#标题(输入的标题保存在e1中)在之前定义过全局变量，所以在函数中可以直接使用
e1.grid(row=4,column=0)
l4=tk.Label(window,text='文本:',width=60,anchor="w",font=f1)
l4.grid(row=5,column=0)
e2=st.ScrolledText(window,width=50,height=10,font=f1)#文本(输入的文本保存在e2中)
e2.grid(row=5,column=0)
b1 = tk.Button(window, text='执行功能1', width=10, height=2, command=insert_1,font=f1)#在insert_1中实现功能1
b1.place(x=415, y=460)
t1=st.ScrolledText(window,height=15,width=85)
t1.place(x=180, y=580)


l2.place(x=750, y=25)#功能2的简介
#功能2的板块
#l3=tk.Label(window,text=' ',font=f1)
#l3.place(x=1300, y=50)
#b2=tk.Button(window,text='执行功能2',width=10, height=2,command=insert_2,font=f1)#在insert_2中实现打开文件的操作
#b2.grid(row=4,column=2,padx=50,pady=10)
b9 = tk.Button(window, text='选择文件', width=10, height=2, command=start_job_2,font=f1)#在start_job_2中开始实现功能2
b9.place(x=1220, y=75)
b2 = tk.Button(window, text='开始预测，预测结果如下', width=19, height=2, command=start_2,font=f1)#在start_2中具体实现功能2
b2.place(x=1160, y=170)
t2=st.ScrolledText(window,font=f1,height=15,width=60)
t2.place(x=935, y=350)


# 适配dpi
try:  # >= win 8.1
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except:  # win 8.0 or less
    ctypes.windll.user32.SetProcessDPIAware()
ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
window.tk.call('tk', 'scaling', ScaleFactor/75)

window.mainloop()