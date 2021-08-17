import tkinter as tk
import easygui as g
import ctypes
from tkinter import scrolledtext as st
from tkinter import messagebox
import tkinter.font as tkFont
import text_classifier as tc
import numpy
import six
import jpype

global e1,e2,t1,t2,t3#定义全局变量，储存标题和文件
global classifier, file_dir

#所需函数


#功能1：输入单条新闻，输出新闻的分类
def text_analysis():
    # t1.place(x=180, y=580)#用于输出程序结果，处理后的结果需要编写）
    t1.delete(1.0, "end")
    title = e1.get(1.0, "end")
    content = e2.get(1.0, "end")
    if title != "\n" or content != "\n":
        res = tc.classify(title, content, classifier)
        t1.insert("end", res)


#功能2.1：支持本地上传csv/xlsx文件，批量输入新闻
def file_in():
    global file_dir
    file_dir = g.fileopenbox('open file', 'C:/User/Administrator/Desktop/__pycache__')
    t2.delete(1.0, "end")
    if file_dir != "":
        if ".xlsx" not in file_dir:
            messagebox.showwarning('警告', '请选择后缀为.xlsx的文件！')
            file_dir == ""
        else:
            t3.delete(0, "end")
            t3.insert("end", file_dir)


#功能2.2：输出新闻分类
def file_analysis():
    print(file_dir)
    if ".xlsx" not in file_dir:
        messagebox.showwarning('警告', '请选择后缀为.xlsx的文件！')
    else:
        t2.delete(1.0, "end")
        t2.insert("end", "正在运行中，请稍后……\n")
        status = tc.classify_all(file_dir, classifier)
        if status:
            t2.insert("end", "已完成")




if __name__ == "__main__":
    # 加载模型
    model_path = "svm_2gram.ser"
    classifier = tc.load_model(model_path)

    # 参数初始化
    file_dir = ""

    # 定义窗口
    window = tk.Tk()
    window.title('my window')
    window.geometry('1800x1000')
    #文本编辑
    f1 = tkFont.Font(family='microsoft yahei', size=16) # 字体设定
    l = tk.Label(window,text=' ')
    l1 = tk.Label(window,text='功能1：输入单条新闻，输出新闻的分类',width=75,font=f1)
    l2 = tk.Label(window,text='功能2：支持本地上传xlsx文件  ，批量输入新闻,并输出新闻分类',width=83,font=f1)
    # dir_info = StringVar()
    t3 = tk.Entry(window, font=f1, width=60)
    # l3 = tk.Label(window, font=f1, textvariable=dir_info)
    # l3.place(x=965, y=270)
    l4 = tk.Label(window, text='标题:', width=60, anchor="w", font=f1)
    e1 = st.ScrolledText(window, width=50, font=f1, height=2)  # 标题(输入的标题保存在e1中)在之前定义过全局变量，所以在函数中可以直接使用
    l4 = tk.Label(window, text='文本:', width=60, anchor="w", font=f1)
    e2 = st.ScrolledText(window, width=50, height=10, font=f1)  # 文本(输入的文本保存在e2中)
    b1 = tk.Button(window, text='执行功能1', width=10, height=2, command=text_analysis, font=f1)  # 在text_analysis中实现功能1
    t1 = st.ScrolledText(window, height=12, width=50, font=f1)
    b9 = tk.Button(window, text='选择文件', width=10, height=2, command=file_in, font=f1)  # 在file_in中开始实现功能2
    b2 = tk.Button(window, text='开始预测，预测结果如下', width=19, height=2, command=file_analysis, font=f1)  # 在file_analysis中具体实现功能2
    t2 = st.ScrolledText(window, font=f1, height=10, width=60)
    tips = tk.Label(window, text="注意：当样本集较大时，程序可能会暂时性卡死数分钟，请耐心等待", anchor="w", font=f1)

    #板块放置

    # 功能1的板块放置
    l.grid()
    l1.grid()
    # l3.grid()
    l4.grid(row=4,column=0)
    e1.grid(row=4,column=0)
    l4.grid(row=5,column=0)
    e2.grid(row=5,column=0)
    b1.place(x=415, y=460)
    t1.place(x=180, y=580)

    # 功能2的板块放置
    l2.place(x=750, y=25)
    b9.place(x=1220, y=75)
    b2.place(x=1160, y=170)
    t2.place(x=935, y=350)
    t3.place(x=935, y=275)
    tips.place(x=935, y=700)

    # 适配dpi
    try:  # >= win 8.1
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except:  # win 8.0 or less
        ctypes.windll.user32.SetProcessDPIAware()
    ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
    window.tk.call('tk', 'scaling', ScaleFactor/75)

    window.mainloop()